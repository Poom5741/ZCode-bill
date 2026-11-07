{
  "writable_scope": "packages/ui（project-sidebar、remote-connection-flow、data-sync 设置段、app-shell 类型、i18n、store/hooks）、packages/desktop wdio 测试、.super-speckit 工件",
  "state_owners": "项目草稿单一 owner（store via hooks）；连接事实归既有 Host 服务；返回意图仅 renderer 内存",
  "dependency_rules": "组件经 hooks 访问服务（packages/ui/AGENTS.md）；不直调 window.zcode；不新增第二套向导/管理 API；不改变任务协议与 workspace 身份",
  "forbidden_example": "组件内直接调用服务实例或新建凭据缓存 → 拒绝",
  "valid_path": "新完成意图分派经 store action + 既有 seam 回调",
  "executable_check": "pnpm architecture:check --changed + 既有架构基线"
}
