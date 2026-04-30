# Changelog

## 2.3.0 - 2026-04-30

- 移除 npm、npx、Node 安装器与相关测试，项目回到离线 skill 包分发模型
- 新增 `agents/openai.yaml`，补齐 agent skill 推荐的界面元数据
- 新增 `references/download-workflow.md`，将下载细节从 `SKILL.md` 拆出，支持渐进式加载
- 精简 `SKILL.md`，保留触发条件、职责边界、执行原则和输出要求
- 更新 `scripts/package_skill.py`，生成 `zentao-workflow-v<version>.zip` 离线运行包
- 加强错误信息脱敏，避免在常见失败路径输出完整禅道 URL 或响应正文
- 清理旧 npm 文档、私库发布说明、构建残留与过时目录说明

## 2.2.0 - 2026-04-26

- 曾扩展 `npx` 安装器为多目标架构，支持多个 agent 目标和兼容别名
- 曾为 Claude Code、Gemini CLI 等目标生成包装层和运行时资源目录
- 曾补充私库 npm 发版说明与安装矩阵
- 以上 npm 安装路径已在 2.3.0 移除，仅保留历史记录

## 2.1.0 - 2026-04-26

- 曾新增 `npx zentao-workflow-skills` 安装器和 Node 侧测试
- 将 `SKILL.md` 中的运行命令改为相对技能根目录解析
- 以上 Node 安装器内容已在 2.3.0 移除，仅保留历史记录

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
