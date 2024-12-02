import os
from datetime import timedelta

class Config:
    # 基础配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change'
    
    # Flask配置
    DEBUG = False
    TESTING = False
    
    # Mike X 配置
    MIKEX_ACCESS_KEY = os.environ.get('MIKEX_ACCESS_KEY')
    MIKEX_SECRET_KEY = os.environ.get('MIKEX_SECRET_KEY')
    
    # 服务器配置
    HOST = '0.0.0.0'
    PORT = 5000

     # 日志配置
    LOG_DIR = 'logs'  # 日志目录
    LOG_FILENAME = 'app.log'  # 日志文件名
    LOG_LEVEL = 'INFO'  # 日志级别
    LOG_FORMAT = '%(asctime)s [%(levelname)s] %(pathname)s:%(lineno)d: %(message)s'  # 日志格式
    LOG_MAX_BYTES = 10 * 1024 * 1024  # 每个日志文件最大尺寸（10MB）
    LOG_BACKUP_COUNT = 5  # 保留的日志文件数量
    # ... 其他配置 ...
    REDIRECT_STDOUT = False  # 默认不重定向


class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False
    # 生产环境特定配置
    
class TestingConfig(Config):
    TESTING = True
    DEBUG = True

# 配置映射
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}