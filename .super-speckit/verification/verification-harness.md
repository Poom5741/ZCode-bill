# Project Verification Harness

状态（2026-11-07，由 rdux15 配置轮次填充；live smoke 尚未运行，首次 runtime QA 前必须补跑并记录证据）。

## Launch and readiness

- Desktop app（主验证对象，RDUX15 全部入口）: `pnpm dev:desktop:test`（`ZCODE_ENV=test` 开发态桌面）。
  就绪标准：Electron 窗口出现且 renderer 无启动错误日志（`packages/ui/src/logger.ts` 输出）。
- Desktop E2E（自动 journey）: `pnpm test:e2e`（`pnpm --filter @zcode/desktop test:e2e`，WebdriverIO；
  wdio 自行构建并启动被测应用实例，测试进程外不共享）。Windows 分片：`pnpm test:e2e:windows:sharded`。
- Web 相关验证: `pnpm dev:web`（并发启动 server+web），URL 以 dev 输出为准（`gates.app_url` 留空即"按需记录"）。
- 单元/工程: `pnpm test:engineering`（全量）/ `pnpm test:engineering:affected`（受影响）。
- 确定性门禁（config 已接线）: `pnpm fmt:check` / `pnpm lint` / `pnpm typecheck` / `pnpm architecture:check --changed` / `pnpm -r build`。

## Test-data isolation

- Desktop E2E：wdio fixture 使用独立 user-data 目录（现有约定，见 `packages/desktop/test/e2e/helpers/`）；
  复用现有 helper，不新造第二套隔离机制。
- 手动 QA：使用 `qa.isolated_test_namespace`（`ss-{{run_id}}`）命名的项目/目录与测试账号；禁用生产身份。
- fixture_reset_command: 暂无独立命令（应用无服务器端 fixture）；重启应用即重置内存态，持久数据仅存在于
  隔离 namespace 目录内。

## Environment capabilities（2026-11-07 实测）

- WSL: 已安装，Ubuntu，WSL 2（`wsl --status`）→ RDUX15 的 WSL 发现/连接用例可在本机真实执行。
- Docker: 29.9.2（`docker --version`）→ Docker 远端用例可在本机真实执行。
- SSH 客户端: OpenSSH for Windows 9.5p2 → **真实 SSH 远端主机未配置**：RDUX15-07/10/18/21 的
  真实远程 E2E 需要用户提供测试 SSH 主机（地址+凭据或 config 条目），在此之前这些场景如实记为
  not-verified（环境阻塞），不得用 mock PASS 冒充。
- Journey UX 执行者: **ADE computer-use surfaces**（用户指示 2026-11-08）。Electron dev build 优先
  `ade app-control`（CDP，可断言 DOM/test-id，后台无指针）；无法附加 debug 端口时回退
  `ade screen`（Windows 私有桌面 seat）。Rakazo 已跳过（config enabled=false）。
  独立性限制如实记录：reviewer 为 ADE lane agent，非独立人类/第三方模型。
- 手机真机 relay / macOS: 不可用 → 相关场景按 ticket 的"环境阻塞必须列出"规则记录。

## Real behavior proof

- 每个 capability 在 `feature-map.md` 映射到真实公共 seam：桌面真实入口（侧栏项目加号、聊天项目菜单、
  设置远程设备页）+ 连接完成分派（`packages/ui/src/remote-connection-flow/contract.ts`）。
- 桌面 journey 使用真实运行的桌面应用（journey_ux.require_real_running_app=true）；不存在的 Playwright
  套件不作为证据来源（gates.playwright 留空是有意的，不是遗漏）。
- 涉及项目写入的断言补 API/DB 层核验（既有项目服务合同测试）。

## Evidence and cleanup

- 证据目录：`.super-speckit/qa/<run-id>/`（截图、日志、trace 按 journey_ux.capture 清单）。
- 清理：停止被测应用进程；删除隔离 namespace 目录；保留 qa-receipt 与环境回执。
- 日志脱敏遵循 `qa.redact_patterns`；不在证据中写入凭据。
