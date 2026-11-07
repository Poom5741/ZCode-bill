# In-progress 文档复triage 报告（2026-11-11）

对 `docs/issues/` 中 11 篇仍标记 `in-progress` 的文档，逐篇对照当前 v3.17.2 代码（HEAD `a9fe401e`）做证据核验。
方法与逐票证据见 `.super-speckit/features/doc-retriage-2026-11/`（scan、matrix、playbook、receipts）。

## 结论

**11 篇的 in-progress 标记全部准确，无一属于"做完没关票"。**
2026-09 的 relay-v2 系列实现已确认进入当前代码库（此前票据写于另一工作区且"未自动 commit"，本次核验确认代码已随同步落地）。
剩余工作集中在三类：① 平台/真机验收尾巴（OSS、ARMS 控制台、真机矩阵）；② 等待产品决定的挂起项；③ 一个已确认待实施的目标票。

## 逐票判定

| 票据 | 判定 | 代码证据 / 依据 | 剩余工作与下一步 |
| --- | --- | --- | --- |
| remote-connection-ux/01 | 仍开放（标记准确） | 父票子任务表：15 票 done，07 `ready-for-human`（挂起等用户），**15 `ready-for-agent` 且未实施**（15 票头，2026-10-12/14 确认为下一轮目标，关联 #21） | 实施 [15 — 项目创建与远程连接管理分离](remote-connection-ux/15-project-device-selection-and-connection-management.md)；07 等用户排期决定 |
| remote-performance-3-16/01 | 仍开放（标记准确） | P0-1 已确认在当前代码：`packages/services/src/project/index.ts:410`（远端身份登记按物理连接代际去重，包住 `bindRemoteProjectIdentities` resolver） | P0-2、P1-2 等待文档「待确认决定」中的产品决定 |
| remote-startup-failures-3-16/01 | 仍开放（外部输入阻塞） | 分诊记录完整，诊断修复已实施（票内记录）；E 类待产品决定（04 共享 home），A/G 类证据不足待用户补日志（05） | 等产品决定 / 用户补充材料；本篇作为分诊记录保持现状 |
| ttft-stage-telemetry/01 | 仍开放（验收尾巴） | 实现与本地验证完成（2026-09-15 记录：E2E 3/3、时钟误差 3.125ms < 10ms、OTLP 证据入库）；`packages/desktop/test/e2e/helpers/ttft-otlp-fixture.ts` 存在并接入 `wdio.conf.ts` | 平台最终验收、控制台瀑布目视确认、门禁收口（票内第 31 行未勾选）；阻塞于 ARMS 控制台与跨平台实机 |
| ttft-stage-telemetry/02 | 仍开放（验收尾巴） | 实现完成（2026-09-15 API 侧核验记录）；同一 OTLP fixture 链路 | 真机取证（macOS/Windows/Linux）、ARMS 权限/容量/保留核验、门禁与使用说明（票内 31/33/34 行） |
| relay-v2/02 | 代码已完成，可关 | V2 契约与假 relay 均在：`packages/shared/src/web-remote-relay/contract.ts:20-33`（`auth_init` 无 role、`pair_status_query` 无 device_sid）、`:124`（`/api/v1/remote/ws2`）、`packages/shared/test/fixtures/fake-relay-v2.ts:238-272` | 门禁已于 2026-09-19 通过（0 error；4 个失败均为既有、与本票无关）；唯一未勾选项是门禁收口声明行，建议关票 |
| relay-v2/03 | 代码已完成，差一步人工联调 | 桌面 V2 transport 在：`packages/desktop/src/main/web-remote-relay/webRemoteControlTransport.ts:53,130,206-210`（`auth_init`/`pair_status_query`/`pair_status` 状态迁移） | 已登录 test endpoint 的真实联调（票内第 25 行手工验证） |
| relay-v2/04 | 代码已完成，E2E 待转正 | 登录门禁 E2E 在：`packages/desktop/test/e2e/manual-review/pending/web-remote-control-auth-gate.test.ts:48`（pending 目录 = 已构建通过 1/1，等人工转正） | 人工确认转正该 E2E；门禁收口（第 19/20 行） |
| relay-v2/05 | 代码已完成，真机验收 outstanding | `/remote/v4` 回调与门禁在：`packages/web/src/auth/oauthStateCodec.ts:4`、`webZaiOAuthConfig.ts:79`、`webRemoteControlEntry.ts` | OSS 测试环境真机验收：扫码首次登录 + 已登录直连两条路径（第 23 行） |
| relay-v2/06 | 代码已完成，真机验收 outstanding | 最近设备落点与设备列表在：`packages/web/src/web-remote-control/app/webRemoteControlEntry.ts:28-32,116,195,218`（含 2026-09-22 "记住的设备名"规则） | 真机验收：无码选设备、刷新恢复、账号不匹配切换（第 20 行） |
| relay-v2/07 | 大部分完成，Docker 链与真机矩阵 outstanding | V1 契约已删：shared 中仅剩 1 处残留注释 `packages/shared/src/protocol.ts:427`（nit，见下）；无 `X-Device-ID`、V1 心跳常量 | 删除三条旧 Docker 构建链（第 14 行未勾）、真机矩阵（第 17 行）、文档链接/命令一致性与 `verify:pre-push`（第 18 行） |

## 附带发现（nit）

- `packages/shared/src/protocol.ts:427` 残留一行 V1 时代的注释（"passHash 必须存 credentialService"），
  紧贴其上的 V2 注释（`:428`）已描述现行语义。属票 07 收口的清理项，不阻塞任何行为。

## 对后续排期的影响

1. **下一个可实施的已确认任务**：remote-connection-ux 票 15（`ready-for-agent`，含 #21）。
2. **等待人的事项**（不自动排期）：relay-v2 03/04/05/06/07 的人工与真机验收、ttft 平台验收、
   perf P0-2/P1-2 产品决定、startup 04 产品决定与 05 用户材料、connection-ux 07 ssh-agent 评估决定。
3. 本报告不翻转任何票据状态标记：核验证据不支持把任何一篇改为 done。
