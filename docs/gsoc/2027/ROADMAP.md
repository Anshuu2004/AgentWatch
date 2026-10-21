# Paptonis — GSoC 2027 Organization Preparation Roadmap

> **Status:** Proposed for maintainer review · **Updated:** 21 October 2026  
> **Organization:** Shinraya Tech Labs · **Current repository:** https://github.com/Shinraya-Tech-Labs/AgentWatch  
> **Internal readiness target:** **15 January 2027** (not an official Google deadline)  
> **Application status:** Not submitted. Participation and selection are not guaranteed.

## Mission and boundaries

Prepare Paptonis (formerly known as AgentWatch; repository branding and migration remain to be reconciled) to apply as a **GSoC 2027 mentoring organization, if eligible**. The immediate goal is **credible community and mentoring capacity**, not maximizing features, stars or issue counts.

The technical direction under review is evidence-first, passive observability for AI-native systems: capture execution evidence, reconstruct provenance, compare runs, and offer **bounded** replay with explicit limitations. Do not claim arbitrary deterministic replay, causal certainty, or implementation completeness without testing.

**Naming blocker:** the current README uses **Panopti** while maintainers have selected **Paptonis**. The repo path remains `AgentWatch`. Make a separate, reviewed branding decision before renaming packages, namespaces, repositories or releases. Preserve compatibility and redirects where possible.

## First gate: eligibility and honesty

Check the *official 2027* GSoC rules when published. Google's **2026** organization guidance referenced a project with **18+ months of history**, at least **five active community members**, released OSI-approved licensed software and demonstrable mentoring capability. These are **2026 reference criteria**, not confirmed 2027 rules.

- [ ] Collect dates and links for earliest public project activity, releases and sustained development. Do not assume a new organization account proves or disproves underlying project history.
- [ ] Verify license, source availability, and released software.
- [ ] Count actual active community participants and independently reviewed PRs; exclude bots and superficial participation.
- [ ] Recruit and confirm at least two eligible organization administrators under the applicable rules.
- [ ] Determine whether standalone application is realistic. If not, explore working through an established eligible mentoring organization or defer. Never misstate eligibility.

