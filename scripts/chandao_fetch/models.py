#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
禅道数据抓取工具 - 数据模型
"""

from dataclasses import dataclass, field
from typing import List, Optional

from .utils import sanitize_filename


@dataclass
class Attachment:
    """附件实体"""
    id: Optional[int] = None
    title: Optional[str] = None
    pathname: Optional[str] = None
    extension: Optional[str] = None
    size: Optional[int] = None
    local_path: Optional[str] = None

    @property
    def file_name(self) -> str:
        """获取文件名"""
        if self.title and self.extension:
            extension = self.extension.lstrip(".")
            if self.title.lower().endswith(f".{extension.lower()}"):
                return self.title
            return f"{self.title}.{extension}"
        if self.title:
            return self.title
        if self.pathname:
            return self.pathname.split("/")[-1]
        return "unknown"

    @property
    def safe_file_name(self) -> str:
        """获取适合写入本地文件系统的附件名。"""
        return sanitize_filename(self.file_name, fallback="unknown")

    def is_image(self) -> bool:
        """判断是否为图片"""
        image_extensions = {"jpg", "jpeg", "png", "gif", "bmp", "webp", "svg"}
        return bool(self.extension and self.extension.lower() in image_extensions)

    @classmethod
    def from_dict(cls, data: dict) -> "Attachment":
        """从字典创建实例"""
        return cls(
            id=data.get("id"),
            title=data.get("title"),
            pathname=data.get("pathname"),
            extension=data.get("extension"),
            size=data.get("size"),
        )


@dataclass
class Story:
    """需求实体"""
    id: Optional[int] = None
    title: Optional[str] = None
    spec: Optional[str] = None
    verify: Optional[str] = None
    status: Optional[str] = None
    stage: Optional[str] = None
    pri: Optional[str] = None
    source: Optional[str] = None
    category: Optional[str] = None
    product: Optional[int] = None
    module: Optional[int] = None
    plan: Optional[int] = None
    project: Optional[int] = None
    opened_by: Optional[str] = None
    opened_date: Optional[str] = None
    assigned_to: Optional[str] = None
    assigned_date: Optional[str] = None
    closed_by: Optional[str] = None
    closed_date: Optional[str] = None
    closed_reason: Optional[str] = None
    parent: Optional[int] = None
    version: Optional[str] = None
    deleted: Optional[str] = None

    # 扩展字段
    product_name: Optional[str] = None
    module_name: Optional[str] = None
    project_name: Optional[str] = None
    attachments: List[Attachment] = field(default_factory=list)
    image_urls: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> "Story":
        """从字典创建实例"""
        story = cls(
            id=data.get("id"),
            title=data.get("title"),
            spec=data.get("spec"),
            verify=data.get("verify"),
            status=data.get("status"),
            stage=data.get("stage"),
            pri=data.get("pri"),
            source=data.get("source"),
            category=data.get("category"),
            product=data.get("product"),
            module=data.get("module"),
            plan=data.get("plan"),
            project=data.get("project"),
            opened_by=data.get("openedBy"),
            opened_date=data.get("openedDate"),
            assigned_to=data.get("assignedTo"),
            assigned_date=data.get("assignedDate"),
            closed_by=data.get("closedBy"),
            closed_date=data.get("closedDate"),
            closed_reason=data.get("closedReason"),
            parent=data.get("parent"),
            version=data.get("version"),
            deleted=data.get("deleted"),
        )

        # 解析附件
        if "files" in data and isinstance(data["files"], dict):
            story.attachments = [
                Attachment.from_dict(f) for f in data["files"].values()
            ]

        return story


@dataclass
class Task:
    """任务实体"""
    id: Optional[int] = None
    name: Optional[str] = None
    desc: Optional[str] = None
    status: Optional[str] = None
    type: Optional[str] = None
    pri: Optional[str] = None
    project: Optional[int] = None
    module: Optional[int] = None
    story: Optional[int] = None
    story_version: Optional[int] = None
    parent: Optional[int] = None
    opened_by: Optional[str] = None
    opened_date: Optional[str] = None
    assigned_to: Optional[str] = None
    assigned_date: Optional[str] = None
    finished_by: Optional[str] = None
    finished_date: Optional[str] = None
    closed_by: Optional[str] = None
    closed_date: Optional[str] = None
    closed_reason: Optional[str] = None
    estimate: Optional[float] = None
    consumed: Optional[float] = None
    left: Optional[float] = None
    deadline: Optional[str] = None
    deleted: Optional[str] = None

    # 扩展字段
    project_name: Optional[str] = None
    module_name: Optional[str] = None
    story_title: Optional[str] = None
    attachments: List[Attachment] = field(default_factory=list)
    image_urls: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """从字典创建实例"""
        task = cls(
            id=data.get("id"),
            name=data.get("name"),
            desc=data.get("desc"),
            status=data.get("status"),
            type=data.get("type"),
            pri=data.get("pri"),
            project=data.get("project"),
            module=data.get("module"),
            story=data.get("story"),
            story_version=data.get("storyVersion"),
            parent=data.get("parent"),
            opened_by=data.get("openedBy"),
            opened_date=data.get("openedDate"),
            assigned_to=data.get("assignedTo"),
            assigned_date=data.get("assignedDate"),
            finished_by=data.get("finishedBy"),
            finished_date=data.get("finishedDate"),
            closed_by=data.get("closedBy"),
            closed_date=data.get("closedDate"),
            closed_reason=data.get("closedReason"),
            estimate=data.get("estimate"),
            consumed=data.get("consumed"),
            left=data.get("left"),
            deadline=data.get("deadline"),
            deleted=data.get("deleted"),
        )

        # 解析附件
        if "files" in data and isinstance(data["files"], dict):
            task.attachments = [
                Attachment.from_dict(f) for f in data["files"].values()
            ]

        return task


@dataclass
class Bug:
    """Bug实体"""
    id: Optional[int] = None
    title: Optional[str] = None
    steps: Optional[str] = None
    status: Optional[str] = None
    severity: Optional[str] = None
    pri: Optional[str] = None
    type: Optional[str] = None
    product: Optional[int] = None
    module: Optional[int] = None
    project: Optional[int] = None
    story: Optional[int] = None
    opened_by: Optional[str] = None
    opened_date: Optional[str] = None
    assigned_to: Optional[str] = None
    assigned_date: Optional[str] = None
    resolved_by: Optional[str] = None
    resolved_date: Optional[str] = None
    resolution: Optional[str] = None
    closed_by: Optional[str] = None
    closed_date: Optional[str] = None
    deleted: Optional[str] = None

    # 扩展字段
    product_name: Optional[str] = None
    module_name: Optional[str] = None
    project_name: Optional[str] = None
    story_title: Optional[str] = None
    attachments: List[Attachment] = field(default_factory=list)
    image_urls: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> "Bug":
        """从字典创建实例"""
        bug = cls(
            id=data.get("id"),
            title=data.get("title"),
            steps=data.get("steps"),
            status=data.get("status"),
            severity=data.get("severity"),
            pri=data.get("pri"),
            type=data.get("type"),
            product=data.get("product"),
            module=data.get("module"),
            project=data.get("project"),
            story=data.get("story"),
            opened_by=data.get("openedBy"),
            opened_date=data.get("openedDate"),
            assigned_to=data.get("assignedTo"),
            assigned_date=data.get("assignedDate"),
            resolved_by=data.get("resolvedBy"),
            resolved_date=data.get("resolvedDate"),
            resolution=data.get("resolution"),
            closed_by=data.get("closedBy"),
            closed_date=data.get("closedDate"),
            deleted=data.get("deleted"),
        )

        # 解析附件
        if "files" in data and isinstance(data["files"], dict):
            bug.attachments = [
                Attachment.from_dict(f) for f in data["files"].values()
            ]

        return bug
