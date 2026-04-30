import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

from scripts.package_skill import (
    PACKAGE_ROOT_NAME,
    build_archive_name,
    build_release_file_list,
    package_skill,
    read_version,
)


class PackageSkillTest(unittest.TestCase):
    def test_release_file_list_contains_core_files(self):
        files = build_release_file_list()
        relative_files = {path.relative_to(Path.cwd()).as_posix() for path in files}

        self.assertIn("SKILL.md", relative_files)
        self.assertIn("agents/openai.yaml", relative_files)
        self.assertIn("references/download-workflow.md", relative_files)
        self.assertIn("scripts/chandao_fetch.py", relative_files)
        self.assertIn("scripts/chandao_fetch/__main__.py", relative_files)
        self.assertNotIn("README.md", relative_files)
        self.assertNotIn("CHANGELOG.md", relative_files)
        self.assertNotIn("VERSION", relative_files)
        self.assertNotIn("tests/test_package_skill.py", relative_files)

    def test_package_skill_creates_zip(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            archive_path = package_skill(Path(temp_dir))
            self.assertTrue(archive_path.exists())
            self.assertEqual(archive_path.name, build_archive_name(read_version()))

            with ZipFile(archive_path) as zf:
                names = set(zf.namelist())
                self.assertIn(f"{PACKAGE_ROOT_NAME}/SKILL.md", names)
                self.assertIn(f"{PACKAGE_ROOT_NAME}/agents/openai.yaml", names)
                self.assertIn(f"{PACKAGE_ROOT_NAME}/references/download-workflow.md", names)
                self.assertIn(f"{PACKAGE_ROOT_NAME}/scripts/chandao_fetch/__main__.py", names)
                self.assertNotIn(f"{PACKAGE_ROOT_NAME}/README.md", names)
                self.assertNotIn(f"{PACKAGE_ROOT_NAME}/CHANGELOG.md", names)
                self.assertNotIn(f"{PACKAGE_ROOT_NAME}/VERSION", names)
                self.assertNotIn(f"{PACKAGE_ROOT_NAME}/tests/test_package_skill.py", names)


if __name__ == "__main__":
    unittest.main()
