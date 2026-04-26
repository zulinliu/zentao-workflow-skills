#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
禅道数据抓取工具 - 配置管理模块

配置文件路径：~/.chandao/config.properties
下载目录：当前工作区下的 chandao/。
"""

import getpass
import os
from pathlib import Path
from typing import Callable, Optional


class ChandaoConfig:
    """禅道配置管理"""

    CONFIG_DIRNAME = ".chandao"
    CONFIG_FILENAME = "config.properties"
    OUTPUT_DIRNAME = "chandao"

    def __init__(self):
        self.base_url: Optional[str] = None
        self.username: Optional[str] = None
        self.password: Optional[str] = None
        self.output_dir: str = ""
        self.connect_timeout: int = 30000
        self.read_timeout: int = 60000
        self._config_source: Optional[str] = None

    @classmethod
    def config_path(cls) -> Path:
        """返回全局配置文件路径。"""
        return Path.home() / cls.CONFIG_DIRNAME / cls.CONFIG_FILENAME

    @classmethod
    def load(cls) -> "ChandaoConfig":
        """加载全局配置文件。"""
        config = cls()
        path = cls.config_path()
        if path.exists():
            config._load_from_file(path)
            config._config_source = str(path)
        return config

    def resolve_output_dir(self, workspace_dir: Optional[str] = None) -> str:
        """将输出目录固定到当前工作区下的 chandao/。"""
        workspace = Path(workspace_dir or os.getcwd()).resolve()
        self.output_dir = str(workspace / self.OUTPUT_DIRNAME)
        return self.output_dir

    def _load_from_file(self, path: Path):
        """从文件加载配置。"""
        try:
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue

                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip()

                    if key == "zentao.url":
                        self.base_url = self._normalize_base_url(value)
                    elif key == "zentao.username":
                        self.username = value
                    elif key == "zentao.password":
                        self.password = value

            print(f"已加载配置文件: {path}")
        except Exception as e:
            print(f"加载配置文件失败: {e}")

    def save_to_global(self):
        """保存配置到全局位置。"""
        path = self.config_path()
        self._save_to_file(path)
        print(f"配置已保存到全局: {path}")

    def _save_to_file(self, path: Path):
        """保存配置到指定文件。"""
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            f.write("# 禅道配置文件\n")
            if self.base_url:
                f.write(f"zentao.url={self.base_url}\n")
            if self.username:
                f.write(f"zentao.username={self.username}\n")
            if self.password:
                f.write(f"zentao.password={self.password}\n")

        self._config_source = str(path)

    def update_from_args(
        self,
        base_url: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ):
        """用命令行参数覆盖当前配置。"""
        if base_url:
            self.base_url = self._normalize_base_url(base_url)
        if username:
            self.username = username.strip()
        if password:
            self.password = password

    def initialize_interactively(
        self,
        input_func: Callable[[str], str] = input,
        getpass_func: Callable[[str], str] = getpass.getpass,
        force_prompt: bool = False,
    ) -> Path:
        """交互式初始化全局配置。"""
        base_url = input_func("请输入禅道地址: ").strip() if force_prompt else (self.base_url or input_func("请输入禅道地址: ")).strip()
        username = input_func("请输入禅道账号: ").strip() if force_prompt else (self.username or input_func("请输入禅道账号: ")).strip()
        password = getpass_func("请输入禅道密码: ") if force_prompt else (self.password or getpass_func("请输入禅道密码: "))

        if not base_url or not username or not password:
            raise ValueError("禅道地址、账号、密码都不能为空")

        self.base_url = self._normalize_base_url(base_url)
        self.username = username
        self.password = password
        self.save_to_global()
        return self.config_path()

    def is_initialized(self) -> bool:
        """检查配置是否已初始化。"""
        return all([self.base_url, self.username, self.password])

    def get_config_source(self) -> Optional[str]:
        """获取配置来源。"""
        return self._config_source

    def get_init_prompt(self) -> str:
        """获取初始化提示信息。"""
        if self.is_initialized():
            return ""

        return (
            "禅道配置未初始化。\n"
            "请先执行 `python scripts/chandao_fetch.py --init` 完成首次初始化，\n"
            f"或手动创建配置文件：{self.config_path()}\n"
            "配置内容示例：\n"
            "zentao.url=https://zentao.example.invalid\n"
            "zentao.username=your_username\n"
            "zentao.password=your_password\n"
            "\n"
            "下载目录固定为当前工作区下的 chandao/。"
        )

    @staticmethod
    def _normalize_base_url(value: str) -> str:
        """规范化禅道地址。"""
        return value.strip().rstrip("/")
