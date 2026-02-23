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
```

## 功能特性

- **视频模块**：视频上传、视频流获取、视频详情查看
- **认证模块**：用户认证、JWT 令牌生成与验证
- **职位模块**：职位信息管理
- **简历模块**：简历信息管理
- **公司模块**：公司信息管理
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
  - 返回：视频列表，包含关联目标信息

- **GET /video/{video_id}**：获取视频详情
  - 参数：video_id
  - 返回：视频详细信息，包含关联目标完整信息

### 认证模块

- 具体接口请参考 API 文档

### 职位模块

- 具体接口请参考 API 文档

### 简历模块

- 具体接口请参考 API 文档

## 数据模型

### 用户模型 (User)
- 认证相关字段

### 视频模型 (Video)
- 视频基本信息
- 关联目标信息
- 上传者信息

### 职位模型 (Job)
- 职位基本信息
- 薪资、地点等

### 简历模型 (Resume)
- 简历基本信息
- 技能、经验等

### 公司模型 (Company)
- 公司基本信息
- 行业、规模等

## 安全特性

- JWT 令牌认证
- 密码哈希存储
- 文件上传安全检查
- 防止目录遍历攻击

## 部署说明

1. 安装依赖
2. 配置环境变量
3. 初始化数据库
4. 启动服务
5. 配置静态文件存储（如使用云存储）
6. 配置反向代理（如 Nginx）

## 未来扩展

- 视频转码服务
- 视频封面生成
- 视频评论系统
- 视频点赞系统
- 推荐算法
- 数据分析接口
- 多语言支持
- 单元测试与集成测试

## 项目状态

后端服务已完成基本功能开发，包括：
- 视频上传与管理
- 用户认证
- 基本的数据模型设计
- API 接口实现

可根据前端需求进行扩展和优化。