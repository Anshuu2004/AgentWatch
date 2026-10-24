"""Tests for the ``panopti bench`` command (Issue #772)."""

from __future__ import annotations

import pytest

from panopti.bench import OpResult, format_bench_report, percentiles, run_bench, time_operation
from panopti.cli import main

OPERATIONS = ("Invariant regex match", "Circuit breaker observe", "Merkle witness record")


def test_bench_prints_a_table_with_every_operation(capsys):
    assert main(["bench", "--iterations", "200"]) == 0

    out = capsys.readouterr().out
    assert "200 iterations per operation" in out
    for name in OPERATIONS:
        assert name in out
    for column in ("Total (ms)", "Ops/sec", "p50", "p95", "p99"):
        assert column in out


def test_bench_uses_10000_iterations_by_default(capsys, monkeypatch):
    seen = {}

    def fake_run_bench(iterations):
        seen["iterations"] = iterations
        return [OpResult("Invariant regex match", iterations, 1.0, 1.0, 1.0, 1.0, 1.0)]

    monkeypatch.setattr("panopti.bench.run_bench", fake_run_bench)

    assert main(["bench"]) == 0
    assert seen["iterations"] == 10000
    assert "10,000 iterations per operation" in capsys.readouterr().out


def test_bench_results_are_sane():
    results = run_bench(300)

    assert [r.name for r in results] == list(OPERATIONS)
    for r in results:
        assert r.iterations == 300
        assert r.total_ms > 0
        assert r.ops_per_sec > 0
        assert 0 < r.p50_us <= r.p95_us <= r.p99_us


def test_single_iteration_is_allowed(capsys):
    assert main(["bench", "--iterations", "1"]) == 0
    assert "1 iterations per operation" in capsys.readouterr().out


@pytest.mark.parametrize(
    ("args", "message"),
    [
        (["bench", "--iterations", "0"], "--iterations must be at least 1, got 0"),
        (["bench", "--iterations", "-5"], "--iterations must be at least 1, got -5"),
        (["bench", "--iterations", "abc"], "--iterations must be a whole number, got 'abc'"),
        (["bench", "--iterations", "2.5"], "--iterations must be a whole number, got '2.5'"),
        (["bench", "--iterations"], "--iterations needs a value"),
        (["bench", "--fast"], "unexpected argument '--fast'"),
        (["bench", "200"], "unexpected argument '200'"),
    ],
)
def test_bench_rejects_bad_arguments(args, message, capsys):
    assert main(args) == 2

    captured = capsys.readouterr()
    assert message in captured.err
    assert captured.out == ""


def test_bench_help_prints_usage(capsys):
    assert main(["bench", "--help"]) == 0
    assert "panopti bench [--iterations <n>]" in capsys.readouterr().out


def test_percentiles_match_known_values():
    # 1..100 microseconds, in nanoseconds, shuffled order must not matter.
    samples = [n * 1000 for n in range(100, 0, -1)]
    p50, p95, p99 = percentiles(samples)

    assert p50 == pytest.approx(50.5)
    assert p95 == pytest.approx(95.05)
    assert p99 == pytest.approx(99.01)


def test_percentiles_of_one_sample():
    assert percentiles([2000]) == (2.0, 2.0, 2.0)


def test_time_operation_calls_the_operation_once_per_iteration_plus_warmup():
    calls = []
    result = time_operation("noop", lambda: calls.append(1), 10)

    assert result.iterations == 10
    assert len(calls) == 10 + 10  # warmup is capped at the iteration count


def test_run_bench_rejects_bad_iterations():
    with pytest.raises(ValueError, match="at least 1"):
        run_bench(0)


def test_report_has_one_row_per_result():
    results = [
        OpResult("A", 5, 1.5, 3333.0, 1.0, 2.0, 3.0),
        OpResult("Longer name", 5, 2.5, 2000.0, 4.0, 5.0, 6.0),
    ]
    lines = format_bench_report(results, 5).splitlines()

    assert lines[0] == "PANOPTI BENCH: 5 iterations per operation"
    assert len(lines) == 2 + 1 + len(results)
    assert lines[3].startswith("A ")
