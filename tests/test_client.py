import unittest
from unittest.mock import MagicMock, patch

import requests

from scripts.chandao_fetch.client import ChandaoClient
from scripts.chandao_fetch.config import ChandaoConfig


class ClientTest(unittest.TestCase):
    def test_request_uses_configured_timeout(self):
        config = ChandaoConfig()
        config.base_url = "https://zentao.example.invalid"
        config.username = "tester"
        config.password = "dummy-password"
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

    def test_request_error_does_not_print_url(self):
        config = ChandaoConfig()
        config.base_url = "https://zentao.example.invalid"
        config.username = "tester"
        config.password = "dummy-password"

        client = ChandaoClient(config)
        client.session.request = MagicMock(
            side_effect=requests.ConnectionError(
                "failed to reach https://zentao.example.invalid/story-view-1.json"
            )
        )

        with self.assertRaises(Exception) as exc:
            client._request("get", "https://zentao.example.invalid/story-view-1.json")

        self.assertNotIn("zentao.example.invalid", str(exc.exception))
        self.assertTrue(exc.exception.__suppress_context__)

    def test_fetch_json_http_error_does_not_print_url(self):
        config = ChandaoConfig()
        config.base_url = "https://zentao.example.invalid"
        config.username = "tester"
        config.password = "dummy-password"

        client = ChandaoClient(config)
        client.logged_in = True
        response = MagicMock()
        response.ok = False
        response.status_code = 404
        client._request = MagicMock(return_value=response)

        with self.assertRaises(Exception) as exc:
            client._fetch_json("https://zentao.example.invalid/story-view-1.json")

        self.assertNotIn("zentao.example.invalid", str(exc.exception))

    def test_read_json_error_does_not_print_response_body(self):
        response = MagicMock()
        response.json.side_effect = ValueError("bad json")
        response.text = "internal host or internal html body"

        with self.assertRaises(Exception) as exc:
            ChandaoClient._read_json(response)

        self.assertNotIn("internal html body", str(exc.exception))

    def test_login_does_not_print_username(self):
        config = ChandaoConfig()
        config.base_url = "https://zentao.example.invalid"
        config.username = "tester"
        config.password = "dummy-password"

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
