import logging
from typing import Dict, List, Optional

import requests

logger = logging.getLogger(__name__)


class NotionClient:
    """Notion API 客户端"""

    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Notion-Version": "2022-06-28",  # 使用最新的 API 版本
            "Content-Type": "application/json",
        }

    def create_page_in_database(
        self, database_id: str, page_title: str, properties: dict
    ) -> str:
        """在数据库中创建新的页面（行记录）

        Args:
            database_id: 数据库 ID
            page_title: 页面标题
            properties: 属性值字典，键为属性名，值为属性内容

        Returns:
            str: 创建的页面 ID

        Raises:
            NotionAPIError: 当 API 调用失败时
        """
        try:
            url = f"{self.base_url}/pages"

            # 构建属性字典
            properties_payload = {
                "标题": {"title": [{"type": "text", "text": {"content": page_title}}]}
            }

            # 添加其他属性
            for prop_name, prop_value in properties.items():
                properties_payload[prop_name] = {
                    "rich_text": [
                        {"type": "text", "text": {"content": str(prop_value)}}
                    ]
                }

            # 构建请求体
            payload = {
                "parent": {"database_id": database_id},
                "properties": properties_payload,
            }

            # 发送请求
            response = requests.post(url, headers=self.headers, json=payload)

            if response.status_code != 200:
                raise NotionAPIError(
                    f"Failed to create page: {response.status_code} - {response.text}"
                )

            # 返回创建的页面 ID
            return response.json()["id"]

        except Exception as e:
            logger.error(
                f"Failed to create page '{page_title}' in database {database_id}: {str(e)}"
            )
            raise NotionAPIError(f"Failed to create page: {str(e)}")

    def create_database_in_page(
        self,
        page_id: str,
        title_plain_text: str,
        properties: list[str],
    ) -> str:
        """在指定页面下创建数据库

        Args:
            page_id: Notion 页面 ID
            title_plain_text: 数据库标题
            properties: 数据库属性列表

        Returns:
            str: 创建的数据库 ID

        Raises:
            NotionAPIError: 当 API 调用失败时
        """
        try:
            url = f"{self.base_url}/databases"

            # 构建属性字典
            properties_dict = {"标题": {"title": {}}}  # 默认标题列

            # 添加其他属性
            for prop in properties:
                properties_dict[prop] = {"rich_text": {}}  # 默认使用富文本类型

            # 构建请求体
            payload = {
                "parent": {"type": "page_id", "page_id": page_id},
                "title": [{"type": "text", "text": {"content": title_plain_text}}],
                "properties": properties_dict,
            }

            # 发送请求
            response = requests.post(url, headers=self.headers, json=payload)

            if response.status_code != 200:
                raise NotionAPIError(
                    f"Failed to create database: {response.status_code} - {response.text}"
                )

            # 返回创建的数据库 ID
            return response.json()["id"]

        except Exception as e:
            logger.error(f"Failed to create database '{title_plain_text}': {str(e)}")
            raise NotionAPIError(f"Failed to create database: {str(e)}")

    def get_database_by_title_text(
        self, page_id: str, title_plain_text: str
    ) -> Optional[Dict]:
        """根据标题文本查找数据库

        Args:
            page_id: Notion 页面 ID
            title_plain_text: 要查找的数据库标题文本

        Returns:
            Optional[Dict]: 找到的数据库信息，如果未找到则返回 None
        """
        try:
            # 获取页面中的所有数据库
            databases = self.get_databases_in_page(page_id)

            # 遍历数据库，查找匹配的标题
            for db in databases:
                # 获取数据库标题
                title = db.get("title", [])
                if not title:
                    continue

                # 提取纯文本标题
                db_title_text = "".join(
                    item.get("plain_text", "")
                    for item in title
                    if isinstance(item, dict)
                )

                # 比较标题
                if db_title_text == title_plain_text:
                    return db

            return None

        except Exception as e:
            logger.error(
                f"Failed to find database with title '{title_plain_text}': {str(e)}"
            )
            raise NotionAPIError(f"Failed to find database: {str(e)}")

    def get_databases_in_page(self, page_id: str) -> List[Dict]:
        """
        获取指定页面下的所有数据库信息

        Args:
            page_id: Notion 页面 ID

        Returns:
            List[Dict]: 数据库信息列表

        Raises:
            NotionAPIError: 当 API 调用失败时
        """
        try:
            # 首先获取页面的块信息
            blocks = self._get_page_blocks(page_id)

            # 过滤出数据库类型的块
            databases = []
            for block in blocks:
                if block.get("type") == "child_database":
                    db_id = block.get("id")
                    # 获取数据库详细信息
                    db_info = self._get_database(db_id)
                    if db_info:
                        databases.append(db_info)

            return databases

        except Exception as e:
            logger.error(f"Failed to get databases in page {page_id}: {str(e)}")
            raise NotionAPIError(f"Failed to get databases: {str(e)}")

    def _get_page_blocks(self, page_id: str) -> List[Dict]:
        """获取页面的所有块"""
        url = f"{self.base_url}/blocks/{page_id}/children"

        results = []
        has_more = True
        start_cursor = None

        while has_more:
            params = {"page_size": 100}
            if start_cursor:
                params["start_cursor"] = start_cursor

            response = requests.get(url, headers=self.headers, params=params)

            if response.status_code != 200:
                raise NotionAPIError(
                    f"Failed to get blocks: {response.status_code} - {response.text}"
                )

            data = response.json()
            results.extend(data.get("results", []))

            has_more = data.get("has_more", False)
            start_cursor = data.get("next_cursor")

        return results

    def _get_database(self, database_id: str) -> Optional[Dict]:
        """获取数据库详细信息"""
        url = f"{self.base_url}/databases/{database_id}"

        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            logger.error(
                f"Failed to get database {database_id}: "
                f"{response.status_code} - {response.text}"
            )
            return None

        return response.json()


class NotionAPIError(Exception):
    """Notion API 调用异常"""

    pass
