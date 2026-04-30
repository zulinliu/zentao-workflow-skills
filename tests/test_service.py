import tempfile
import unittest
from pathlib import Path

from scripts.chandao_fetch.config import ChandaoConfig
from scripts.chandao_fetch.models import Story, Task
from scripts.chandao_fetch.service import ChandaoService


class FakeClient:
    def __init__(self):
        self.story_calls = []
        self.task_calls = []

    def login(self):
        return True

    def get_task(self, task_id):
        self.task_calls.append(task_id)
        if task_id == 10:
            return Task(id=10, name="子任务", desc="<p> </p>", story=20, parent=30)
        if task_id == 30:
            return Task(id=30, name="父任务", desc="<p>父任务描述</p>")
        raise AssertionError(f"unexpected task id: {task_id}")

    def get_story(self, story_id):
        self.story_calls.append(story_id)
        if story_id == 20:
            return Story(id=20, title="关联需求", spec="<p>需求描述</p>")
        raise AssertionError(f"unexpected story id: {story_id}")

    def get_bug(self, bug_id):
        raise AssertionError(f"unexpected bug id: {bug_id}")

    def download_attachment(self, attachment_id):
        raise AssertionError(f"unexpected attachment download: {attachment_id}")

    def download_image(self, image_path):
        raise AssertionError(f"unexpected image download: {image_path}")


class FakeExporter:
    def __init__(self, output_dir):
        self.output_dir = Path(output_dir)
        self.exported = []

    def export_story(self, story):
        path = self.output_dir / "story" / f"{story.id}.md"
        self.exported.append(("story", story.id))
        return path

    def export_task(self, task):
        path = self.output_dir / "task" / f"{task.id}.md"
        self.exported.append(("task", task.id))
        return path

    def export_bug(self, bug):
        path = self.output_dir / "bug" / f"{bug.id}.md"
        self.exported.append(("bug", bug.id))
        return path


class ServiceTest(unittest.TestCase):
    def test_blank_task_downloads_related_story_and_parent(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            config = ChandaoConfig()
            config.base_url = "https://zentao.example.invalid"
            config.username = "tester"
            config.password = "dummy-password"
            config.output_dir = temp_dir

            service = ChandaoService(config)
            service.client = FakeClient()
            service.exporter = FakeExporter(temp_dir)

            exported = service.execute("task", [10], download_attachments=False, download_images=False)

            self.assertEqual([str(path) for path in exported], [str(Path(temp_dir) / "task" / "10.md")])
            self.assertEqual(service.client.story_calls, [20])
            self.assertEqual(service.client.task_calls, [10, 30])
            self.assertEqual(
                service.exporter.exported,
                [("story", 20), ("task", 30), ("task", 10)],
            )


if __name__ == "__main__":
    unittest.main()
