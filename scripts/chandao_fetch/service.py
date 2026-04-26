#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
禅道数据抓取工具 - 服务层
"""

import re
from pathlib import Path
from typing import List, Optional, Set, Tuple

from .client import ChandaoClient
from .config import ChandaoConfig
from .exporter import MarkdownExporter
from .models import Attachment, Task
from .utils import filename_from_url, has_visible_text


class ChandaoService:
    """禅道服务主类。"""

    def __init__(self, config: ChandaoConfig):
        self.config = config
        self.client = ChandaoClient(config)
        self.exporter = MarkdownExporter(config.output_dir)

    def execute(
        self,
        content_type: str,
        ids: List[int],
        download_attachments: bool = True,
        download_images: bool = True,
    ) -> List[Path]:
        """执行下载任务。"""
        if not self.client.login():
            raise Exception("登录失败")

        visited: Set[Tuple[str, int]] = set()
        exported_files: List[Path] = []
        for item_id in ids:
            file_path = self._fetch_by_id(
                content_type,
                item_id,
                download_attachments=download_attachments,
                download_images=download_images,
                visited=visited,
            )
            if file_path:
                exported_files.append(file_path)
        return exported_files

    def _fetch_by_id(
        self,
        content_type: str,
        item_id: int,
        download_attachments: bool,
        download_images: bool,
        visited: Set[Tuple[str, int]],
    ) -> Optional[Path]:
        """根据类型和 ID 获取内容。"""
        content_type = content_type.lower()
        key = (content_type, item_id)
        if key in visited:
            return None
        visited.add(key)

        if content_type == "story":
            story = self.client.get_story(item_id)
            attach_dir = Path(self.config.output_dir) / "attachments" / "story" / str(item_id)
            if download_attachments and story.attachments:
                self._download_attachments(story.attachments, attach_dir)
            if download_images:
                story.spec = self._download_content_images(story.spec, attach_dir)
                story.verify = self._download_content_images(story.verify, attach_dir)
            return self.exporter.export_story(story)

        if content_type == "task":
            task = self.client.get_task(item_id)
            attach_dir = Path(self.config.output_dir) / "attachments" / "task" / str(item_id)
            if download_attachments and task.attachments:
                self._download_attachments(task.attachments, attach_dir)
            if download_images:
                task.desc = self._download_content_images(task.desc, attach_dir)

            self._download_related_task_context(task, download_attachments, download_images, visited)
            return self.exporter.export_task(task)

        if content_type == "bug":
            bug = self.client.get_bug(item_id)
            attach_dir = Path(self.config.output_dir) / "attachments" / "bug" / str(item_id)
            if download_attachments and bug.attachments:
                self._download_attachments(bug.attachments, attach_dir)
            if download_images:
                bug.steps = self._download_content_images(bug.steps, attach_dir)
            return self.exporter.export_bug(bug)

        raise Exception(f"未知类型: {content_type}")

    def _download_related_task_context(
        self,
        task: Task,
        download_attachments: bool,
        download_images: bool,
        visited: Set[Tuple[str, int]],
    ):
        """当任务描述为空时，自动补充关联需求和父任务。"""
        if has_visible_text(task.desc):
            return

        related_targets = []
        if task.story:
            related_targets.append(("story", int(task.story), f"关联需求 {task.story}"))
        if task.parent and int(task.parent) != int(task.id):
            related_targets.append(("task", int(task.parent), f"父任务 {task.parent}"))

        if not related_targets:
            return

        print(f"任务 {task.id} 描述为空，开始补充关联上下文。")
        for related_type, related_id, label in related_targets:
            self._fetch_by_id(
                related_type,
                related_id,
                download_attachments=download_attachments,
                download_images=download_images,
                visited=visited,
            )
            print(f"已补充下载: {label}")

    def _download_attachments(self, attachments: List[Attachment], attach_dir: Path):
        """下载附件。"""
        attach_dir.mkdir(parents=True, exist_ok=True)

        for att in attachments:
            try:
                content = self.client.download_attachment(att.id)
                file_path = attach_dir / att.safe_file_name
                with open(file_path, "wb") as f:
                    f.write(content)

                att.local_path = str(file_path)
                print(f"下载附件: {att.safe_file_name} -> {file_path}")
            except Exception as e:
                print(f"下载附件失败: {att.id} - {att.title}: {e}")

    def _download_content_images(self, content: Optional[str], attach_dir: Path) -> Optional[str]:
        """下载内容中的图片，但保留原始 HTML 内容。"""
        if not content:
            return content

        attach_dir.mkdir(parents=True, exist_ok=True)
        pattern = r'<img[^>]+src="([^"]+)"[^>]*>'

        for src in re.findall(pattern, content):
            try:
                filename = filename_from_url(src, fallback="image")
                file_path = attach_dir / filename
                if file_path.exists():
                    continue

                image_content = self.client.download_image(src)
                with open(file_path, "wb") as f:
                    f.write(image_content)

                print(f"下载图片: {filename} -> {file_path}")
            except Exception as e:
                print(f"下载图片失败: {src}: {e}")

        return content
