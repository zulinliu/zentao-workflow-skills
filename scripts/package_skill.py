#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
打包最小 agent skill 发布产物。
"""

from __future__ import annotations

import argparse
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PACKAGE_ROOT_NAME = "zentao-workflow-skills"
PACKAGE_ITEMS = [
    "SKILL.md",
    "scripts/chandao_fetch.py",
    "scripts/requirements.txt",
    "scripts/chandao_fetch",
]
SKIP_DIR_NAMES = {"__pycache__"}
SKIP_SUFFIXES = {".pyc", ".pyo"}


def build_release_file_list(project_root: Path = PROJECT_ROOT) -> list[Path]:
    """返回需要打包的项目内文件列表。"""
    files: list[Path] = []

    for item in PACKAGE_ITEMS:
        path = project_root / item
        if path.is_file():
            files.append(path)
            continue

        if path.is_dir():
            for child in sorted(path.rglob("*")):
                if not child.is_file():
                    continue
                if any(part in SKIP_DIR_NAMES for part in child.parts):
                    continue
                if child.suffix in SKIP_SUFFIXES:
                    continue
                files.append(child)
            continue

        raise FileNotFoundError(f"打包缺少必要文件或目录: {path}")

    return sorted(files)


def read_version(project_root: Path = PROJECT_ROOT) -> str:
    """读取版本号。"""
    version_file = project_root / "VERSION"
    return version_file.read_text(encoding="utf-8").strip()


def build_archive_name(version: str) -> str:
    """生成压缩包文件名。"""
    return f"{PACKAGE_ROOT_NAME}-v{version}.zip"


def package_skill(output_dir: Path, project_root: Path = PROJECT_ROOT) -> Path:
    """生成发布压缩包。"""
    output_dir.mkdir(parents=True, exist_ok=True)
    version = read_version(project_root)
    archive_path = output_dir / build_archive_name(version)
    files = build_release_file_list(project_root)

    with ZipFile(archive_path, "w", compression=ZIP_DEFLATED) as zf:
        for file_path in files:
            relative_path = file_path.relative_to(project_root)
            archive_member = Path(PACKAGE_ROOT_NAME) / relative_path
            zf.write(file_path, archive_member.as_posix())

    return archive_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="打包 zentao-workflow-skills 发布压缩包")
    parser.add_argument(
        "--output-dir",
        default=str(PROJECT_ROOT / "dist"),
        help="压缩包输出目录，默认 dist/",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    archive_path = package_skill(Path(args.output_dir).resolve())
    print(f"打包完成: {archive_path}")


if __name__ == "__main__":
    main()
