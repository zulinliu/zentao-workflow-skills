# zentao-workflow-skills

一个面向真实研发场景的通用 agent workflow 包。

它只做一件核心事情：把禅道内容稳定下载到本地工作区，并把结果交接给后续设计、计划、实现流程。当前运行时仍保持最小化：

1. 全局初始化禅道配置到 `~/.chandao/config.properties`
2. 将 story、task、bug 固定下载到当前工作区 `./chandao/`
3. 将下载结果交给 superpowers 或当前 agent 的后续开发流程

同时，这个仓库已经补齐了跨主流 agent 的 `npx` 安装器，支持按不同客户端的官方能力安装到原生目录或兼容目录。

## 当前范围

- 下载器只保留 Python 实现
- 禅道配置只允许使用 `~/.chandao/config.properties`
- 下载目录固定为当前工作区 `./chandao/`
- 禅道访问保持只读
- 技能运行包只保留 `SKILL.md` 与 `scripts/`
- `npx` 安装器负责生成各 agent 需要的技能目录、命令文件或子代理文件

## 支持矩阵

| 目标 | 安装模式 | 用户级目录 | 项目级目录 | 当前支持级别 |
| --- | --- | --- | --- | --- |
| `codex` | 官方 Agent Skills 目录 | `~/.agents/skills/zentao-workflow/` | `.agents/skills/zentao-workflow/` | 原生支持 |
| `claude` | 官方 command + subagent + 本地运行时资源 | `~/.claude/commands/`、`~/.claude/agents/`、`~/.claude/agent-resources/zentao-workflow/` | `.claude/commands/`、`.claude/agents/`、`.claude/agent-resources/zentao-workflow/` | 原生适配 |
| `gemini` | 官方 command + subagent + 本地运行时资源 | `~/.gemini/commands/`、`~/.gemini/agents/`、`~/.gemini/agent-resources/zentao-workflow/` | `.gemini/commands/`、`.gemini/agents/`、`.gemini/agent-resources/zentao-workflow/` | 原生适配 |
| `opencode` | 原生 skill | `~/.config/opencode/skills/zentao-workflow/` | `.opencode/skills/zentao-workflow/` | 原生支持 |
| `windsurf` | 原生 skill | `~/.codeium/windsurf/skills/zentao-workflow/` | `.windsurf/skills/zentao-workflow/` | 原生支持 |
| `copilot` / `vscode` | 官方 Agent Skills 目录 | `~/.copilot/skills/zentao-workflow/` | `.github/skills/zentao-workflow/` | 原生支持 |
| `agent-skills` | 通用 Agent Skills 目录 | `~/.agents/skills/zentao-workflow/` | `.agents/skills/zentao-workflow/` | 标准支持 |
| `cursor` | 复用 Agent Skills open standard | `~/.agents/skills/zentao-workflow/` | `.agents/skills/zentao-workflow/` | 兼容模式 |
| `trae` / `trae-cn` / `tran-cn` | 复用 Agent Skills open standard | `~/.agents/skills/zentao-workflow/` | `.agents/skills/zentao-workflow/` | 兼容模式 |

说明：

- `cursor` 与 `trae` 当前统一走 Agent Skills 兼容目录，目的是降低安装分叉，保持同一套运行时可被多客户端复用。
- `claude` 与 `gemini` 没有被强行伪装成 skill；本项目为它们生成官方支持的命令和子代理包装层，并单独落一份运行时资源目录。
- `codex` 当前按 OpenAI 官方 Agent Skills 目录安装；如果要做更广泛的产品化分发，Codex 官方更推荐 plugin 形态。
- `all` 是安装器内置聚合目标，会一次安装到 `codex`、`claude`、`gemini`、`opencode`、`windsurf`、`copilot`、`agent-skills`。由于 `cursor`、`trae` 本身复用 `agent-skills`，执行 `all` 后它们也会覆盖到。

## 环境准备

### Python

先确认 Python 可用：

```bash
python --version
```

如果当前环境没有 Python：

- Windows：`winget install Python.Python.3.12`
- macOS：`brew install python`
- Ubuntu / Debian：`sudo apt update && sudo apt install -y python3 python3-pip`

再安装下载器依赖：

```bash
python -m pip install -r scripts/requirements.txt
```

如需单独检查 `requests`：

```bash
python -c "import requests; print(requests.__version__)"
```

### Node / npm / npx

如需使用 `npx` 安装器，先确认 Node.js：

```bash
node --version
npm --version
```

如果当前环境没有 Node.js：

- Windows：`winget install OpenJS.NodeJS.LTS`
- macOS：`brew install node`
- Ubuntu / Debian：`sudo apt update && sudo apt install -y nodejs npm`

### superpowers

如果后续只执行下载，superpowers 不是必需项。

如果还需要把下载结果继续交给设计、计划或开发流程，建议先确认 superpowers 已就绪，并按当前 agent 的官方安装入口完成安装。

## 快速开始

### 1. 使用 `npx` 查看支持目标

```bash
npx zentao-workflow-skills list-targets
```

### 2. 安装到目标 agent

安装到当前用户级 Codex：

```bash
npx zentao-workflow-skills install --target codex
```

安装到当前项目级 Claude Code：

```bash
npx zentao-workflow-skills install --target claude --scope project
```

安装到当前项目级 OpenCode 和 Windsurf：

```bash
npx zentao-workflow-skills install --target opencode,windsurf --scope project
```

安装到当前项目级 Cursor、Trae 兼容目录：

