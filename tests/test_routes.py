import dotenv

dotenv.load_dotenv()
import json

from mike_x_webhook_server.routes import update_notion_database_with_form_submit

mock_form_data = {
    "common": {
        "SYS": {
            "CLIENT_ID": 90118,
            "FORM_ID": 200613744,
            "FORM_NAME": "【TOPIC】Mike -> Notion 表单统一-副本",
            "SUBMIT_ID": 272702538,
            "SUBMIT_NO": 3,
            "SUBMIT_TIME_LOCAL": "2024-11-26 14:54:44",
            "IP_LOCATION": "上海市",
        }
    },
    "question": [
        {"id": "206270735", "type": "CT_NAME", "text": "姓名\/昵称"},
        {"id": "206270736", "type": "TEXT", "text": "微信\/手机号"},
        {"id": "206270743", "type": "RADIO", "text": "是否参加过往期共学？"},
        {
            "id": "206270740",
            "type": "TEXT",
            "text": "你的自我介绍",
        },
        {
            "id": "206270742",
            "type": "RADIO",
            "text": "你是从哪里看到并加入本次共学的？",
        },
        {"id": "206270737", "type": "TEXT", "text": "你的邮箱"},
        {
            "id": "206270738",
            "type": "TEXT",
            "text": "可否告知具体社群，我们会向该在地社区或小组进行捐赠",
        },
        {"id": "206270741", "type": "TEXT", "text": "Sui 钱包地址收集"},
        {"id": "206270739", "type": "SALE", "text": "购票"},
        {
            "id": "206270744",
            "type": "TEXT",
            "text": "关于活动的问题和建议，或你是否有任何期望？",
        },
    ],
    "submit": [
        {"question_id": "206270735", "answer": {"text": "maoerbaoziXx"}},
        {"question_id": "206270736", "answer": {"text": "15527366855"}},
        {
            "question_id": "206270743",
            "answer": {"id": 206400796, "text": "否，第一次参加"},
        },
        {
            "question_id": "206270740",
            "answer": {"text": "请给个自我介绍，让我们更了解你吧！"},
        },
        {
            "question_id": "206270742",
            "answer": {"id": 206400784, "text": "706公众号及社群"},
        },
        {"question_id": "206270737", "answer": {"text": "695513639@qq.com"}},
        {"question_id": "206270738", "answer": {"text": "上海706"}},
        {"question_id": "206270741", "answer": {"text": "ceshidizhi 123123"}},
        {
            "question_id": "206270739",
            "answer": [
                {
                    "id": 200203369,
                    "commodity": "早鸟票",
                    "quantity": 1,
                    "unit_price": 349,
                    "sub_total": "349.00",
                    "currency_code": "CNY",
                    "currency_sign": "¥",
                },
                {
                    "id": 200203370,
                    "commodity": "正价票",
                    "quantity": 1,
                    "unit_price": 399,
                    "sub_total": "399.00",
                    "currency_code": "CNY",
                    "currency_sign": "¥",
                },
            ],
        },
        {
            "question_id": "206270744",
            "answer": {"text": "关于活动的问题和建议，或你是否有任何期望？ceshiceshi"},
        },
    ],
    "cashier": {
        "mike_order_number": "IFP-IT1L1-2411260000028246",
        "currency_code": "CNY",
        "currency_sign": "¥",
        "total": "748.00",
    },
}


def test_integration_update_notion_database_with_form_submit():
    """集成测试：实际调用 Notion API
    注意：需要设置环境变量 NOTION_TEST_TOKEN 和 NOTION_TEST_PAGE_ID
    """
    payload = json.dumps(mock_form_data)
    update_notion_database_with_form_submit(payload)
