# Changelog

## 2.2.0 - 2026-04-26

- 将 `npx` 安装器扩展为多目标架构，支持 `codex`、`claude`、`gemini`、`opencode`、`windsurf`、`agent-skills`
- 新增 `cursor`、`copilot`、`vscode`、`trae`、`trae-cn`、`tran-cn` 等目标与兼容别名
- 为 Claude Code 生成官方命令与子代理包装层，并单独落地运行时资源目录
- 为 Gemini CLI 生成官方命令与子代理包装层，并单独落地运行时资源目录
- 将 Codex 安装目录校正为官方 Agent Skills 路径，并将 GitHub Copilot / VS Code Agent 调整为原生技能目录
- 增加 `all` 聚合安装目标、`--dry-run` 安装演练、私库发布脚本与私库发版说明
- 重写 README，补齐主流 agent 支持矩阵、安装模式、更新与卸载、私库发版流程

## 2.1.0 - 2026-04-26

- 新增 `npx zentao-workflow-skills` 安装器，支持安装到 Codex、Claude Code 与通用 Agent Skills 标准目录
- 新增 Node 侧安装测试与版本一致性校验
- 将 `SKILL.md` 中的运行命令改为相对技能根目录解析，去掉无效的 `{SKILL_DIR}` 占位符

## 2.0.0 - 2026-04-26

- 移除 Java 版下载器、JAR、Java 源码、Java 参考文档
- 下载器重构为 Python-only，配置只保留 `~/.chandao/config.properties`
- 下载输出固定为当前工作区 `./chandao/`
- 修复 `requests` 超时配置未真正生效的问题
- 修复 `--no-attachment` 与 `--no-image` 逻辑耦合的问题
- 补上“任务描述为空时自动下载关联需求和父任务”的真实实现
- 新增单元测试，覆盖配置、CLI、超时、子任务关联下载
- 新增本地打包脚本，并将发布包收敛为仅包含 `SKILL.md` 与 `scripts/` 的最小技能结构
- 重写 `SKILL.md`、`README.md`、`AGENTS.md`
- 删除许可证、发布、作者、GitHub Release 等非核心仓库信息

## 1.6.0 - 2026-04-02

- 提出“子任务自动补齐关联内容”的设计目标
- 下载后增加需求摘要展示思路

## 1.5.0 - 2025-03-27

- 首次接入 superpowers 技能链
- 将方案输出收敛为“技术实现方案”

## 1.0.0 - 2025-03-26

- 初始版本
- 支持下载禅道需求、任务、Bug 及附件
