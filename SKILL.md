---
name: zentao-workflow
description: |
  禅道工作流助手 v2.2.0。

  当用户提到禅道、zentao、chandao、需求、story、任务、task、Bug、缺陷、禅道链接、
  下载禅道内容、同步禅道、基于禅道内容开始设计或开发时，必须使用此技能。

  本技能聚焦三件事：
  1. 首次初始化 ~/.chandao/config.properties
  2. 用 Python 下载器把禅道内容固定下载到当前工作区 ./chandao/
  3. 将下载结果移交给 superpowers 进入 brainstorming / writing-plans / implementation
---

# 禅道工作流助手

## 目标

把禅道内容稳定下载到工作区，并将结果以适合开发的形式交给 superpowers。

## 核心原则

- 下载器通过 Python 命令行提供
- 所有脚本路径都相对当前技能根目录解析
- 禅道配置只认 `~/.chandao/config.properties`
- 下载输出固定为当前工作区 `./chandao/`
- 禅道访问保持只读
- superpowers 负责后续设计、计划、执行

## 执行步骤

### Step 1: 检查基础环境

先检查 Python 是否可用：

```bash
python --version
```

再检查下载依赖是否可用：

```bash
python -c "import requests; print(requests.__version__)"
```

如果 Python 缺失：

- Windows：`winget install Python.Python.3.12`
- macOS：`brew install python`
- Ubuntu/Debian：`sudo apt update && sudo apt install -y python3 python3-pip`

如果 `requests` 缺失：

```bash
python -m pip install -r scripts/requirements.txt
```

### Step 2: 检查 superpowers 是否可用

如果用户只想下载，可以继续执行下载流程。

如果用户还要继续设计、计划或开发：

- 检查 `superpowers` 是否已安装
- 如果未安装，先引导用户完成安装，再继续后续流程
- 按当前 agent 的插件、skills 或 extensions 管理方式进行检查
- 如环境支持命令式安装入口，则使用该 agent 的官方安装方式
- Codex、Claude Code 等环境都应按各自原生安装入口处理

### Step 3: 检查并初始化禅道配置

只使用全局配置：

```text
~/.chandao/config.properties
```

配置文件内容固定为：

```properties
zentao.url=https://zentao.example.invalid
zentao.username=your_username
zentao.password=your_password
```

如果配置不存在：

1. 一次性向用户收集禅道地址、账号、密码
2. 创建 `~/.chandao/config.properties`
3. 告知后续会复用这份配置
4. 强调示例值仅作占位，禁止把真实凭据写入仓库

不要在仓库内创建包含凭据的本地配置文件，也不要让用户配置下载目录。

### Step 4: 解析用户要下载的禅道内容

支持以下输入：

- 纯 ID：`39382`
- 类型 + ID：`需求39382`、`task 61563`、`bug 66445`
- 禅道链接：`story-view-39382`、`task-view-61563`、`bug-view-66445`

如果用户同时要求下载多个内容：

- 可以下载
- 但如果后续要进入开发，提醒用户最好逐个进入设计和实现

### Step 5: 执行下载

使用固定命令：

```bash
python scripts/chandao_fetch.py -t {type} -i {id}
```

或批量：

```bash
python scripts/chandao_fetch.py -t {type} --ids {id1},{id2}
```

关键约束：

- 不要传自定义输出目录
- 下载结果固定落在当前工作区 `./chandao/`
- `task` 描述为空时，下载器会自动补充关联需求和父任务

### Step 6: 汇总下载结果

下载完成后，至少给出：

- 主文件路径
- 附件目录路径
- 如果是空描述任务，补充说明关联需求、父任务也已下载

输出结构参考：

```text
{workspace}/chandao/story/{id}-标题.md
{workspace}/chandao/task/{id}-标题.md
{workspace}/chandao/bug/{id}-标题.md
{workspace}/chandao/attachments/{type}/{id}/
```

### Step 7: 决定是否进入 superpowers 工作流

如果用户只要下载，到这里结束。

如果用户要继续设计、计划或开发：

1. 先把已下载文件路径、标题、关联文件路径整理成上下文
2. 调用 `superpowers:brainstorming`
3. 让 superpowers 按自己的标准流程继续：
   - `brainstorming`
   - `writing-plans`
   - `subagent-driven-development` 或 `executing-plans`

不要在本技能里重复描述 superpowers 的内部工作流，也不要额外定义平行流程。

## 输出要求

每次执行后都应让用户清楚看到：

- 配置是否已初始化
- Python 与依赖是否已就绪
- 本次下载到了哪个工作区目录
- 生成了哪些主文件
- 后续是“结束下载”还是“继续进入 superpowers”

## 注意事项

- 不在仓库内保存真实禅道地址、账号、密码或其他凭据
- 不创建工作区级 `.chandao` 配置
