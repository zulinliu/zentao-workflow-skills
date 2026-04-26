# AGENTS.md

## 项目定位

这是一个通用 agent skill 项目，目标是把“下载禅道内容 -> 进入 superpowers 工作流”压缩成一个核心精简、稳定可复用的入口，并适配 Codex、Claude Code 等具备技能或插件能力的智能体环境。

## 当前边界

- 下载入口为 `scripts/chandao_fetch.py` 与 `scripts/chandao_fetch/`
- `npx` 安装入口负责把运行时安装到目标 agent 的原生技能目录、命令目录或兼容目录
- 禅道配置只存 `~/.chandao/config.properties`
- 下载输出固定为当前工作区 `./chandao/`
- 禅道接口只允许只读操作
- 核心文档为 `README.md`、`CHANGELOG.md`、`SKILL.md`

## 开发命令

```bash
python -m pip install -r scripts/requirements.txt
python -m unittest discover -s tests -v
node --test tests-node/*.test.js
python -m scripts.chandao_fetch --help
python scripts/package_skill.py
npm pack
npm run publish:corp:dry-run
```

## 目录结构

```text
scripts/
├── chandao_fetch.py          # 直接运行入口
├── package_skill.py          # Skill 运行包打包
├── requirements.txt
└── chandao_fetch/
    ├── __main__.py           # CLI 入口
    ├── config.py             # 全局配置管理
    ├── client.py             # 禅道只读客户端
    ├── exporter.py           # Markdown 导出
    ├── models.py             # 数据模型
    ├── service.py            # 下载主流程
    └── utils.py              # 文件名/内容辅助函数

bin/
└── zentao-workflow-skills.js # npx 入口

lib/
├── cli.js                    # npm CLI 参数解析
└── installer.js              # 多 agent 安装逻辑与适配层生成

tests/
├── test_cli.py
├── test_client.py
├── test_config.py
└── test_service.py

tests-node/
└── installer.test.js         # Node 安装器测试
```

## 修改约束

- 不要扩展工作区级配置或自定义输出目录
- 环境检测与安装说明要和当前支持的平台、工具保持一致
- 不要在 Skill 内复制 superpowers 的完整计划和执行流程
- 不要在仓库内写入真实禅道地址、账号、密码或其他凭据
- `package.json` 版本号必须与 `VERSION` 保持一致
- 私库发布地址固定为 `http://npmreg.gzdevops.tsintergy.com/`
- 如果调整下载结果格式，必须同步更新 `README.md`、`CHANGELOG.md`、`SKILL.md`
- 所有文档和注释默认使用中文
