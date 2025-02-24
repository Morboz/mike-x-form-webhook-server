from typing import List, Optional

from pydantic import BaseModel


class CommonSysInfo(BaseModel):
    CLIENT_ID: int
    FORM_ID: int
    FORM_NAME: str
    SUBMIT_ID: int
    SUBMIT_NO: int
    SUBMIT_TIME_LOCAL: str
    IP_LOCATION: str


class CommonRandomCode(BaseModel):
    code: Optional[str]
    title: Optional[str]


class CommonTicket(BaseModel):
    title: Optional[str]
    description: Optional[str]
    number: Optional[str]
    url_qrcode: Optional[str]


class CommonInfo(BaseModel):
    SYS: CommonSysInfo
    random_code: Optional[CommonRandomCode] = None
    ticket: Optional[CommonTicket] = None
    wechat_open_id: Optional[str] = None


class CashierInfo(BaseModel):
    mike_order_number: str
    currency_code: str
    currency_sign: str
    total: str


class Question(BaseModel):
    id: str
    type: str
    text: str


class Answer(BaseModel):
    text: Optional[str] = None
    id: Optional[int] = None

    def to_plain_text(self) -> str:
        return self.text


class SalesAnswer(BaseModel):
    id: int
    commodity: str
    quantity: int
    unit_price: float
    sub_total: str
    currency_code: str
    currency_sign: str

    def to_plain_text(self) -> str:
        return f"{self.commodity} x {self.quantity} ({self.currency_sign}{self.unit_price}) = {self.currency_sign}{self.sub_total}"


class QuestionSubmit(BaseModel):
    question_id: str
    answer: Answer | List[SalesAnswer]


class FormSubmission(BaseModel):
    common: CommonInfo
    question: List[dict]
    submit: List[QuestionSubmit]
    cashier: Optional[CashierInfo] = None

    def get_form_title(self) -> str:
        return self.common.SYS.FORM_NAME

    def get_question_submit_mapping(self) -> dict[str, str]:
        """获取问题文本和答案文本的映射关系

        Returns:
            dict[str, str]: 键为问题文本，值为答案文本。多个答案用'|'分隔
        """
        # 先创建问题ID到问题文本的映射
        question_text_map = {q["id"]: q["text"] for q in self.question}

        # 创建最终的问题文本到答案的映射
        result = {}
        for submit_item in self.submit:
            question_id = submit_item.question_id
            question_text = question_text_map[question_id]

            # 处理答案
            if isinstance(submit_item.answer, list):
                # 如果是多个答案（比如销售类型），用'|'连接
                answer_text = " | ".join(
                    item.to_plain_text() for item in submit_item.answer
                )
            else:
                # 单个答案
                answer_text = submit_item.answer.to_plain_text()

            result[question_text] = answer_text

        return result

    def get_questions(self) -> list[str]:
        """获取表单中所有问题的文本列表

        Returns:
            list[str]: 问题文本列表
        """
        return [question["text"] for question in self.question]

    def get_notion_page_title(self) -> str:
        """获取 Notion 页面标题

        Returns:
            str: 如果存在 CT_NAME 类型的问题答案，返回该答案；否则返回随机生成的 UUID
        """
        import uuid

        # 遍历所有问题和提交
        for question, submit in zip(self.question, self.submit):
            if question["type"] == "CT_NAME":
                return submit.answer.text

        # 如果没有找到 CT_NAME 类型的问题答案，返回随机 UUID
        return str(uuid.uuid4())


if __name__ == "__main__":
    # 使用示例
    mock_form_data = {
        "common": {
            "SYS": {
                "CLIENT_ID": 90118,
                "FORM_ID": 200613744,
                "FORM_NAME": "Mike -> Notion 表单统一-副本",
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
                "text": "请给个自我介绍，让我们更了解你吧！",
            },
            {
                "id": "206270742",
                "type": "RADIO",
                "text": "你是从哪里看到并加入本次共学的？",
            },
            {"id": "206270737", "type": "TEXT", "text": "邮箱"},
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
                "answer": {
                    "text": "关于活动的问题和建议，或你是否有任何期望？ceshiceshi"
                },
            },
        ],
        "cashier": {
            "mike_order_number": "IFP-IT1L1-2411260000028246",
            "currency_code": "CNY",
            "currency_sign": "¥",
            "total": "748.00",
        },
    }
    form_submission = FormSubmission(**mock_form_data)
    print(form_submission.model_dump())
    print(form_submission.model_dump_json())
    print(form_submission.get_form_title())
    print(form_submission.get_question_submit_mapping())
