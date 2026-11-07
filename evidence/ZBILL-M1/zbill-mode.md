# ZBill product-mode changes (2026-11-07 12:59)

Purpose-built surface changes (user feedback: "still looks like ZCode"):
- vite define __ZBILL_PRODUCT__ from env ZBILL_PRODUCT=1 (packages/desktop/vite.config.ts)
- ZBILL_PRODUCT const in packages/shared/src/env.ts (+ "./env" export)
- ProjectSidebarNavigation hides Automations + Plugin Marketplace buttons in ZBill mode
- mise dev task sets ZCODE_DESKTOP_APPLICATION_NAME=ZBill + ZBILL_PRODUCT=1
- Verified: menu bar "ZBill", user-data dir "Application Support/ZBill"; error overlay
  from .js-suffixed import fixed (screenshot zbill-mode-login.png)
Remaining for purpose-built feel (next iteration): welcome-screen branding ("Welcome to
ZCode" i18n), suggested prompts (server scene), file/output panel defaults.
