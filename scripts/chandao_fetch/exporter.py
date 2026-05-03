#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
禅道数据抓取工具 - Markdown 导出模块
"""

import re
from html import unescape
from pathlib import Path
from typing import List, Optional

from .models import Attachment, Bug, Story, Task
from .utils import filename_from_url, has_visible_text, sanitize_filename


class MarkdownExporter:
    """Markdown 导出服务。"""

    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)

    def export_story(self, story: Story) -> Path:
        """导出需求。"""
        safe_title = sanitize_filename(story.title, fallback="unnamed")
        filename = f"{story.id}-{safe_title}"
        attach_path = f"../attachments/story/{story.id}"

        md = [
            f"# 【{story.title}】{story.id}",
            "",
            "> 类型: 需求",
            "",
            "## 基本信息",
            "",
            "| 字段 | 值 |",
            "|------|----|",
            f"| 状态 | {self._safe(story.status)} |",
            f"| 阶段 | {self._safe(story.stage)} |",
            f"| 优先级 | {self._safe(story.pri)} |",
            f"| 来源 | {self._safe(story.source)} |",
            f"| 分类 | {self._safe(story.category)} |",
        ]

        if story.product_name:
            md.append(f"| 产品 | {story.product_name} |")
        if story.project_name:
            md.append(f"| 项目 | {story.project_name} |")
        md.extend([
            f"| 创建人 | {self._safe(story.opened_by)} |",
            f"| 创建时间 | {self._safe(story.opened_date)} |",
            f"| 指派给 | {self._safe(story.assigned_to)} |",
            "",
        ])

        if has_visible_text(story.spec):
            md.extend(["## 需求描述", "", self._process_content(story.spec, attach_path), ""])
        if has_visible_text(story.verify):
            md.extend(["## 验收标准", "", self._process_content(story.verify, attach_path), ""])

        self._append_attachments(md, story.attachments, attach_path)

        file_path = self.output_dir / "story" / f"{filename}.md"
        self._write_file(file_path, "\n".join(md))
        print(f"导出需求: {file_path}")
        return file_path

    def export_task(self, task: Task) -> Path:
        """导出任务。"""
        safe_name = sanitize_filename(task.name, fallback="unnamed")
        filename = f"{task.id}-{safe_name}"
        attach_path = f"../attachments/task/{task.id}"

        md = [
            f"# 【{task.name}】{task.id}",
            "",
            "> 类型: 任务",
            "",
            "## 基本信息",
            "",
            "| 字段 | 值 |",
            "|------|----|",
            f"| 状态 | {self._safe(task.status)} |",
            f"| 类型 | {self._safe(task.type)} |",
            f"| 优先级 | {self._safe(task.pri)} |",
        ]

        if task.project_name:
            md.append(f"| 项目 | {task.project_name} |")
        if task.story_title:
            md.append(f"| 相关需求 | {task.story_title} |")
        elif task.story:
            md.append(f"| 相关需求 ID | {task.story} |")
        if task.parent:
            md.append(f"| 父任务 ID | {task.parent} |")

        md.extend([
            f"| 创建人 | {self._safe(task.opened_by)} |",
            f"| 创建时间 | {self._safe(task.opened_date)} |",
            f"| 指派给 | {self._safe(task.assigned_to)} |",
        ])

        if task.deadline:
            md.append(f"| 截止日期 | {task.deadline} |")
        if task.estimate:
            md.append(f"| 预计工时 | {task.estimate}h |")
        if task.consumed:
            md.append(f"| 已消耗 | {task.consumed}h |")
        md.append("")

        if has_visible_text(task.desc):
            md.extend(["## 任务描述", "", self._process_content(task.desc, attach_path), ""])
        elif task.story or task.parent:
            md.extend(["## 上下文提示", "", "该任务原始描述为空，建议结合关联需求或父任务一起阅读。", ""])

        self._append_attachments(md, task.attachments, attach_path)

        file_path = self.output_dir / "task" / f"{filename}.md"
        self._write_file(file_path, "\n".join(md))
        print(f"导出任务: {file_path}")
        return file_path

    def export_bug(self, bug: Bug) -> Path:
        """导出 Bug。"""
        safe_title = sanitize_filename(bug.title, fallback="unnamed")
        filename = f"{bug.id}-{safe_title}"
        attach_path = f"../attachments/bug/{bug.id}"

        md = [
            f"# 【{bug.title}】{bug.id}",
            "",
            "> 类型: Bug",
            "",
            "## 基本信息",
            "",
            "| 字段 | 值 |",
            "|------|----|",
            f"| 状态 | {self._safe(bug.status)} |",
            f"| 严重程度 | {self._safe(bug.severity)} |",
            f"| 优先级 | {self._safe(bug.pri)} |",
            f"| 类型 | {self._safe(bug.type)} |",
        ]

        if bug.product_name:
            md.append(f"| 产品 | {bug.product_name} |")
        if bug.project_name:
            md.append(f"| 项目 | {bug.project_name} |")
        md.extend([
            f"| 创建人 | {self._safe(bug.opened_by)} |",
            f"| 创建时间 | {self._safe(bug.opened_date)} |",
            f"| 指派给 | {self._safe(bug.assigned_to)} |",
        ])
        if bug.resolved_by:
            md.extend([
                f"| 解决人 | {bug.resolved_by} |",
                f"| 解决时间 | {self._safe(bug.resolved_date)} |",
                f"| 解决方案 | {self._safe(bug.resolution)} |",
            ])
        md.append("")

        if has_visible_text(bug.steps):
            md.extend(["## 重现步骤", "", self._process_content(bug.steps, attach_path), ""])

        self._append_attachments(md, bug.attachments, attach_path)

        file_path = self.output_dir / "bug" / f"{filename}.md"
        self._write_file(file_path, "\n".join(md))
        print(f"导出Bug: {file_path}")
        return file_path

    def _process_content(self, content: str, attach_path: str) -> str:
        """处理内容：将 HTML 转换为 Markdown。"""
        if not content:
            return ""

        result = self._convert_img_tags(content, attach_path)
        result = self._html_to_markdown(result)
        return re.sub(r"\n{3,}", "\n\n", result).strip()

    def _convert_img_tags(self, content: str, attach_path: str) -> str:
        """转换图片标签为 Markdown 格式。"""
        if not content:
            return ""

        pattern = r'<img[^>]+src="([^"]+)"[^>]*>'

        def replace_img(match):
            src = match.group(1)
            filename = filename_from_url(src, fallback="image")
            return f"\n\n![]({attach_path}/{filename})\n\n"

        return re.sub(pattern, replace_img, content)

    def _html_to_markdown(self, html: str) -> str:
        """将 HTML 转换为 Markdown。"""
        if not html:
            return ""

        result = html
        result = re.sub(r"<h1[^>]*>\s*", "\n\n# ", result, flags=re.IGNORECASE)
        result = re.sub(r"<h2[^>]*>\s*", "\n\n## ", result, flags=re.IGNORECASE)
        result = re.sub(r"<h3[^>]*>\s*", "\n\n### ", result, flags=re.IGNORECASE)
        result = re.sub(r"<h4[^>]*>\s*", "\n\n#### ", result, flags=re.IGNORECASE)
        result = re.sub(r"<h5[^>]*>\s*", "\n\n##### ", result, flags=re.IGNORECASE)
        result = re.sub(r"<h6[^>]*>\s*", "\n\n###### ", result, flags=re.IGNORECASE)
        result = re.sub(r"</h[1-6]>", "\n\n", result, flags=re.IGNORECASE)

        result = re.sub(r"<p[^>]*>\s*", "\n\n", result, flags=re.IGNORECASE)
        result = re.sub(r"</p>", "\n\n", result, flags=re.IGNORECASE)

        result = re.sub(r"<br\s*/?>\s*", "\n", result, flags=re.IGNORECASE)
        result = re.sub(r"<br[^>]*>", "\n", result, flags=re.IGNORECASE)

        result = re.sub(r"<ul[^>]*>\s*", "\n", result, flags=re.IGNORECASE)
        result = re.sub(r"</ul>", "\n", result, flags=re.IGNORECASE)
        result = re.sub(r"<ol[^>]*>\s*", "\n", result, flags=re.IGNORECASE)
        result = re.sub(r"</ol>", "\n", result, flags=re.IGNORECASE)
        result = re.sub(r"<li[^>]*>\s*", "- ", result, flags=re.IGNORECASE)
        result = re.sub(r"</li>", "\n", result, flags=re.IGNORECASE)

        result = re.sub(r"<strong[^>]*>", "**", result, flags=re.IGNORECASE)
        result = re.sub(r"</strong>", "**", result, flags=re.IGNORECASE)
        result = re.sub(r"<b[^>]*>", "**", result, flags=re.IGNORECASE)
        result = re.sub(r"</b>", "**", result, flags=re.IGNORECASE)
        result = re.sub(r"<em[^>]*>", "*", result, flags=re.IGNORECASE)
        result = re.sub(r"</em>", "*", result, flags=re.IGNORECASE)
        result = re.sub(r"<i[^>]*>", "*", result, flags=re.IGNORECASE)
        result = re.sub(r"</i>", "*", result, flags=re.IGNORECASE)

        result = re.sub(r"<code[^>]*>", "`", result, flags=re.IGNORECASE)
        result = re.sub(r"</code>", "`", result, flags=re.IGNORECASE)
        result = re.sub(r"<pre[^>]*>\s*", "\n\n```\n", result, flags=re.IGNORECASE)
        result = re.sub(r"</pre>", "\n```\n", result, flags=re.IGNORECASE)

        result = re.sub(r'<a[^>]+href="([^"]+)"[^>]*>([^<]+)</a>', r"[\2](\1)", result, flags=re.IGNORECASE)

        result = re.sub(r"<table[^>]*>\s*", "\n\n", result, flags=re.IGNORECASE)
        result = re.sub(r"</table>", "\n\n", result, flags=re.IGNORECASE)
        result = re.sub(r"<tr[^>]*>\s*", "| ", result, flags=re.IGNORECASE)
        result = re.sub(r"</tr>", " |\n", result, flags=re.IGNORECASE)
        result = re.sub(r"<td[^>]*>\s*", " ", result, flags=re.IGNORECASE)
        result = re.sub(r"</td>", " |", result, flags=re.IGNORECASE)
        result = re.sub(r"<th[^>]*>\s*", " ", result, flags=re.IGNORECASE)
        result = re.sub(r"</th>", " |", result, flags=re.IGNORECASE)
        result = re.sub(r"<thead[^>]*>\s*", "", result, flags=re.IGNORECASE)
        result = re.sub(r"</thead>", "", result, flags=re.IGNORECASE)
        result = re.sub(r"<tbody[^>]*>\s*", "", result, flags=re.IGNORECASE)
        result = re.sub(r"</tbody>", "", result, flags=re.IGNORECASE)

        result = re.sub(r"<span[^>]*>", "", result, flags=re.IGNORECASE)
        result = re.sub(r"</span>", "", result, flags=re.IGNORECASE)
        result = re.sub(r"<div[^>]*>\s*", "\n", result, flags=re.IGNORECASE)
        result = re.sub(r"</div>", "\n", result, flags=re.IGNORECASE)

        result = re.sub(r"<[^>]+>", "", result)
        result = unescape(result).replace("\xa0", " ")
        result = re.sub(r"\n{3,}", "\n\n", result)
        return result.strip()

    def _append_attachments(self, md: List[str], attachments: Optional[List[Attachment]], attach_path: str):
        """添加附件列表。"""
        if not attachments:
            return

        md.extend(["## 附件", ""])
        for att in attachments:
            file_name = Path(att.local_path).name if att.local_path else att.safe_file_name
            if att.is_image():
                md.extend([f"![{file_name}]({attach_path}/{file_name})", ""])
            else:
                md.append(f"- [{file_name}]({attach_path}/{file_name})")
        md.append("")

    @staticmethod
    def _safe(value: Optional[str]) -> str:
        """安全获取字符串值。"""
        return value if value else "-"

    @staticmethod
    def _write_file(path: Path, content: str):
        """写入文件。"""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
