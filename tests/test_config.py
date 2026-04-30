import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.chandao_fetch.config import ChandaoConfig


class ChandaoConfigTest(unittest.TestCase):
    def test_resolve_output_dir_is_fixed_workspace_chandao(self):
        config = ChandaoConfig()
        output_dir = config.resolve_output_dir(r"D:\work\demo")

        self.assertTrue(output_dir.endswith("demo\\chandao"))

    def test_initialize_interactively_writes_global_config(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            fake_home = Path(temp_dir)
            config = ChandaoConfig()

            with patch("scripts.chandao_fetch.config.Path.home", return_value=fake_home):
                config.initialize_interactively(
                    input_func=lambda prompt: {
                        "请输入禅道地址: ": "https://zentao.example.invalid/",
                        "请输入禅道账号: ": "tester",
                    }[prompt],
                    getpass_func=lambda prompt: "dummy-password",
                )

                saved_file = fake_home / ".chandao" / "config.properties"
                self.assertTrue(saved_file.exists())

                loaded = ChandaoConfig.load()
                self.assertEqual(loaded.base_url, "https://zentao.example.invalid")
                self.assertEqual(loaded.username, "tester")
                self.assertEqual(loaded.password, "dummy-password")

    def test_initialize_interactively_force_prompt_overwrites_existing_values(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            fake_home = Path(temp_dir)
            config = ChandaoConfig()
            config.base_url = "https://old.example.invalid"
            config.username = "old-user"
            config.password = "old-dummy-password"

            with patch("scripts.chandao_fetch.config.Path.home", return_value=fake_home):
                config.initialize_interactively(
                    input_func=lambda prompt: {
                        "请输入禅道地址: ": "https://new.example.invalid",
                        "请输入禅道账号: ": "new-user",
                    }[prompt],
                    getpass_func=lambda prompt: "new-dummy-password",
                    force_prompt=True,
                )

                loaded = ChandaoConfig.load()
                self.assertEqual(loaded.base_url, "https://new.example.invalid")
                self.assertEqual(loaded.username, "new-user")
                self.assertEqual(loaded.password, "new-dummy-password")


if __name__ == "__main__":
    unittest.main()
