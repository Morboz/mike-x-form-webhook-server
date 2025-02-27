import unittest
from unittest.mock import MagicMock, patch

import requests

from mike_x_webhook_server.notion import NotionClient


class TestNotionClient(unittest.TestCase):
    def setUp(self):
        self.client = NotionClient("fake_token")

    @patch("time.sleep")  # 防止测试实际等待
    @patch("requests.get")
    def test_get_database_with_retry(self, mock_get, mock_sleep):
        # 创建一个模拟响应对象
        success_response = MagicMock()
        success_response.status_code = 200
        success_response.json.return_value = {"id": "test_db_id"}

        # 设置前两次请求失败，第三次成功
        mock_get.side_effect = [
            requests.RequestException("连接错误"),  # 第1次失败
            requests.RequestException("超时"),  # 第2次失败
            success_response,  # 第3次成功
        ]

        # 调用方法
        result = self.client._get_database("fake_db_id")

        # 验证结果
        self.assertEqual(result["id"], "test_db_id")

        # 验证重试次数
        self.assertEqual(mock_get.call_count, 3)

        # 验证重试间隔
        mock_sleep.assert_any_call(1)  # 第一次重试等待1秒
        mock_sleep.assert_any_call(2)  # 第二次重试等待2秒

    @patch("time.sleep")
    @patch("requests.get")
    def test_get_database_max_retries_exceeded(self, mock_get, mock_sleep):
        # 设置所有请求都失败
        mock_get.side_effect = requests.RequestException("持续失败")

        # 验证达到最大重试次数后抛出异常
        with self.assertRaises(requests.RequestException):
            self.client._get_database("fake_db_id")

        # 验证重试次数为5
        self.assertEqual(mock_get.call_count, 5)
