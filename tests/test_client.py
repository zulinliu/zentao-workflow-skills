import unittest
from unittest.mock import MagicMock, patch

from scripts.chandao_fetch.client import ChandaoClient
from scripts.chandao_fetch.config import ChandaoConfig


class ClientTest(unittest.TestCase):
    def test_request_uses_configured_timeout(self):
        config = ChandaoConfig()
        config.base_url = "https://zentao.example.invalid"
        config.username = "tester"
        config.password = "secret"
        config.connect_timeout = 12000
        config.read_timeout = 34000

        client = ChandaoClient(config)
        client.session.request = MagicMock()

        client._request("get", "https://zentao.example.invalid/story-view-1.json")

        client.session.request.assert_called_once_with(
            "get",
            "https://zentao.example.invalid/story-view-1.json",
            timeout=(12.0, 34.0),
        )

    def test_login_does_not_print_username(self):
        config = ChandaoConfig()
        config.base_url = "https://zentao.example.invalid"
        config.username = "tester"
        config.password = "secret"

        client = ChandaoClient(config)
        response = MagicMock()
        response.ok = True
        client._request = MagicMock(return_value=response)
        client._read_json = MagicMock(return_value={"result": "success"})

        with patch("builtins.print") as mock_print:
            self.assertTrue(client.login())

        mock_print.assert_called_once_with("登录成功")


if __name__ == "__main__":
    unittest.main()
