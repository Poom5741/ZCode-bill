# Spec — RDUX15 项目创建与远程连接管理分离

Authority: docs/issues/remote-connection-ux/15-project-device-selection-and-connection-management.md
(confirmed Q1–Q12, 52 user stories, 25 acceptance scenarios RDUX15-01..25) + #21 chat contract
(RDUX21-01..24). This file is the native Spec Kit spec surface; the ticket remains the requirement
source of record. Feature matrix: ./matrix.md (REQ-01..REQ-20 map 1:1 to ticket anchors).

## Problem
Project creation currently forces a local/remote pre-screen and a separate connection wizard;
device selection, project creation, and connection management are entangled across sidebar, chat
menu, and settings; drafts do not survive device round trips.

## Solution (confirmed)
- 「项目 +」opens a direct-create form: 项目名称、设备、源文件夹 in one surface. No pre-screen.
- Device default = current task's device, else 此电脑; offline devices stay selected with status.
- Device dropdown lists only added devices (+添加远程设备…); discovery candidates stay in settings.
- All add-connection entries open Settings→Remote devices categorized add window (SSH default,
  WSL/Docker per platform capability), primary action 「添加并连接」; settings-sourced completion
  ends in device management.
- Existing-device selection never connects; online→添加文件夹, offline→连接并选择文件夹 inside the
  project flow. Existing-project secondary entry preserves original project identity; draft survives
  the round trip. Chat source always resolves a remote folder per #21 before send.
- Completion intent dispatches by origin; background continue never hijacks navigation; cancel keeps
  saved records and shared connections; late results are inert; close-after-success never disconnects.

## Requirements
REQ-01..REQ-20 — see ./matrix.md (1:1 with ticket anchors Q1–Q12 and RDUX15-01..25).

## Out of scope
Transport/auth/install/reconnect state machines; save-only mode; remote multi-root; cross-restart
draft persistence; mobile remote-management expansion; ssh-agent; task protocol/workspace identity
changes (ticket Out of Scope, binding).

## Acceptance
RDUX15-01..25 with declared evidence types; environment-blocked scenarios record honest
not-verified rationale (harness documents WSL2/Docker available locally; SSH host pending).
