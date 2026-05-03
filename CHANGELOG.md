# Changelog

## 2.4.0 - 2026-05-03

- 新增 GitHub Actions 自动发版工作流，推送 `v*` 标签即可触发自动测试、打包和发布
- 发版流程自动运行单元测试和 CLI 验证，确保发布质量
- 发布产物自动上传为 GitHub Release 附件（离线 zip 包）

## 2.3.0 - 2026-04-30

- 收敛为离线 skill 包分发模型，运行包只包含技能执行所需文件
- 新增 `agents/openai.yaml`，补齐 agent skill 推荐的界面元数据
- 新增 `references/download-workflow.md`，将下载细节从 `SKILL.md` 拆出，支持渐进式加载
- 明确支持所有具备 skills 或等价技能目录机制的 agent，包括 Claude Code、Codex、Cursor、Trae、OpenCode 等
- 精简 `SKILL.md`，保留触发条件、职责边界、执行原则和输出要求
- 更新 `scripts/package_skill.py`，生成 `zentao-workflow-v<version>.zip` 离线运行包
- 加强错误信息脱敏，避免在常见失败路径输出完整禅道 URL 或响应正文
- 清理构建残留、过时目录说明和不应纳入版本管理的内容

## 2.0.0 - 2026-04-26

- 移除 Java 版下载器、JAR、Java 源码、Java 参考文档
- 下载器重构为 Python-only，配置只保留 `~/.chandao/config.properties`
- 下载输出固定为当前工作区 `./chandao/`
- 修复 `requests` 超时配置未真正生效的问题
- 修复 `--no-attachment` 与 `--no-image` 逻辑耦合的问题
- 实现任务描述为空时自动下载关联需求和父任务
- 新增单元测试，覆盖配置、CLI、超时、子任务关联下载
- 新增本地打包脚本，并将发布包收敛为最小技能结构
- 重写 `SKILL.md`、`README.md`、`AGENTS.md`

## 1.6.0 - 2026-04-02

- 提出“子任务自动补齐关联内容”的设计目标
- 下载后增加需求摘要展示思路

## 1.5.0 - 2025-03-27

- 首次接入后续开发技能链
- 将方案输出收敛为“技术实现方案”

## 1.0.0 - 2025-03-26

- 初始版本
- 支持下载禅道需求、任务、Bug 及附件