```bash
npx zentao-workflow-skills install --target cursor,trae --scope project
```

安装到当前项目级 GitHub Copilot / VS Code Agent：

```bash
npx zentao-workflow-skills install --target copilot --scope project
```

一次性安装全部主流目标：

```bash
npx zentao-workflow-skills install --target all --scope project
```

如目标目录已存在，增加 `--force`：

```bash
npx zentao-workflow-skills install --target all --scope project --force
```

如需先看写入计划，不真正落盘：

```bash
npx zentao-workflow-skills install --target claude,gemini --scope project --dry-run
```

### 3. 首次初始化禅道配置

```bash
python scripts/chandao_fetch.py --init
```

初始化后会在用户目录生成：

```text
~/.chandao/config.properties
```

配置中只允许保存本机私有地址、账号、密码；禁止提交真实凭据到仓库。

### 4. 下载禅道内容

```bash
python scripts/chandao_fetch.py -t story -i 39382
python scripts/chandao_fetch.py -t task -i 61563
python scripts/chandao_fetch.py -t bug -i 66445
```

### 5. 继续进入设计或开发

在当前 agent 中直接描述目标即可，例如：

```text
帮我下载禅道需求 39382，并基于下载结果继续设计和实现
```

## 下载行为

- `task` 描述为空时，会自动补充下载关联需求和父任务
- `--no-attachment` 与 `--no-image` 独立生效
- HTTP 请求超时会真实传递到 `requests`
- 附件和图片文件名会做跨平台清理，避免 Windows 非法字符问题

## 输出结构

所有下载结果固定落在当前工作区 `chandao/` 目录：

```text
{workspace}/
└── chandao/
    ├── story/
    ├── task/
    ├── bug/
    └── attachments/
```

示例：

```text
{workspace}/chandao/story/39382-需求标题.md
{workspace}/chandao/task/61563-任务标题.md
{workspace}/chandao/bug/66445-Bug标题.md
{workspace}/chandao/attachments/task/61563/
```

## 手工分发与最小运行包

### 直接复制目录

对原生支持 skill 的客户端，也可以直接复制最小运行包到对应目录。最小运行包只要求：

- `SKILL.md`
- `scripts/chandao_fetch.py`
- `scripts/requirements.txt`
- `scripts/chandao_fetch/`

### 生成 zip 运行包

```bash
python scripts/package_skill.py
```

默认会生成：

```text
dist/zentao-workflow-skills-v2.2.0.zip
```

该 zip 只适合 skill 目录式分发；像 Claude Code、Gemini CLI 这种需要命令或子代理包装层的客户端，仍建议优先使用 `npx` 安装器。

## 更新与卸载

### 更新

`npx` 安装方式的更新，直接重跑原安装命令并增加 `--force`：

```bash
npx zentao-workflow-skills install --target all --scope project --force
```

更新不会修改用户自己的 `~/.chandao/config.properties`。

### 卸载

按对应目标删除目录或包装文件即可：

- skill 模式目标：删除对应的 `zentao-workflow/` 目录
- Claude Code：删除 `.claude/commands/zentao-workflow.md`、`.claude/agents/zentao-workflow.md`、`.claude/agent-resources/zentao-workflow/`
- Gemini CLI：删除 `.gemini/commands/zentao-workflow.toml`、`.gemini/agents/zentao-workflow.md`、`.gemini/agent-resources/zentao-workflow/`

## 开发与验证

Python 测试：

```bash
python -m unittest discover -s tests -v
```

Node 安装器测试：

```bash
node --test tests-node/*.test.js
```

本地 npm 打包：

```bash
npm pack
```

本地 `npx` 烟测：

```bash
npx --yes .\zentao-workflow-skills-2.2.0.tgz install --target codex --scope project
```

私库发版前演练：

```bash
npm run publish:corp:dry-run
```

## 私库发布

公司私库地址固定为：

```text
http://npmreg.gzdevops.tsintergy.com/
```

建议发布流程：

1. 更新 [VERSION](D:/Agent/CodexProject/zentao-workflow-skills/VERSION)
2. 更新 [package.json](D:/Agent/CodexProject/zentao-workflow-skills/package.json) 的 `version`
3. 更新 [CHANGELOG.md](D:/Agent/CodexProject/zentao-workflow-skills/CHANGELOG.md)
4. 运行 Python 测试
5. 运行 Node 安装器测试
6. 执行 `npm pack`
7. 执行 `npm run publish:corp:dry-run`
8. 确认已登录公司私库
9. 执行 `npm run publish:corp`

如果当前机器尚未登录私库，可执行：

```bash
npm adduser --registry http://npmreg.gzdevops.tsintergy.com/
```

如果使用方机器的默认 npm registry 已经指向公司私库，发布成功后可直接通过：

```bash
npx zentao-workflow-skills install --target all --scope project
```

或显式指定公司私库：

```bash
npx --registry http://npmreg.gzdevops.tsintergy.com/ zentao-workflow-skills install --target all --scope project
```

## 安全约束

- 不在仓库中保存真实禅道地址、账号、密码或其他凭据
- 不创建工作区级 `.chandao` 配置
- 私库发布不提交 `.npmrc` 凭据
- 下载器保持只读，不执行禅道写操作

## 后续建议

- 继续增加真实禅道接口回归样例
- 为更多客户端补充“官方原生入口”而不是兼容入口
- 在私库发版后补一轮使用侧回归，确认各 agent 的自动发现行为一致
