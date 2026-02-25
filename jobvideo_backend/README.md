# JobVideo 后端平台

这是一个基于 FastAPI 开发的短视频招聘平台后端服务。

## 项目结构

```
app/
├── auth/          # 认证模块
│   ├── __init__.py
│   ├── deps.py     # 依赖项
│   ├── models.py   # 数据模型
│   ├── routes.py   # 路由
│   ├── schemas.py  # 数据校验
│   └── utils.py    # 工具函数
├── company/       # 公司模块
│   └── models.py   # 数据模型
├── interactions/  # 交互行为模块
│   ├── __init__.py
│   ├── models.py   # 数据模型
│   ├── routes.py   # 路由
│   └── services.py # 业务逻辑
├── job/           # 职位模块
│   ├── models.py   # 数据模型
│   ├── routes.py   # 路由
│   └── schemas.py  # 数据校验
├── resume/        # 简历模块
│   ├── models.py   # 数据模型
│   ├── routes.py   # 路由
│   └── schemas.py  # 数据校验
├── video/         # 视频模块
│   ├── __init__.py
│   ├── models.py   # 数据模型
│   ├── resolvers.py # 解析器
│   ├── routes.py   # 路由
│   ├── schemas.py  # 数据校验
│   └── utils.py    # 工具函数
├── __init__.py
├── config.py      # 配置文件
├── db.py          # 数据库配置
└── main.py        # 主入口
Archive/            # 归档文件
README.md           # 项目说明
command.sh          # 命令脚本
test.ipynb          # 测试笔记本
check_and_add_test_data.py # 测试数据脚本
```

## 功能特性

- **视频模块**：视频上传、视频流获取、视频详情查看
- **认证模块**：用户认证、JWT 令牌生成与验证、测试令牌支持
- **职位模块**：职位信息管理
- **简历模块**：简历信息管理
- **公司模块**：公司信息管理
- **交互行为模块**：视频点赞、收藏、浏览记录
- **静态文件服务**：视频文件存储与访问
- **CORS 支持**：跨域请求处理
- **全局异常处理**：统一错误响应

## 技术栈

- Python 3.8+
- FastAPI
- SQLAlchemy ORM
- SQLite（默认）/ PostgreSQL（可选）
- JWT 认证
- Pydantic V2 数据校验

## 安装与运行

### 安装依赖

```bash
pip install fastapi uvicorn sqlalchemy python-jose[cryptography] passlib[bcrypt] python-multipart python-dotenv
```

### 开发环境运行

```bash
uvicorn app.main:app --reload
```

### 生产环境运行

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API 文档

启动服务后，可以访问以下地址查看自动生成的 API 文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 配置说明

### 环境变量

项目支持通过 `.env` 文件配置环境变量，主要配置项：

- `SECRET_KEY`: JWT 签名密钥
- `DATABASE_URL`: 数据库连接 URL

### 数据库配置

默认使用 SQLite 数据库，存储在 `./test.db`。如需使用 PostgreSQL，可修改 `DATABASE_URL`：

```
# SQLite
sqlite:///./test.db

# PostgreSQL
postgresql://user:password@localhost/dbname
```

### 视频存储

视频文件默认存储在 `video_storage` 目录，可通过 `VIDEO_STORAGE_DIR` 配置。

## 主要 API 接口

### 视频模块

- **POST /video/upload**：上传视频
  - 参数：title, description, target_type, target_id, file
  - 返回：视频信息

- **GET /video/feed**：获取视频流
  - 参数：skip, limit, target_type
  - 返回：视频列表，包含关联目标信息、点赞数、收藏数、用户交互状态

- **GET /video/{video_id}**：获取视频详情
  - 参数：video_id
  - 返回：视频详细信息，包含关联目标完整信息、点赞数、收藏数、用户交互状态

### 认证模块

- **POST /auth/register**：用户注册
  - 参数：username, phone, password, role
  - 返回：用户信息

- **POST /auth/login**：用户登录
  - 参数：username, password
  - 返回：access_token, token_type

- **GET /auth/me**：获取当前用户信息
  - 返回：用户信息

- **GET /auth/users**：获取所有用户
  - 返回：用户列表

### 交互行为模块

- **POST /video/{video_id}/like**：切换视频点赞状态
  - 参数：video_id
  - 返回：liked (是否点赞), like_count (点赞数)

- **POST /video/{video_id}/favorite**：切换视频收藏状态
  - 参数：video_id
  - 返回：favorited (是否收藏), favorite_count (收藏数)

- **POST /video/{video_id}/view**：记录视频浏览
  - 参数：video_id
  - 返回：status: "ok"

## 数据模型

### 用户模型 (User)
- id: 主键
- username: 用户名
- phone: 手机号（替换了原有的email字段）
- password_hash: 密码哈希
- role: 用户角色

### 视频模型 (Video)
- id: 主键
- title: 视频标题
- filename: 文件名
- description: 视频描述
- file_path: 视频文件路径
- cover_path: 封面路径
- created_at: 创建时间
- upload_time: 上传时间
- owner_id: 上传者ID
- target_type: 目标类型
- target_id: 目标ID

### 交互行为模型
- **VideoLike**：视频点赞记录
- **VideoFavorite**：视频收藏记录
- **VideoView**：视频浏览记录

## 安全特性

- JWT 令牌认证
- 密码哈希存储
- 文件上传安全检查
- 防止目录遍历攻击
- 测试令牌支持（开发环境）

## 部署说明

1. 安装依赖
2. 配置环境变量
3. 初始化数据库
4. 启动服务
5. 配置静态文件存储（如使用云存储）
6. 配置反向代理（如 Nginx）

## 前端对接说明

### 认证方式

- 支持标准 JWT Token 认证
- 开发环境支持测试 Token: `test-token`
- 测试 Token 会自动关联到数据库中的第一个用户

### 视频数据结构

后端返回的视频数据结构：

```json
{
  "id": 1,
  "title": "测试视频1",
  "filename": "test_video_1.mp4",
  "description": "这是第一个测试视频",
  "file_path": "https://www.w3schools.com/html/mov_bbb.mp4",
  "cover_path": null,
  "created_at": "2026-02-25T15:04:06.144479",
  "upload_time": "2026-02-25T15:04:06.144479",
  "owner_username": "testuser",
  "target_type": null,
  "target_id": null,
  "target_summary": null,
  "like_count": 0,
  "favorite_count": 0,
  "is_liked_by_me": false,
  "is_favorited_by_me": false
}
```

### 局域网访问

- 后端服务已配置为 `--host 0.0.0.0`，支持局域网访问
- 前端服务已配置为 `host: true`，支持局域网访问

## 测试数据

项目包含 `check_and_add_test_data.py` 脚本，用于：

- 检查数据库表结构
- 添加测试用户
- 添加测试视频

运行脚本：

```bash
python check_and_add_test_data.py
```

## 已知问题与解决方案

1. **前端滑动触感问题**：上下滑切换视频的触感需要优化
2. **点赞收藏更新问题**：前端点击后需要优化状态更新逻辑

## 未来扩展

- 视频转码服务
- 视频封面生成
- 视频评论系统
- 推荐算法
- 数据分析接口
- 多语言支持
- 单元测试与集成测试

## 项目状态

后端服务已完成核心功能开发，包括：
- 视频上传与管理
- 用户认证与授权
- 交互行为系统
- 数据模型设计
- API 接口实现
- 测试数据支持

可根据前端需求进行扩展和优化。
