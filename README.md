# Mike X Form Webhook Server

一个用于处理表单提交的 Webhook 服务器，基于 Flask 构建。

## 功能特点

- 接收并处理表单提交的数据
- 支持多种日志输出方式
- 可配置的环境变量
- 开发模式支持热重载

## 快速开始

### 安装

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/mike-x-form-webhook-server.git
cd mike-x-form-webhook-server
```

2. 安装依赖：
```bash
pip install -e .
```

### 配置

1. 创建 `.env` 文件：
```env
FLASK_ENV=development
FLASK_DEBUG=1
LOG_LEVEL=DEBUG
```

2. 创建 `.flaskenv` 文件（可选）：
```env
FLASK_APP=src.mike_x_webhook_server
```

### 运行服务器

有多种方式可以运行服务器：

1. 使用 Flask CLI：
```bash
flask run
```

2. 使用 Python 模块：
```bash
python -m mike_x_webhook_server
```

3. 使用开发调试脚本：
```bash
python debug.py
```

## API 接口

### 接收表单数据

```http
POST /webhook/form
Content-Type: application/json

{
    "name": "张三",
    "email": "zhangsan@example.com",
    "message": "测试消息"
}
```

## 开发指南

### 项目结构

```
mike-x-form-webhook-server/
├── src/
│   └── mike_x_webhook_server/
│       ├── __init__.py      # 应用初始化
│       ├── __main__.py      # 入口点
│       ├── app.py           # Flask app 定义
│       ├── config.py        # 配置
│       ├── logger.py        # 日志配置
│       └── routes/          # 路由
├── tests/                   # 测试文件
├── debug.py                 # 开发调试入口
├── pyproject.toml          # 项目元数据
└── README.md
```

### 调试

1. IDE 调试（推荐）：
   - 使用 `debug.py` 作为入口点
   - 可以设置断点
   - 支持热重载

2. 使用 pytest 运行测试：
```bash
pytest -s
```

### 日志配置

日志会同时输出到文件和控制台：

- 日志文件位置：`logs/app.log`
- 日志级别通过环境变量 `LOG_LEVEL` 控制
- 支持日志文件轮转

## 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| FLASK_ENV | 运行环境 | production |
| FLASK_DEBUG | 调试模式 | 0 |
| LOG_LEVEL | 日志级别 | INFO |
| LOG_DIR | 日志目录 | logs |
| LOG_FILENAME | 日志文件名 | app.log |

## 部署

### 使用 Docker（推荐）

1. 构建镜像：
```bash
docker build -t mike-x-webhook-server .
```

2. 运行容器：
```bash
docker run -p 5000:5000 mike-x-webhook-server
```

### 直接部署

1. 安装依赖：
```bash
pip install .
```

2. 使用 gunicorn 运行：
```bash
gunicorn "mike_x_webhook_server:create_app()"
```

## 贡献指南

1. Fork 项目
2. 创建特性分支
3. 提交改动
4. 发起 Pull Request

## 许可证

[MIT License](LICENSE)

## 联系方式

- 作者：[Your Name]
- 邮箱：[your.email@example.com]