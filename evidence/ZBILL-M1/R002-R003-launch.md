# R-002 / R-003 evidence — build & launch (2026-11-07 12:49)

- R-002 PASS: `pnpm build` exit 0 (all packages incl. desktop renderer, 29.64s rolldown build)
- R-003 PARTIAL (app launches; panel journey pending user permission):
  - Launched via `pnpm dev:desktop:test` (isolated env)
  - Dev runtime self-provisioned at .zcode-runtime/desktop-dev/44.7.0-arm64/ZCode
  - Menu bar shows "ZCode Dev" (distinct from host app) — screenshot app-launch-1.png
  - Sidebar + agent center visible; macOS permission dialog ("bypass system private window
    picker" — screen recording) must be allowed by user before folder-select journey (R-003
    file-panel + R-004 output panel verification continues after)
