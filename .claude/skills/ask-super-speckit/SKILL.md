---
name: ask-super-speckit
description: Autonomously route a feature, bug, or idea through Super-SpecKit.
---

# ask-super-speckit

Locate the active project root as the nearest ancestor containing `.super-speckit/`. The canonical Super-SpecKit instructions live at `.super-speckit/skills/ask-super-speckit/SKILL.md` relative to that root. If no ancestor contains `.super-speckit/`, explain that Super-SpecKit must first be installed into the active project and stop. Read the canonical file completely before acting, then resolve source/adapter paths inside `.super-speckit/` and state/artifact paths from the project root. Invoke bundled tools as `python3 .super-speckit/scripts/<tool>.py --repo .` from the project root where supported; the adapter CLI derives its kit path from its installation and uses `--kit .super-speckit` only when overriding it. This wrapper exists only to make the installed entry point discoverable; it is not a second source of workflow truth.
