# Feature Specification: ZBill M1 — fork builds and runs as 3-panel native app

**Feature Branch**: `zbill/m1-scaffold`

**Created**: 2026-11-07

**Status**: Draft

**Input**: User vision: fork ZCode into a simple native app — file panel (left), AI (center), output files (right) — that generates monthly EV-charging reimbursement reports. M1 proves the fork builds, launches, and the billing skill produces xlsx+PDF visible in the output panel.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Engineer builds the app from fork source (Priority: P1)

A developer clones Poom5741/ZCode-bill, installs the pinned toolchain (mise: node 24.14.0, pnpm 10.33.2), runs install + build, and obtains a launchable macOS desktop app.

**Why this priority**: Nothing else is possible until the fork builds.

**Independent Test**: `mise install && pnpm install && pnpm build` exit 0 and a launchable Electron artifact exists.

**Acceptance Scenarios**:
1. **Given** a clean clone on macOS arm64, **When** pinned toolchain install runs, **Then** exit code 0
2. **Given** installed dependencies, **When** `pnpm build` runs, **Then** exit code 0 with desktop artifact produced

### User Story 2 - User launches the app and sees the 3-panel shell (Priority: P1)

The built app launches on macOS and displays: file tree (left), AI agent chat (center), output/document panel (right).

**Why this priority**: This shell IS the product shape; everything else renders inside it.

**Independent Test**: Launch the app from build output; screenshot shows all three panels.

**Acceptance Scenarios**:
1. **Given** the built app, **When** launched, **Then** window opens with 3 visible panels
2. **Given** the app is running, **When** the user opens a file from the left tree, **Then** it renders in a center/right surface

### User Story 3 - User generates a monthly reimbursement report inside the app (Priority: P2)

With fixture receipts present in the workspace, the user asks the AI to create the monthly report; the billing skill runs the proven pipeline and the produced xlsx+PDF open in the output panel.

**Why this priority**: This is the product's core value demo; needs the shell working first.

**Independent Test**: With fixture inbox prepared, invoking the skill in the running app produces output files that open in the panel.

**Acceptance Scenarios**:
1. **Given** fixture receipts in the project workspace, **When** user asks for the monthly report, **Then** xlsx+PDF are produced
2. **Given** produced report, **When** opened from the app, **Then** document panel renders it (Thai text correct, receipt images visible)

### User Story 4 - Upstream provenance is documented (Priority: P3)

The exact upstream base SHA and the fork's ZBill additions are documented so future syncs from zai-org/ZCode are tractable.

**Why this priority**: Prevents unmergeable fork drift; no runtime behavior.

**Independent Test**: evidence/upstream-base.md exists with base SHA and diff summary.

**Acceptance Scenarios**:
1. **Given** the M1 branch, **When** reading evidence/upstream-base.md, **Then** it names base SHA, added files, and no edits to legacy modules

## Requirements *(from verification matrix ZBILL-M1-matrix.md)*

R-001 toolchain install clean; R-002 desktop build; R-003 launch + 3-panel shell; R-004 billing skill report visible in panel; R-005 upstream provenance documented.

## Constraints

- Toolchain via mise only (mise.toml pins); never global node
- ZBill additions locally contained: new top-level dirs (billing skill, fixture data, evidence); no edits inside legacy modules (rpc/shared/provider/services per architecture-policy.yaml)
- Desktop dev/QA runs in isolated data dir (dev:desktop:test), never the user's real profile
- Thai rendering must use proven stack (fpdf2 + HarfBuzz); LibreOffice headless is broken for Thai on this machine

## Non-goals (deferred)

Gmail OAuth wizard (M2), re-branding (M3), Windows packaging (M4), multi-tenant billing
