#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
禅道数据抓取工具 - 直接运行入口

使用方法:
    python chandao_fetch.py -t story -i 38817
    python chandao_fetch.py -t task --ids 12345,12346
    python chandao_fetch.py --init
    python chandao_fetch.py -t bug -i 67890
"""

import sys
import os

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chandao_fetch.__main__ import main

if __name__ == "__main__":
    main()
