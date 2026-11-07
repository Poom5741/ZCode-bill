# Architecture contract — doc-retriage-2026-11 (docs-only delivery)

## Scope of writable files

- Status/verdict markers inside exactly these 11 documents under `docs/issues/`:
  remote-connection-ux/01, remote-performance-3-16/01, remote-startup-failures-3-16/01,
  ttft-stage-telemetry/01+02, web-remote-control-relay-v2/02..07.
- New consolidated report: `docs/issues/RETRIAGE-2026-11.md`.
- Feature artifacts under `.super-speckit/features/doc-retriage-2026-11/` and feature state under
  `.super-speckit/state/features/` (kit-owned).

## State ownership

- `docs/issues/RETRIAGE-2026-11.md` is the single owner of triage verdicts.
- Individual docs own only their own status line; the report references, never duplicates, their
  evidence beyond a summary row.

## Dependency / boundary rules (validated)

- No imports, no code files, no config, no schema changes: a docs-only feature cannot add
  dependencies. Check: after the candidate commit, `git diff --stat` must touch only the files
  listed above (plus kit state). A diff touching `packages/` or `apps/` violates this contract.
- Forbidden example (mechanically rejected): editing any file under `packages/**` or `apps/**` —
  outside this feature's declared writable set.
- Valid path: status marker + verdict note inside a triaged doc, citing evidence that exists at
  the candidate commit.

## Public interfaces

- None added. The report is a new documentation entry point for future backlog consumers.

## Exceptions

- None. Any need to touch product code voids this contract and re-routes the feature.
