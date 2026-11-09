# Investigation — build tooling (2026-11-07)

- mise.toml pins node 24.14.0 + pnpm 10.33.2; tasks: install → bootstrap → dev (desktop test env, isolated data dir ~/.zcode-dev-home)
- Machine has node v22.23.3 global → must use mise (not installed yet) or install node 24 to build
- Root build = `pnpm -r build`; desktop = packages/desktop (Electron, electron-builder.config.js, native/ dir)
- ELECTRON_MIRROR points to npmmirror (CN network); may need override for Thailand network
- Dev entry: `mise dev` → pnpm dev:desktop:test (isolated local test env)
