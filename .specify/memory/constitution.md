# [PROJECT_NAME] Constitution
<!-- Example: Spec Constitution, TaskFlow Constitution, etc. -->

## Core Principles

### [PRINCIPLE_1_NAME]
<!-- Example: I. Library-First -->
[PRINCIPLE_1_DESCRIPTION]
<!-- Example: Every feature starts as a standalone library; Libraries must be self-contained, independently testable, documented; Clear purpose required - no organizational-only libraries -->

### [PRINCIPLE_2_NAME]
<!-- Example: II. CLI Interface -->
[PRINCIPLE_2_DESCRIPTION]
<!-- Example: Every library exposes functionality via CLI; Text in/out protocol: stdin/args → stdout, errors → stderr; Support JSON + human-readable formats -->

### [PRINCIPLE_3_NAME]
<!-- Example: III. Test-First (NON-NEGOTIABLE) -->
[PRINCIPLE_3_DESCRIPTION]
<!-- Example: TDD mandatory: Tests written → User approved → Tests fail → Then implement; Red-Green-Refactor cycle strictly enforced -->

### [PRINCIPLE_4_NAME]
<!-- Example: IV. Integration Testing -->
[PRINCIPLE_4_DESCRIPTION]
<!-- Example: Focus areas requiring integration tests: New library contract tests, Contract changes, Inter-service communication, Shared schemas -->

### [PRINCIPLE_5_NAME]
<!-- Example: V. Observability, VI. Versioning & Breaking Changes, VII. Simplicity -->
[PRINCIPLE_5_DESCRIPTION]
<!-- Example: Text I/O ensures debuggability; Structured logging required; Or: MAJOR.MINOR.BUILD format; Or: Start simple, YAGNI principles -->

## [SECTION_2_NAME]
<!-- Example: Additional Constraints, Security Requirements, Performance Standards, etc. -->

[SECTION_2_CONTENT]
<!-- Example: Technology stack requirements, compliance standards, deployment policies, etc. -->

## [SECTION_3_NAME]
<!-- Example: Development Workflow, Review Process, Quality Gates, etc. -->

[SECTION_3_CONTENT]
<!-- Example: Code review requirements, testing gates, deployment approval process, etc. -->

## Governance
<!-- Example: Constitution supersedes all other practices; Amendments require documentation, approval, migration plan -->

[GOVERNANCE_RULES]
<!-- Example: All PRs/reviews must verify compliance; Complexity must be justified; Use [GUIDANCE_FILE] for runtime development guidance -->

**Version**: [CONSTITUTION_VERSION] | **Ratified**: [RATIFICATION_DATE] | **Last Amended**: [LAST_AMENDED_DATE]
<!-- Example: Version: 2.1.1 | Ratified: 2025-06-13 | Last Amended: 2025-07-16 -->

---

# Super-SpecKit delivery policy (appended)

## Independent verification

Changes SHALL follow a persisted PStack playbook. Normal/milestone work SHALL use native Spec Kit specification, plan, and tasks; bounded micro work SHALL use a compact playbook and requirement matrix. A feature is not merge-ready merely because code review, OCR, or unit tests pass. Each requirement SHALL map to verification evidence or an explicit `not-verified`/`not-applicable` rationale. Candidate commits SHALL be checked in an independent clean QA clone or explicitly selected worktree. Confirmed defects SHALL receive durable bug artifacts, regression coverage when practical, and independent retest before closure.

## Native feedback loops

Before any material implementation, the orchestrator SHALL discover and run the cheapest real feedback loop available for the changed behavior. Tests use red-green development at an agreed public seam when possible. Other work SHALL use an equivalent observable loop such as API/DB assertions, browser or visual checks, trace replay, simulator, fixture, differential, performance, or bounded human observation. A successful command exit, static analysis, or source reading alone is not proof. Missing feedback capability is a tracked engineering gap, not permission to guess.

## Purpose and adversarial understanding

Before technical implementation begins, the intended outcome, affected people, success signal, and non-goals SHALL be human-confirmed in a Purpose Map. For normal/milestone scope a separate evidence-labeled Spec Grill SHALL challenge the resulting spec; agents may resolve technical questions autonomously but SHALL return to the Purpose Gate when discovery would materially alter the confirmed purpose.

## Architecture and engineering acceptance

Every delivery SHALL inspect relevant local structure and language/framework guidance before choosing its implementation. New playbook-led deliveries SHALL retain research and architecture receipts, executable project-specific boundaries, durable-state owners and narrow exceptions. Release SHALL require independent engineering review of the exact candidate and real user-journey evidence. Green tests alone SHALL NOT establish usability. One code writer SHALL own each checkout. Unattended continuation SHALL require an observed host runner, persisted predicate, authority, budget and checkpoints.

## Shared understanding and prevention

PStack investigation SHALL establish relevant conventions, constraints and applicable lessons before scope selection or Spec Kit planning. Small understood features MAY use micro. New knowledge-v2 deliveries SHALL retain source-bound playbook steps, digest-bound shared design and exact-candidate independent result with convention reconciliation. Archify SHALL render relevant Atlas, Change Story and Bug Story when available; fallback limitations SHALL be disclosed. Diagram checks SHALL NOT substitute for behavior or architecture enforcement. Bugs SHALL retain supported cause, regression coverage or justified alternative, independent retest, visual explanation and scoped prevention. Lessons SHALL favor demonstrated structural/test protection and be retrieved when applicable to future investigation.

