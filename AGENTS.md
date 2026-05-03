# AGENTS.md

## 语言偏好

- 面向用户阅读和审查的文档、注释、提交说明、Agent 交互内容优先使用中文
- 命令、路径、配置键名和代码标识保持原文

## 终端设定

- Windows 环境默认使用 PowerShell 7：`C:\Program Files\PowerShell\7\pwsh.exe`

## 项目定位

这是一个通用 agent skill 项目，目标是把“下载禅道内容 -> 整理为后续开发上下文”压缩成一个核心精简、稳定可复用的离线技能包。该技能面向所有支持 skills 或等价技能目录机制的 agent，包括但不限于 Claude Code、Codex、Cursor、Trae、OpenCode。

## 当前边界

- 下载入口为 `scripts/chandao_fetch.py` 与 `scripts/chandao_fetch/`
- 只发布离线 skill 压缩包，不维护平台专属自动安装矩阵
- 禅道配置只存 `~/.chandao/config.properties`
- 下载输出固定为当前工作区 `./chandao/`
- 禅道接口只允许只读操作
- 运行包内容由 `scripts/package_skill.py` 和 `tests/test_package_skill.py` 共同约束
- 核心文档为 `README.md`、`CHANGELOG.md`、`SKILL.md`、`references/download-workflow.md`
- `agents/openai.yaml` 仅是可选界面元数据，不代表技能绑定单一 agent

## 开发命令

```bash
python -m pip install -r scripts/requirements.txt
python -m unittest discover -s tests -v
python -m scripts.chandao_fetch --help
python scripts/package_skill.py
```

## 目录结构

```text
agents/
└── openai.yaml               # Skill UI 元数据

references/
└── download-workflow.md      # 下载执行细节，按需渐进加载

scripts/
├── chandao_fetch.py          # 直接运行入口
├── package_skill.py          # 离线 Skill 运行包打包
├── requirements.txt
└── chandao_fetch/
    ├── __main__.py           # CLI 入口
    ├── config.py             # 全局配置管理
    ├── client.py             # 禅道只读客户端
    ├── exporter.py           # Markdown 导出
    ├── models.py             # 数据模型
    ├── service.py            # 下载主流程
    └── utils.py              # 文件名/内容辅助函数

tests/
├── test_cli.py
├── test_client.py
├── test_config.py
├── test_package_skill.py
└── test_service.py
```

## 修改约束

- 不要扩展工作区级配置或自定义输出目录
- 不要引入平台专属自动安装矩阵或绑定单一 agent 的安装逻辑
- 不要在 Skill 内复制后续开发工作流的完整计划和执行流程
- 不要在仓库内写入真实禅道地址、账号、密码、Token、证书或其它凭据
- 如果调整下载结果格式，必须同步更新 `README.md`、`CHANGELOG.md`、`SKILL.md`、`references/download-workflow.md`
- 如果调整运行包内容，必须同步更新 `scripts/package_skill.py`、`tests/test_package_skill.py`、`README.md`
- 所有文档和注释默认使用中文
