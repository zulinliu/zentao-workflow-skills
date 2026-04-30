import tempfile
import unittest
from unittest.mock import MagicMock, patch

from scripts.chandao_fetch.__main__ import collect_ids, main
from scripts.chandao_fetch.config import ChandaoConfig


class CliTest(unittest.TestCase):
    @staticmethod
    def make_initialized_config():
        config = ChandaoConfig()
        config.base_url = "https://zentao.example.invalid"
        config.username = "tester"
        config.password = "dummy-password"
        return config

    def test_collect_ids_keeps_order_and_deduplicates(self):
        args = type("Args", (), {"id": 12, "ids": "12, 13,14,13"})
        self.assertEqual(collect_ids(args), [12, 13, 14])

    def test_main_passes_download_switches_independently(self):
        config = self.make_initialized_config()
        service_instance = MagicMock()
        service_instance.execute.return_value = []

        with tempfile.TemporaryDirectory() as temp_dir:
            with patch("scripts.chandao_fetch.__main__.ChandaoConfig.load", return_value=config), \
                    patch("scripts.chandao_fetch.__main__.ChandaoService", return_value=service_instance), \
                    patch("sys.argv", ["chandao_fetch.py", "-t", "story", "-i", "1", "--no-image"]), \
                    patch("os.getcwd", return_value=temp_dir):
                main()

        service_instance.execute.assert_called_once_with(
            content_type="story",
            ids=[1],
            download_attachments=True,
            download_images=False,
        )

    def test_main_requires_complete_credentials_when_writing_config(self):
        config = ChandaoConfig()

        with tempfile.TemporaryDirectory() as temp_dir:
            with patch("scripts.chandao_fetch.__main__.ChandaoConfig.load", return_value=config), \
                    patch("sys.argv", ["chandao_fetch.py", "-t", "story", "-i", "1", "--url", "https://zentao.example.invalid"]), \
                    patch("os.getcwd", return_value=temp_dir):
                with self.assertRaises(SystemExit) as exc:
                    main()

        self.assertEqual(exc.exception.code, 1)

    def test_main_init_with_credentials_saves_global_config(self):
        config = ChandaoConfig()
        config.save_to_global = MagicMock()

        with tempfile.TemporaryDirectory() as temp_dir:
            with patch("scripts.chandao_fetch.__main__.ChandaoConfig.load", return_value=config), \
                    patch("sys.argv", [
                        "chandao_fetch.py",
                        "--init",
                        "--url", "https://zentao.example.invalid",
                        "--username", "tester",
                        "--password", "dummy-password",
                    ]), \
                    patch("os.getcwd", return_value=temp_dir):
                main()

        config.save_to_global.assert_called_once()


if __name__ == "__main__":
    unittest.main()
