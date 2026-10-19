# AgentWatch Contributor & Engineering Guidelines

> **Project Maintainer:** [Shinraya-Tech-Labs](https://github.com/Shinraya-Tech-Labs)  
> **Repository:** [Shinraya-Tech-Labs/AgentWatch](https://github.com/Shinraya-Tech-Labs/AgentWatch)  
> **Programs:** SSOC 2026, NSOC 2026, ELUSoC 2026, and Open Community Contributors  

AgentWatch is a high-assurance, evidence-first observability and formal verification engine for AI agents. Because the core engine operates under strict formal logic, mathematical invariants, and zero-trust security standards, **contributions are held to rigorous production engineering standards**.

---

## ⚡ Quick Summary for Contributors (TL;DR)

Before contributing to AgentWatch (under NSoC, SSoC, or open community cycles), make sure you understand these **4 core rules**:

| Rule | Requirement | Details |
| :--- | :--- | :--- |
| **1. Discord Membership** | **Mandatory** | You **must** join our official Discord server: [**https://discord.gg/UT9uaeY46e**](https://discord.gg/UT9uaeY46e). |
| **2. Discord Proof on Claim** | **Required in comment** | Provide your exact Discord username (e.g., `Discord Handle: @username`) in your assignment request. |
| **3. Technical Plan** | **Required (No `/claim`)** | Bare `/claim` requests are declined. Outline your architectural approach, files to change, and test strategy. |
| **4. Max 3 Concurrent Issues** | **Cap of 3 issues** | Contributors can be assigned a **maximum of up to 3 active issues** at a time. |
| **5. 72-Hour Progress SLA** | **No issue camping** | Submit a draft PR or progress update within 72 hours of assignment, or the issue is re-assigned. |

---

## 🚫 1. Anti-Spam & AI-Generated Slop Policy

We take code quality and review time seriously. 

1. **Zero Hallucinated / AI-Slop Code**:
   - Submitting unreviewed, blind copy-pastes from ChatGPT, Claude, or other LLMs is strictly prohibited.
   - You must thoroughly understand every line of code you submit. In PR reviews, maintainers will ask specific questions about your design decisions. Inability to explain your implementation will result in immediate PR closure.
2. **No "Issue Farming" or Reservation Camping**:
   - Claiming issues without active work is prohibited.
   - Splitting a single feature into multiple trivial issues or PRs solely to inflate contest metrics will result in disqualification.
3. **No Mass or Automated Issues**:
   - Do not open generic automated scanner reports or boilerplate issues without a verified, reproducible failure in AgentWatch.

---

## 📋 2. Mandatory Issue Assignment & 72-Hour Inactivity Rule

To maintain fair opportunities and prevent duplicate work:

1. **Mandatory Discord Membership & Proof Required**:
   - All contributors **must join the official AgentWatch Discord community**: **[https://discord.gg/UT9uaeY46e](https://discord.gg/UT9uaeY46e)**.
   - When requesting assignment to any issue, you **must include proof of Discord membership** (your Discord username / handle) in your comment. Requests lacking Discord proof will not be assigned.
2. **Never open a PR without an assigned issue**:
   - PRs submitted for unassigned issues will be **closed immediately without review**.
3. **How to Request Assignment**:
   - Comment on the issue with your Discord handle and a **concrete, step-by-step Technical Implementation Plan**:
     ```text
     I would like to be assigned to this issue.
     
     Discord Handle: @my_discord_username
     Proof of Membership: Member of AgentWatch Discord
     
     Technical Implementation Plan:
     1. Architectural Plane: Plane B (Interpretation Plane)
     2. Files to Modify: agentwatch/events/normalizer.py, agentwatch/contracts/evaluator.py
     3. Invariant & Edge Cases Handled: Clock skew where delta exceeds window bound
     4. Testing Strategy: Add unit test in tests/contracts/ verifying overlapping intervals
     ```
   - Wait for maintainer approval and official GitHub assignment.
4. **Concurrent Assignment Limit (Max 3 Issues)**:
   - A contributor may hold a **maximum of up to 3 assigned issues concurrently**.
   - Contributors must demonstrate active progress on their existing assigned issues before requesting additional ones.
5. **Strict 72-Hour Inactivity Expiration**:
   - Once assigned, you have **72 hours** to submit a draft PR or post a verified progress update.
   - If an issue sits idle for 72 hours with no communication, **you will be automatically unassigned**, and the issue will be released to other contributors.

---

## 🛡️ 3. Non-Negotiable Security Standards (`SECURITY-BASELINE.md`)

AgentWatch operates under a **Zero-Baseline Security Standard**:

1. **Absolute Prohibition of Baseline Files**:
   - Never create or modify `bandit-baseline.json` or any global suppression file.
   - Any PR introducing a baseline file will be automatically rejected.
2. **Scoped Inline Suppressions Only**:
   - If a line of code genuinely triggers a false positive (e.g., non-cryptographic seeded PRNGs for reproducible statistical tests), it must be suppressed inline with the exact format:
     ```python
     rng = random.Random(seed)  # noqa: S311  # nosec B311 — seeded statistics for drift permutations
     assert anchor is not None  # nosec B101 — invariant: caller must pass start or end timestamp
     ```
   - Three elements are mandatory:
     - `# nosec <TEST-ID>`: Scoped strictly to the specific check (never a bare `# nosec`).
     - `# noqa: <RULE>`: Scoped for Ruff consistency.
     - **A prose reason**: Explaining why standard cryptographic or assertion safeguards do not apply.
3. **Mandatory Documentation**:
   - Every new suppression must be added with an architectural justification table in [`SECURITY-BASELINE.md`](SECURITY-BASELINE.md).

---

## 🧪 4. Test-Driven Development (TDD) & Quality Gates

Every pull request must pass all local quality gates before submission:

### 1. Test Coverage Requirement
- **No Untested Code**: Every bug fix must include a regression test proving the fix. Every new feature must include comprehensive unit tests.
- **Coverage Gate**: Test coverage across the modified package must satisfy the repository gate (**>= 70%**).
- Tests must be deterministic (no flaky sleep calls, no external network dependencies).

### 2. Format & Linting Standards
Code must adhere strictly to Ruff formatting rules (Python 3.12+, 100 character line length, double quotes):

```bash
# Check formatting
ruff format --check agentwatch/

# Check linter rules
ruff check agentwatch/

# Run security scan
bandit -r agentwatch
```

### 3. Architecture Plane Boundaries
Code must respect the 6 Architectural Planes ([`docs/v3/V3_ARCHITECTURE.md`](docs/v3/V3_ARCHITECTURE.md)):
- `Evidence Plane` (Plane A) contains immutable raw envelopes.
- `Interpretation Plane` (Plane B) normalizes observations into `ComputationalEvent`s.
- `Structure Plane` (Plane C) handles graph and provenance relations.
- Lower planes must **never** import from higher planes. Violating plane boundaries will block PR approval.

---

## 🔄 5. Git & PR Hygiene

1. **One PR per Issue**: Keep diffs focused, minimal, and atomic ("Ponytail" principle). Do not bundle unrelated refactors into a bug fix.
2. **Conventional Commits**:
   - `feat(contracts): implement interval precedence check`
   - `fix(sensors): resolve span orphan drop on late delivery`
   - `test(causality): add permutation test for blast radius`
   - `docs(vault): update architecture planes diagram`
3. **Synchronize with `main`**:
   - Always rebase your branch on `origin/main` before opening or updating a PR:
     ```bash
     git fetch origin main
     git rebase origin/main
     ```

---

## 💬 6. Discord & Community Collaboration

For architectural discussions, RFC proposals, or questions regarding mid/hard issues:
- **Discord Server**: [https://discord.com/invite/ZbQ9m9HtnE](https://discord.com/invite/ZbQ9m9HtnE)
- **Maintainer Escalation**: Ping `@Project Admin` in `#contributors` channel.

Failure to follow these guidelines may result in assignment revocation, PR rejection, or removal from mentorship program leaderboards.
