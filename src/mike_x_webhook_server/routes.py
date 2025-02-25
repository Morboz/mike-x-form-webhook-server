import hashlib
import json
import os
import traceback
import threading

from flask import Blueprint, current_app, request

from mike_x_webhook_server.mikex.form import FormSubmission
from mike_x_webhook_server.notion import NotionClient

bp = Blueprint("main", __name__)


# 首页路由
@bp.route("/")
def home():
    return "Hello, Flask!"


@bp.route("/url_verify", methods=["POST"])
def url_verify():
    try:
        # 获取表单字段
        req_uuid = request.form.get("req_uuid", "")
        repeat = request.form.get("repeat", "")
        timestamp = request.form.get("timestamp", "")
        payload = request.form.get("payload", "")
        sign = request.form.get("sign", "")
        # event = 'URL_VERIFY'
        event = request.form.get("event", "")
        access_key = os.environ.get("MIKEX_ACCESS_KEY", "")
        secret_key = os.environ.get("MIKEX_SECRET_KEY", "")
        valid_sign = check_sign(
            event, req_uuid, repeat, timestamp, payload, access_key, secret_key, sign
        )

        if valid_sign == sign:
            # return payload, 200
            return do_handle_event(event, payload)
        else:
            return "Invalid signature", 400

    except Exception as e:
        current_app.logger.error(f"Error processing request: {str(e)}")
        return "Internal server error", 500


def do_handle_event(event, payload) -> tuple[str, int]:
    if event == "URL_VERIFY":
        return do_handle_URL_VERIFY(payload), 200
    elif event == "FORM_SUBMIT_NEW":
        return do_handle_FORM_SUBMIT_NEW(payload), 200
    elif event == "IFP_PAID":
        return do_handle_IFP_PAID(payload), 200
    else:
        return "Unsupported event", 400


def do_handle_URL_VERIFY(payload) -> str:
    return payload


def do_handle_FORM_SUBMIT_NEW(payload) -> str:
    current_app.logger.info(f"Received payload: {payload}")
    json.loads(payload)
    return "ok"


def do_handle_IFP_PAID(payload) -> str:
    current_app.logger.info(f"Received payload: {payload}")
    try:
        # update_notion_database_with_form_submit(payload)
        # 使用线程异步处理
        task_thread = threading.Thread(
            target=update_notion_database_with_form_submit, args=(payload,)
        )
        task_thread.start()
        return "ok"
    except Exception as e:
        current_app.logger.error(f"Error processing IFP_PAID event: {str(e)}")
        current_app.logger.error(traceback.format_exc())
        return "Internal server error", 500


def check_sign(
    event, req_uuid, repeat, timestamp, payload, access_key, secret_key, sign
):
    # 按指定顺序拼接字符串
    string = f"{event}\n{req_uuid}\n{repeat}\n{timestamp}\n{payload}\n{access_key}\n{secret_key}\n"
    current_app.logger.info(f"String to sign: {string}")
    calculated_sign = hashlib.sha256(string.encode()).hexdigest()
    current_app.logger.info(f"Calculated sign: {calculated_sign}")
    current_app.logger.info(f"Received sign: {sign}")
    # 比对签名
    if calculated_sign == sign:
        return calculated_sign
    else:
        return None


def update_notion_database_with_form_submit(payload: str) -> str:
    form_data = json.loads(payload)
    form_submission = FormSubmission(**form_data)
    database_title = form_submission.get_form_title()
    token = os.getenv("NOTION_TOKEN")
    page_id = os.getenv("NOTION_PAGE_ID")
    notion_client = NotionClient(token=token)

    result = notion_client.get_database_by_title_text(page_id, database_title)
    if result is None:
        database_id = notion_client.create_database_in_page(
            page_id, database_title, form_submission.get_questions()
        )
    else:
        database_id = result["id"]

    page_id = notion_client.create_page_in_database(
        database_id,
        form_submission.get_notion_page_title(),
        form_submission.get_question_submit_mapping(),
    )
    return page_id
