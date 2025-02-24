from flask import Flask

from .config import config
from .logger import setup_logger


def create_app(config_name="default"):
    try:
        app = Flask(__name__)
        print("4")

        # 加载配置
        app.config.from_object(config[config_name])

        print("5")

        # 设置日志
        setup_logger(app)
        print("6")

        # 注册路由和蓝图
        from . import routes

        app.register_blueprint(routes.bp)

        app.logger.info("Application started")
        return app
    except Exception as e:
        import traceback

        traceback.print_exc()
        traceback.print_stack()
