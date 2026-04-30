# zentao-workflow-skills

一个最小化的禅道 agent skill 项目，用于把禅道 story、task、bug 只读下载到本地工作区，并把结果交给后续设计、计划或实现流程。

## 当前范围

- 下载器只保留 Python 实现
- 禅道配置只使用 `~/.chandao/config.properties`
- 下载结果固定写入当前工作区 `./chandao/`
- 发布物只提供离线 skill 压缩包，不再提供 npm、npx 或 Node 安装器
- 运行包只包含 `SKILL.md`、`agents/openai.yaml`、`references/` 和 `scripts/`

## 运行结构

```text
zentao-workflow/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   └── download-workflow.md
└── scripts/
    ├── chandao_fetch.py
    ├── requirements.txt
    └── chandao_fetch/
```

## 环境准备

先确认 Python 可用：

```bash
python --version
```

如需安装 Python：

- Windows：`winget install Python.Python.3.12`
- macOS：`brew install python`
- Ubuntu / Debian：`sudo apt update && sudo apt install -y python3 python3-pip`

安装下载器依赖：

```bash
python -m pip install -r scripts/requirements.txt
```

如需单独检查依赖：

```bash
python -c "import requests; print(requests.__version__)"
```

## 离线安装

### 1. 获取发布包

从内部发布渠道下载 `zentao-workflow-v<version>.zip`，解压后应得到一个 `zentao-workflow/` 目录。

### 2. 复制到目标技能目录

将完整的 `zentao-workflow/` 目录复制到目标 agent 支持的技能目录。不同客户端的技能目录由客户端自身约定，本项目不再维护自动探测或自动安装逻辑。

通用目录形态：

```text
<agent-skills-root>/zentao-workflow/
```

安装后如当前会话未立即识别新技能，重启对应 agent 或重新加载技能列表。

### 3. 校验安装内容

确认目标目录至少包含：

```text
zentao-workflow/SKILL.md
zentao-workflow/agents/openai.yaml
zentao-workflow/references/download-workflow.md
zentao-workflow/scripts/chandao_fetch.py
zentao-workflow/scripts/requirements.txt
zentao-workflow/scripts/chandao_fetch/__main__.py
```

## 首次配置

在用户工作区执行：

```bash
python <技能目录>/scripts/chandao_fetch.py --init
```

初始化会写入用户级配置：

```text
~/.chandao/config.properties
```

配置内容示例只能使用占位值：

```properties
zentao.url=https://zentao.example.invalid
zentao.username=your_username
zentao.password=your_password
```

禁止把真实禅道地址、账号、密码或 `.npmrc`、证书、密钥等凭据提交到仓库。

## 下载使用

单个内容：

```bash
python <技能目录>/scripts/chandao_fetch.py -t story -i 39382
python <技能目录>/scripts/chandao_fetch.py -t task -i 61563
python <技能目录>/scripts/chandao_fetch.py -t bug -i 66445
```

批量同类型内容：

```bash
python <技能目录>/scripts/chandao_fetch.py -t story --ids 39382,39383
```

可选控制项：

- `--no-attachment`：不下载附件
- `--no-image`：不下载正文图片
- `--verbose`：失败时输出堆栈，便于本地排查

## 下载行为

- `task` 描述为空时，会自动补充下载关联需求和父任务
- `--no-attachment` 与 `--no-image` 独立生效
- HTTP 请求超时会传递到 `requests`
- 附件和图片文件名会做跨平台清理，避免 Windows 非法字符问题
- 错误信息会避免输出完整禅道 URL 或响应正文，降低泄露内部信息的风险

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

## 打包发版

生成离线 skill 运行包：

```bash
python scripts/package_skill.py
```

默认输出：

```text
dist/zentao-workflow-v2.3.0.zip
```

发布前检查：

1. 更新 `VERSION`
2. 更新 `CHANGELOG.md`
3. 运行 Python 单元测试
4. 运行 CLI 帮助命令
5. 生成离线 zip 包
6. 检查 zip 只包含运行所需文件
7. 通过内部文件发布、制品库或人工离线方式分发 zip

## 开发验证

安装依赖：

```bash
python -m pip install -r scripts/requirements.txt
```

运行测试：

```bash
python -m unittest discover -s tests -v
```

检查 CLI：

```bash
python -m scripts.chandao_fetch --help
```

生成发布包：

```bash
python scripts/package_skill.py
```

## 安全约束

- 不在仓库中保存真实禅道地址、账号、密码或其它凭据
- 不创建工作区级 `.chandao` 配置
- 不提交下载结果 `chandao/`、构建产物 `dist/` 或压缩包
- 不提交 `.npmrc`、证书、私钥、Token 等敏感文件
- 下载器保持只读，不执行禅道写操作

## 维护原则

- 修改下载结果格式时，同步更新 `README.md`、`SKILL.md`、`references/download-workflow.md` 和 `CHANGELOG.md`
- 修改运行包内容时，同步更新 `scripts/package_skill.py` 与 `tests/test_package_skill.py`
- 不重新引入 npm、npx、Node 安装器或客户端自动安装矩阵
