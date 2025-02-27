import dotenv

dotenv.load_dotenv()

import pytest

from mike_x_webhook_server.notion import NotionClient


@pytest.fixture
def notion_client():
    """创建 NotionClient 实例的 fixture"""
    return NotionClient(token="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")


def test_integration_get_databases():
    """集成测试：实际调用 Notion API
    注意：需要设置环境变量 NOTION_TEST_TOKEN 和 NOTION_TEST_PAGE_ID
    """
    import os

    token = os.getenv("NOTION_TOKEN")
    page_id = os.getenv("NOTION_PAGE_ID")

    print(token)
    print(page_id)

    if not token or not page_id:
        pytest.skip("Missing test credentials")

    client = NotionClient(token=token)
    result = client.get_databases_in_page(page_id)

    assert isinstance(result, list)


def test_integration_get_database_by_title():
    """集成测试：实际调用 Notion API
    注意：需要设置环境变量 NOTION_TEST_TOKEN 和 NOTION_TEST_PAGE_ID
    """
    import os

    token = os.getenv("NOTION_TOKEN")
    page_id = os.getenv("NOTION_PAGE_ID")

    print(token)
    print(page_id)

    if not token or not page_id:
        pytest.skip("Missing test credentials")

    client = NotionClient(token=token)
    result = client.get_database_by_title_text(page_id, "USER")
    print(result)


def test_create_database():
    import os

    token = os.getenv("NOTION_TOKEN")
    page_id = os.getenv("NOTION_PAGE_ID")

    print(token)
    print(page_id)

    if not token or not page_id:
        pytest.skip("Missing test credentials")

    client = NotionClient(token=token)
    database_id = client.create_database_in_page(
        page_id=page_id,
        title_plain_text="我的数据库",
        properties=["姓名", "电话", "备注"],
    )
    print(database_id)


def test_create_page_in_database():
    import os

    token = os.getenv("NOTION_TOKEN")
    page_id = os.getenv("NOTION_PAGE_ID")

    print(token)
    print(page_id)

    if not token or not page_id:
        pytest.skip("Missing test credentials")

    client = NotionClient(token=token)
    page_id = client.create_page_in_database(
        database_id="150ec3603acf81cdaea7f4b24afaf159",
        page_title="新记录",
        properties={"姓名": "张三", "电话": "13800138000", "备注": "测试数据"},
    )
    print(page_id)
