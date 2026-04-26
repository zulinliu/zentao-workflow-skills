#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
禅道数据抓取工具 - 主入口

从禅道系统下载任务、需求、Bug 详情到当前工作区的 chandao/ 目录。
"""

import argparse
import os
import sys
from typing import List

from .config import ChandaoConfig
from .service import ChandaoService


def parse_args():
    """解析命令行参数。"""
    parser = argparse.ArgumentParser(
        description="禅道数据抓取工具 - 下载需求/任务/Bug到当前工作区的 chandao/ 目录"
    )

    parser.add_argument(
        "--url", "-u",
        help="禅道服务器地址（会写入 ~/.chandao/config.properties）"
    )
    parser.add_argument(
        "--username",
        help="登录用户名（会写入 ~/.chandao/config.properties）"
    )
    parser.add_argument(
        "--password",
        help="登录密码（会写入 ~/.chandao/config.properties）"
    )
    parser.add_argument(
        "--init",
        action="store_true",
        help="首次使用时初始化 ~/.chandao/config.properties"
    )

    parser.add_argument(
        "--type", "-t",
        choices=["story", "task", "bug"],
        help="内容类型: story(需求), task(任务), bug(缺陷)"
    )
    parser.add_argument(
        "--id", "-i",
        type=int,
        help="单个 ID"
    )
    parser.add_argument(
        "--ids",
        help="批量 ID，逗号分隔 (如: 123,456,789)"
    )

    parser.add_argument(
        "--no-attachment",
        action="store_true",
        help="不下载附件"
    )
    parser.add_argument(
        "--no-image",
        action="store_true",
        help="不下载图片"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="详细输出"
    )

    return parser.parse_args()


def collect_ids(args) -> List[int]:
    """解析并去重 ID。"""
    ids: List[int] = []
    seen = set()

    def append_id(value: int):
        if value not in seen:
            seen.add(value)
            ids.append(value)

    if args.id is not None:
        append_id(args.id)

    if args.ids:
        try:
            for raw_value in args.ids.split(","):
                raw_value = raw_value.strip()
                if raw_value:
                    append_id(int(raw_value))
        except ValueError as exc:
            raise ValueError("--ids 只能包含逗号分隔的数字") from exc

    return ids


def main():
    """主函数。"""
    args = parse_args()
    workspace_dir = os.getcwd()

    config = ChandaoConfig.load()
    config.update_from_args(args.url, args.username, args.password)
    config.resolve_output_dir(workspace_dir)

    if args.init:
        try:
            if args.url or args.username or args.password:
                if not (args.url and args.username and args.password):
                    print("错误: 使用 --init 并通过命令行写入配置时，禅道地址、账号、密码必须同时提供。")
                    sys.exit(1)
                config.save_to_global()
            else:
                config.initialize_interactively(force_prompt=True)
        except ValueError as exc:
            print(f"初始化失败: {exc}")
            sys.exit(1)

        if not args.type and args.id is None and not args.ids:
            return
    elif args.url or args.username or args.password:
        if not config.is_initialized():
            print("错误: 通过命令行写入配置时，禅道地址、账号、密码必须同时提供。")
            sys.exit(1)
        config.save_to_global()

    if not config.is_initialized():
        print(config.get_init_prompt())
        sys.exit(1)

    if not args.type:
        print("错误: 必须指定内容类型 (-t story/task/bug)")
        sys.exit(1)

    try:
        ids = collect_ids(args)
    except ValueError as exc:
        print(f"错误: {exc}")
        sys.exit(1)

    if not ids:
        print("错误: 必须指定 ID (-i 或 --ids)")
        sys.exit(1)

    try:
        service = ChandaoService(config)
        exported_files = service.execute(
            content_type=args.type,
            ids=ids,
            download_attachments=not args.no_attachment,
            download_images=not args.no_image,
        )
        print(f"输出目录: {config.output_dir}")
        for file_path in exported_files:
            print(f"已生成: {file_path}")
        print("任务执行完成")
    except Exception as e:
        print(f"执行失败: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
