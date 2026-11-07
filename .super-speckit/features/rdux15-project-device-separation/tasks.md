# Tasks — RDUX15 项目创建与远程连接管理分离

Ordered; each task names its evidence seam. Scenario IDs = ticket acceptance list.

- [ ] T1 (M1): Map RDUX15 scenarios to case catalog + coverage matrix; add failing E2E/integration
      skeletons for RDUX15-01/02/03/06/08 at the three real entries (red first). Evidence: test files + run log.
- [ ] T2 (M1): Direct-create project form (name/device/folder single surface) replacing pre-screen;
      default device per Q3; offline device retained with status. [REQ-01, REQ-02] RDUX15-01/02.
- [ ] T3 (M1): Device dropdown from added-device facts only; 添加远程设备… entry; no discovery
      candidates. [REQ-03] RDUX15-03.
- [ ] T4 (M1): Existing-device no-connect rule; online 添加文件夹 / offline 连接并选择文件夹 in-flow.
      [REQ-06] RDUX15-06/07 (WSL/Docker real evidence first).
- [ ] T5 (M2): Settings categorized add window (SSH default, WSL/Docker capability-gated, discovery
      failure non-blocking); primary action 添加并连接. [REQ-05] RDUX15-05.
- [ ] T6 (M2): Rewire three entries (sidebar composer form, chat menu 「新建远程连接…」, settings) to
      the same settings section + window. [REQ-04] RDUX15-04.
- [ ] T7 (M2): Settings-sourced completion = locate device card, no project continuation.
      [REQ-08] RDUX15-10.
- [ ] T8 (M3): Completion-intent dispatch via existing remote-connection-flow seam: return-to-draft
      with Q7 confirm on folders; chat source folder resolve per #21; background continue notify-only.
      [REQ-09, REQ-10, REQ-14] RDUX15-11/12/14/19.
- [ ] T9 (M3): Cancel/close/Esc semantics + late-result inertia via existing request invalidation.
      [REQ-15, REQ-16] RDUX15-13/20/21.
- [ ] T10 (M4): Existing-project secondary entry (identity-preserving attach, draft retained,
      duplicate-add guard, read-only legacy support); local multi-root preserved. [REQ-11, REQ-12]
      RDUX15-15/16/17.
- [ ] T11 (M5): Credential/install confirmations preserved + retry; unused credentials never
      overwrite. [REQ-13] RDUX15-18/21/22 (real remote evidence).
- [ ] T12 (M6): Keyboard/focus/Esc layering + a11y assertions; theme/language/narrow-window visual
      evidence; web/mobile capability regression. [REQ-17, REQ-18, REQ-19] RDUX15-23/24/25.
- [ ] T13: All gates green on final candidate; convergence (native); evidence pack + handoff.