References: [GSoC FAQ](https://developers.google.com/open-source/gsoc/faq), [Mentor guide](https://google.github.io/gsocguides/mentor/org-application), [GSoC timeline](https://developers.google.com/open-source/gsoc/timeline), [2026 organization call](https://opensource.googleblog.com/2026/01/mentor-org-applications-for-google-summer-of-code-2026-open-through-feb-3.html).

## Ownership: two-person execution

| Workstream | Accountable | Evidence |
|---|---|---|
| Organization eligibility, governance, community, GSoC application, mentors, newcomer experience | **OSS & GSoC lead** (founder) | Public policies, commitments, activity data, documented reviews |
| Product architecture, v3 implementation audit, tests, CI, benchmarking and technical roadmap | **Technical lead** (friend) | Verified feature matrix, reproducible demonstrations, CI/benchmarks |
| GSoC ideas and milestone definitions | **Joint**: OSS lead owns mentorship/scope, technical lead approves feasibility | Mentor-owned project briefs with measurable criteria |
| Application go/no-go | **Joint**, with actual organization administrators | Written evidence-backed decision |

No one becomes an organization administrator or mentor merely by being given a title here. Get affirmative commitment and weekly availability.

## Phase 0 — Project identity and baseline (21–31 October 2026)

**Accountable:** OSS & GSoC lead; technical lead verifies code.

- [ ] Publish evidence for project history and the eligibility risk.
- [ ] Audit current `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md` and existing governance before creating or changing files.
- [ ] Agree on product identity and clearly separate v3 passive behavior from legacy active-guardrail functionality.
- [ ] Create a public `docs/gsoc/2027/READINESS_EVIDENCE.md` listing each requirement, status (verified / at risk / unknown), proof link and owner.
- [ ] Export a 90-day community baseline: unique external contributors, actual merged PRs, repeat contributors, first-review median and p90, and active reviewers.

**Exit criterion:** written eligibility status and truthful implementation/community baseline, without inferred numbers.

## Phase 1 — Contributor and governance foundation (1–15 November 2026)

**Accountable:** OSS & GSoC lead.

- [ ] Publish `GOVERNANCE.md` and `MAINTAINERS.md` after assigning genuine review, release and escalation responsibilities.
- [ ] Simplify newcomer onboarding in `CONTRIBUTING.md`; small docs/test PRs should not require private instructions or mandatory chat membership.
- [ ] Create `START_HERE.md`, a quickstart and an introductory architecture tour.
- [ ] Test clone → install → test → tiny PR with **two people outside the core maintainers**.
- [ ] Curate **8–15 real, bounded** `good first issue` tasks with acceptance criteria and reviewer.
- [ ] Establish a public discussion space for technical decisions and a confidential vulnerability reporting route.
- [ ] Set *internal* service goals: acknowledge newcomer questions within two working days and provide initial PR reviews within three working days.

**Exit criterion:** newcomers can contribute without insider knowledge, and maintainers demonstrably respond.

## Phase 2 — Technical proof and sustained community activity (16 November–15 December 2026)

**Accountable:** Technical lead for code; OSS & GSoC lead for community.

- [ ] Produce an `implemented / partial / documented-only / unverified` v3 capability matrix, referencing code and tests.
- [ ] Demonstrate a reproducible record → reconstruct → compare → bounded replay workflow, with nondeterminism limits made explicit.
- [ ] Run AWBench against **fresh independent workloads**, disclose methodology and limitations; do not invent performance advantages.
- [ ] Keep critical CI gates reproducible; report measured coverage, test failures, dependency findings and release checks.
- [ ] Hold at least two public newcomer contribution/review sessions; publish follow-ups.
- [ ] Track first-time PRs, second PRs, independent code reviews and response times throughout the period.
- [ ] Recruit genuinely qualified mentors with declared availability, subsystem expertise and backup coverage.

**Exit criterion:** usable evidence-backed engineering plus observed contributor mentoring, not just documentation.

## Phase 3 — Mentor-owned project ideas (16 December 2026–5 January 2027)

**Accountable:** Joint.

Draft **three to five** independent project ideas; publish only those with committed mentors and bounded acceptance tests. Candidate areas (not promises):

1. **AWBench fresh held-out validation:** reproducibility, representative fixtures and benchmark reports.
2. **Cross-source artifact lineage:** precision/recall of evidence-grounded provenance links.
3. **Lightweight packaging and local DX:** core/extras separation, clean install and migration validation.
4. **Replay-fidelity and side-effect boundaries:** only with a qualified replay/systems mentor.
5. **Privacy-aware evidence capture:** configurable redaction, adversarial fixtures and retention tests.

Each idea must specify current verified behavior, scope, prerequisites, approximate project size **subject to 2027 rules**, primary and backup mentors, skills, milestone 1, a mergeable midpoint, final outcome, tests, failure modes and safe scope cuts. Qualification tasks should be genuinely small, not unpaid portions of the whole project.

**Exit criterion:** each published idea is feasible and independently mentor-able.

## Phase 4 — Application go/no-go (6–15 January 2027)

**Accountable:** OSS & GSoC lead, approved by committed administrators and mentors.

- [ ] Recheck **official 2027 eligibility and application dates**; update this roadmap.
- [ ] Verify age, community, licensing, releases, mentor depth and reviewer responsiveness.
- [ ] Publish public GSoC landing/ideas/FAQ/proposal resources and transparent selection and evaluation processes.
- [ ] Get external review of the application narrative, contributor walkthrough and project scopes.
- [ ] Record decision: **standalone submission**, **established-organization collaboration**, or **deferral**, with reasons.

**Exit criterion:** supported go/no-go memo and a complete, evidence-backed application if eligible.

After acceptance, *if selected*, plan regular accessible discussions, incremental merged milestones, and mentor reviews. Operationally aim for **one or two contributors** in a first year unless qualified mentor capacity demonstrably supports more; Google controls allocations.

## Community scoreboard (targets are internal, not Google requirements)

| Metric | How to measure | Internal goal |
|---|---|---|
| Active community | Distinct humans with meaningful development/review activity | Meet verified 2027 rules; 2026 guidance referred to 5+ |
| Successful external quickstarts | Documented outsider tests | 2 |
| Beginner issues | Reviewed issue specs with bounded work | 8–15 |
| Human first response | Median/p90 business-hour time | Typically within 2 working days |
| First PR review | Median/p90 human review latency | Typically within 3 working days |
| Repeat contributors | People who return for a second meaningful change | Track; no invented target or baseline |
| Admin/mentor capacity | Actual commitments and backup availability | Meet rules and cover each offered slot |
| Technical credibility | Reproducible CI, benchmark and release evidence | Publish measured results and limitations |

Do not use forks/stars, automatic comments, or artificially generated issues as evidence of an engaged community.

## Risks and stop/go mitigations

| Risk | Mitigation |
|---|---|
| Insufficient project age or sustained community | Verify records; consider established-org collaboration or defer |
| Mentor bus factor | Assign committed backups; require reviews by people other than the founder |
| Panopti / Paptonis / AgentWatch inconsistency | Make and document brand migration decision before renaming |
| README describes unsupported capabilities | Correct claims using implementation and benchmark evidence |
| Ideas are oversized or tightly coupled | Narrow or remove them before publication |
| Official 2027 rules differ | Update requirements and timeline promptly |

## Immediate two-person sprint (21 October–4 November 2026)

**OSS & GSoC lead**
- [ ] Publish this roadmap as a reviewed repository document.
- [ ] Document 18-month history question and five-active-member reference threshold with evidence.
- [ ] Inventory community, contributor guide and current good-first-issue labels.
- [ ] Begin administrator/mentor recruitment, with explicit consent.
- [ ] Prepare governance/onboarding edits and baseline community metrics.

**Technical lead**
- [ ] Document the v3 vs legacy discrepancy and naming migration risks.
- [ ] Build actual code/test-backed feature-state matrix.
- [ ] Verify clean install, CI smoke tests and first execution-forensics workflow.
- [ ] Suggest three narrowly scoped ideas with code pointers and realistic acceptance tests.

**Joint checkpoint, 4 November:** review eligibility, first external contributor feedback, implementation evidence and project-idea feasibility.

---

*This roadmap is a proposal prepared for public review. It does not claim endorsement, confirmed GSoC 2027 dates, selection or mentor commitments.*
