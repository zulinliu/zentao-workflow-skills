#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
禅道数据抓取工具 - API 客户端模块
"""

import json
from typing import List
from urllib.parse import urljoin

import requests

from .config import ChandaoConfig
from .models import Attachment, Bug, Story, Task


class ChandaoClient:
    """
    禅道 API 客户端

    只允许查询操作，禁止新增、修改、删除。
    """

    def __init__(self, config: ChandaoConfig):
        self.config = config
        self.session = requests.Session()
        self.logged_in = False
        self.timeout = (
            config.connect_timeout / 1000,
            config.read_timeout / 1000,
        )

        self.session.headers.update({
            "User-Agent": "zentao-workflow-python/2.0",
            "Accept": "application/json",
        })

    def login(self) -> bool:
        """登录禅道。"""
        if self.logged_in:
            return True

        url = urljoin(self.config.base_url, "/user-login.json")
        response = self._request(
            "post",
            url,
            data={
                "account": self.config.username,
                "password": self.config.password,
                "keepLogin": "1",
            },
        )
        if not response.ok:
            raise Exception(f"登录失败: HTTP {response.status_code}")

        result = self._read_json(response)
        if result.get("result") == "success" or result.get("status") == "success":
            self.logged_in = True
            print("登录成功")
            return True

        message = result.get("message", "未知错误")
        raise Exception(f"登录失败: {message}")

    def _ensure_logged_in(self):
        """确保已登录。"""
        if not self.logged_in:
            self.login()

    def _fetch_json(self, url: str) -> dict:
        """获取并解析 JSON 数据。"""
        self._ensure_logged_in()
        response = self._request("get", url)
        if not response.ok:
            raise Exception(f"请求失败: {url} HTTP {response.status_code}")

        body = self._read_json(response)
        data = body.get("data", body)
        if isinstance(data, str):
            data = json.loads(data)
        return data

    def _parse_attachments(self, files_data: dict) -> List[Attachment]:
        """解析附件列表。"""
        attachments = []
        if files_data and isinstance(files_data, dict):
            for file_data in files_data.values():
                try:
                    attachments.append(Attachment.from_dict(file_data))
                except Exception as e:
                    print(f"解析附件失败: {e}")
        return attachments

    def get_story(self, story_id: int) -> Story:
        """获取需求详情。"""
        url = urljoin(self.config.base_url, f"/story-view-{story_id}.json")
        data = self._fetch_json(url)
        story_node = data.get("story", data)

        story = Story(
            id=story_node.get("id"),
            title=story_node.get("title"),
            spec=story_node.get("spec"),
            verify=story_node.get("verify"),
            status=story_node.get("status"),
            stage=story_node.get("stage"),
            pri=story_node.get("pri"),
            source=story_node.get("source"),
            category=story_node.get("category"),
            product=story_node.get("product"),
            module=story_node.get("module"),
            plan=story_node.get("plan"),
            project=story_node.get("project"),
            opened_by=story_node.get("openedBy"),
            opened_date=story_node.get("openedDate"),
            assigned_to=story_node.get("assignedTo"),
            assigned_date=story_node.get("assignedDate"),
            closed_by=story_node.get("closedBy"),
            closed_date=story_node.get("closedDate"),
            closed_reason=story_node.get("closedReason"),
            parent=story_node.get("parent"),
            version=story_node.get("version"),
            deleted=story_node.get("deleted"),
        )

        if "files" in story_node:
            story.attachments = self._parse_attachments(story_node["files"])

        if "product" in data and isinstance(data["product"], dict):
            story.product_name = data["product"].get("name")

        if "storyModule" in data and isinstance(data["storyModule"], dict):
            story.module_name = data["storyModule"].get("name")

        print(f"获取需求: {story_id} - {story.title}")
        return story

    def get_task(self, task_id: int) -> Task:
        """获取任务详情。"""
        url = urljoin(self.config.base_url, f"/task-view-{task_id}.json")
        data = self._fetch_json(url)
        task_node = data.get("task", data)

        task = Task(
            id=task_node.get("id"),
            name=task_node.get("name"),
            desc=task_node.get("desc"),
            status=task_node.get("status"),
            type=task_node.get("type"),
            pri=task_node.get("pri"),
            project=task_node.get("project"),
            module=task_node.get("module"),
            story=task_node.get("story"),
            story_version=task_node.get("storyVersion"),
            parent=task_node.get("parent"),
            opened_by=task_node.get("openedBy"),
            opened_date=task_node.get("openedDate"),
            assigned_to=task_node.get("assignedTo"),
            assigned_date=task_node.get("assignedDate"),
            finished_by=task_node.get("finishedBy"),
            finished_date=task_node.get("finishedDate"),
            closed_by=task_node.get("closedBy"),
            closed_date=task_node.get("closedDate"),
            closed_reason=task_node.get("closedReason"),
            estimate=task_node.get("estimate"),
            consumed=task_node.get("consumed"),
            left=task_node.get("left"),
            deadline=task_node.get("deadline"),
            deleted=task_node.get("deleted"),
        )

        if "files" in task_node:
            task.attachments = self._parse_attachments(task_node["files"])

        print(f"获取任务: {task_id} - {task.name}")
        return task

    def get_bug(self, bug_id: int) -> Bug:
        """获取 Bug 详情。"""
        url = urljoin(self.config.base_url, f"/bug-view-{bug_id}.json")
        data = self._fetch_json(url)
        bug_node = data.get("bug", data)

        bug = Bug(
            id=bug_node.get("id"),
            title=bug_node.get("title"),
            steps=bug_node.get("steps"),
            status=bug_node.get("status"),
            severity=bug_node.get("severity"),
            pri=bug_node.get("pri"),
            type=bug_node.get("type"),
            product=bug_node.get("product"),
            module=bug_node.get("module"),
            project=bug_node.get("project"),
            story=bug_node.get("story"),
            opened_by=bug_node.get("openedBy"),
            opened_date=bug_node.get("openedDate"),
            assigned_to=bug_node.get("assignedTo"),
            assigned_date=bug_node.get("assignedDate"),
            resolved_by=bug_node.get("resolvedBy"),
            resolved_date=bug_node.get("resolvedDate"),
            resolution=bug_node.get("resolution"),
            closed_by=bug_node.get("closedBy"),
            closed_date=bug_node.get("closedDate"),
            deleted=bug_node.get("deleted"),
        )

        if "files" in bug_node:
            bug.attachments = self._parse_attachments(bug_node["files"])

        print(f"获取Bug: {bug_id} - {bug.title}")
        return bug

    def download_attachment(self, attachment_id: int) -> bytes:
        """下载附件。"""
        self._ensure_logged_in()
        url = urljoin(self.config.base_url, f"/file-download-{attachment_id}.json")
        response = self._request("get", url)
        if not response.ok:
            raise Exception(f"下载附件失败: HTTP {response.status_code}")
        return response.content

    def download_image(self, image_path: str) -> bytes:
        """下载图片。"""
        self._ensure_logged_in()
        url = image_path if image_path.startswith("http") else urljoin(self.config.base_url, image_path)
        response = self._request("get", url)
        if not response.ok:
            raise Exception(f"下载图片失败: HTTP {response.status_code}")
        return response.content

    def _request(self, method: str, url: str, **kwargs) -> requests.Response:
        """统一发起请求，确保超时配置真正生效。"""
        return self.session.request(method, url, timeout=self.timeout, **kwargs)

    @staticmethod
    def _read_json(response: requests.Response) -> dict:
        """读取 JSON 响应，并在失败时返回可诊断错误。"""
        try:
            return response.json()
        except ValueError as exc:
            preview = response.text[:200].replace("\n", " ").strip()
            raise Exception(f"禅道返回了非 JSON 响应: {preview}") from exc
