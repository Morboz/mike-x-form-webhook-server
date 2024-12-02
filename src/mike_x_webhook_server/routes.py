import hashlib
from flask import Blueprint, request, current_app
import os
import json

bp = Blueprint('main', __name__)


# 首页路由
@bp.route('/')
def home():
    return 'Hello, Flask!'

@bp.route('/url_verify', methods=['POST'])
def url_verify():
    try:
        # 获取表单字段
        req_uuid = request.form.get('req_uuid', '')
        repeat = request.form.get('repeat', '')
        timestamp = request.form.get('timestamp', '')
        payload = request.form.get('payload', '')
        sign = request.form.get('sign', '')
        # event = 'URL_VERIFY'
        event = request.form.get('event', '')
        access_key = os.environ.get('MIKEX_ACCESS_KEY', '')
        secret_key = os.environ.get('MIKEX_SECRET_KEY', '')   
        valid_sign = check_sign(event, req_uuid, repeat, timestamp, payload, access_key, secret_key, sign)

        if valid_sign == sign:
            # return payload, 200
            return do_handle_event(event, payload)
        else:
            return 'Invalid signature', 400

    except Exception as e:
        current_app.logger.error(f"Error processing request: {str(e)}")
        return 'Internal server error', 500


def do_handle_event(event, payload) -> tuple[str, int]:
    if event == 'URL_VERIFY':
        return do_handle_URL_VERIFY(payload), 200
    elif event == 'FORM_SUBMIT_NEW':
        return do_handle_FORM_SUBMIT_NEW(payload), 200


def do_handle_URL_VERIFY(payload) -> str:
    return payload

def do_handle_FORM_SUBMIT_NEW(payload) -> str:
    current_app.logger.info(f"Received payload: {payload}")
    json.loads(payload)
    return 'OK'


def check_sign(event, req_uuid, repeat, timestamp, payload, access_key, secret_key, sign):
    # 按指定顺序拼接字符串
    string = f'{event}\n{req_uuid}\n{repeat}\n{timestamp}\n{payload}\n{access_key}\n{secret_key}\n'
    current_app.logger.info(f"String to sign: {string}")
    calculated_sign = hashlib.sha256(string.encode()).hexdigest()
    current_app.logger.info(f"Calculated sign: {calculated_sign}")
    current_app.logger.info(f"Received sign: {sign}")
    # 比对签名
    if calculated_sign == sign:
        return calculated_sign
    else:
        return None