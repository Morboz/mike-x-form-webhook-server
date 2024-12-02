import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from flask import request


class LoggerWriter:
    def __init__(self, logger, level):
        self.logger = logger
        self.level = level
        self.buffer = []

    def write(self, message):
        if message.strip():
            self.logger.log(self.level, message.strip())
        return len(message)  # 返回写入的字符数
    
    def flush(self):
        pass

def setup_logger(app):
    print("setup_logger ... 1")
    # 创建日志目录
    if not os.path.exists(app.config['LOG_DIR']):
        os.makedirs(app.config['LOG_DIR'])
    print("setup_logger ... 2")
    
    # 设置日志文件路径
    log_file = os.path.join(app.config['LOG_DIR'], app.config['LOG_FILENAME'])
    
    # 创建 RotatingFileHandler
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=app.config['LOG_MAX_BYTES'],
        backupCount=app.config['LOG_BACKUP_COUNT'],
        encoding='utf-8'
    )
    print("setup_logger ... 3")
    
    # 设置日志格式
    formatter = logging.Formatter(app.config['LOG_FORMAT'])
    file_handler.setFormatter(formatter)
    print("setup_logger ... 4")

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    print("setup_logger ... 5")

    
    # 设置日志级别
    file_handler.setLevel(app.config['LOG_LEVEL'])
    stream_handler.setLevel(app.config['LOG_LEVEL'])

    
    # 添加处理器到 app.logger
    app.logger.addHandler(file_handler)
    app.logger.addHandler(stream_handler)

    app.logger.setLevel(app.config['LOG_LEVEL'])
    print("setup_logger ... 6")
    
    # # 将标准输出和错误输出重定向到日志
    # 安全地重定向标准输出和错误输出
    if app.config.get('REDIRECT_STDOUT', False):
        sys.stdout = LoggerWriter(app.logger, logging.INFO)
        sys.stderr = LoggerWriter(app.logger, logging.ERROR)
    # sys.stdout.write = lambda x: app.logger.info(x.strip())
    # sys.stderr.write = lambda x: app.logger.error(x.strip())
    print("setup_logger ... 7")
    
    # 添加请求日志中间件
    @app.before_request
    def log_request_info():
        app.logger.debug('Headers: %s', dict(request.headers))
        app.logger.debug('Body: %s', request.get_data())

    @app.after_request
    def log_response_info(response):
        app.logger.info(
            '%s %s %s %s %s',
            request.remote_addr,
            request.method,
            request.url,
            response.status,
            response.content_length,
        )
        return response

    # 记录未处理的异常
    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.exception('Unhandled Exception: %s', str(e))
        return 'Internal Server Error', 500