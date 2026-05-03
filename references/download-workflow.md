# 禅道下载执行参考

仅在需要初始化配置、下载禅道内容或排查下载问题时读取本文件。

## 运行环境

1. 在用户工作区执行命令，保持当前工作目录不变。
2. 从技能根目录解析脚本路径：`scripts/chandao_fetch.py`。
3. 先确认 Python 可用：`python --version`。
4. 如缺少 `requests`，执行：`python -m pip install -r <技能根目录>/scripts/requirements.txt`。

## 配置规则

- 只使用用户级配置：`~/.chandao/config.properties`。
- 不创建工作区级 `.chandao` 配置。
- 不把真实禅道地址、账号、密码写入仓库、文档或提交记录。
- 示例配置只能使用占位值：

```properties
zentao.url=https://zentao.example.invalid
zentao.username=your_username
zentao.password=your_password
```

首次初始化优先运行：

```bash
python <技能根目录>/scripts/chandao_fetch.py --init
```

如需非交互初始化，`--url`、`--username`、`--password` 必须同时提供。

## 输入解析

支持以下用户输入形式：

- 纯 ID：`39382`
- 类型 + ID：`需求39382`、`story 39382`、`任务61563`、`task 61563`、`bug 66445`
- 禅道链接片段：`story-view-39382`、`task-view-61563`、`bug-view-66445`

当用户没有明确类型时，先根据上下文判断；仍无法判断时再询问。

## 下载命令

单个内容：

```bash
python <技能根目录>/scripts/chandao_fetch.py -t <story|task|bug> -i <id>
```

批量内容：

```bash
python <技能根目录>/scripts/chandao_fetch.py -t <story|task|bug> --ids <id1,id2,id3>
```

可选项：

- `--no-attachment`：不下载附件
- `--no-image`：不下载正文图片
- `--verbose`：失败时输出堆栈

禁止传入或发明自定义输出目录；下载器固定写入当前工作区 `./chandao/`。

## 输出汇总

下载完成后向用户汇总：

- 当前工作区输出目录
- 生成的主 Markdown 文件
- 附件目录位置
- 空描述任务是否已补充下载关联需求或父任务
- 后续是结束下载，还是继续进入设计、计划或实现

输出路径形态：

```text
{workspace}/chandao/story/{id}-标题.md
{workspace}/chandao/task/{id}-标题.md
{workspace}/chandao/bug/{id}-标题.md
{workspace}/chandao/attachments/{type}/{id}/
```

## 后续交接

如果用户只要求下载，到下载汇总后结束。

如果用户要求继续设计或开发，先整理已下载文件路径、标题和关联文件，再交给当前 agent 可用的设计、计划或实现流程继续处理。
