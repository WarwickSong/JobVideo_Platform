# 本地开发环境验证（conda 可选）

这份文档不是给公网服务器用的，是给你自己在本机开发环境里验证改动用的。

当前结论：

- 云服务器部署不需要安装 conda，使用 Python 自带 `.venv` 即可
- 本地如果你已经习惯用 conda，可以继续用 conda 验证
- 本地如果不用 conda，也可以用 Python `venv` 验证

## 这份文档解决什么问题

你现在已经有了：

- 公网部署相关配置
- 环境变量配置方式
- 云服务器部署步骤
- 前端演示登录面板

还需要确认：

- 后端能启动
- 前端能启动
- 前后端联通正常
- 视频流、视频播放、演示登录、点赞收藏行为正常

## 建议验证顺序

请按这个顺序来。

1. 先验证后端能启动
2. 再验证前端能启动
3. 再验证前后端联通
4. 最后再验证登录、点赞、收藏

## 一、验证前先做什么

### 1. 进入项目根目录

```powershell
cd C:\Coding\JobVideo_Platform
```

### 2. 选择本地 Python 环境

如果你使用 conda：

```powershell
conda activate jobvideo-backend
```

如果你使用 venv：

```powershell
cd C:\Coding\JobVideo_Platform\jobvideo_backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. 确认 Python 和 Node 版本

```powershell
python --version
node --version
npm --version
```

当前前端使用 Vite 7，本地 Node.js 也建议使用 20.19+ 或 22.12+。

## 二、后端验证

### 1. 进入后端目录

```powershell
cd C:\Coding\JobVideo_Platform\jobvideo_backend
```

### 2. 安装后端依赖

```powershell
pip install -r requirements.txt
```

### 3. 检查是否需要 `.env`

当前后端支持 `.env` 配置。

本地开发建议内容：

```env
APP_ENV=development
SECRET_KEY=dev-secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
DATABASE_URL=sqlite:///./test.db
VIDEO_STORAGE_DIR=video_storage
FRONTEND_ORIGINS=http://localhost:5173
ENABLE_TEST_TOKEN=true
```

### 4. 启动后端

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. 检查后端是否启动成功

浏览器打开：

```text
http://127.0.0.1:8000/docs
```

也可以检查：

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/video/feed
```

如果 `video/feed` 报错，优先检查：

- 数据库文件是否存在
- 表结构是否完整
- `video_storage` 目录是否存在

## 三、前端验证

### 1. 新开一个终端窗口

如果你使用 conda，可以激活同一个环境；如果只是跑前端，通常只需要 Node.js/npm。

```powershell
cd C:\Coding\JobVideo_Platform\jobvideo_frontend
```

### 2. 安装前端依赖

```powershell
npm ci
```

如果失败，再使用：

```powershell
npm install
```

### 3. 检查前端环境变量

本地开发建议创建：

```text
.env.development
```

内容：

```env
VITE_API_BASE_URL=/api
VITE_DEV_BACKEND_URL=http://localhost:8000
```

如果你要用手机访问局域网地址，可以把 `localhost` 换成你的电脑局域网 IP。

### 4. 启动前端

```powershell
npm run dev
```

### 5. 打开前端页面

```text
http://localhost:5173
```

## 四、联调验证

页面打开后，请按这个顺序验证。

### 1. 视频流是否能正常显示

你应该能看到：

- 视频画面
- 标题
- 右侧操作区

### 2. 视频是否能播放

如果页面打开但视频不播放，优先检查：

- `file_path` 是否正确
- `/videos/...` 路径是否能访问
- 视频文件是否真实存在

### 3. 未登录状态是否能浏览

未登录用户应该也能加载 `feed`。

### 4. 点赞/收藏未登录提示

如果没有登录，点击点赞或收藏，应该提示需要先登录。

### 5. 演示账号登录

当前前端支持演示账号登录。

先进入后端目录创建演示账号：

```powershell
cd C:\Coding\JobVideo_Platform\jobvideo_backend
python create_demo_users.py
```

当前内置演示账号：

- `demo_seeker` / `Demo123456`
- `demo_employer` / `Demo123456`
- `demo_seeker_2` / `Demo123456`

启动前后端后，打开首页，左上角会出现演示登录面板。

## 五、生产前必须再检查一次

正式上线前，服务器 `.env` 必须确认：

```env
APP_ENV=production
FRONTEND_ORIGINS=https://zhenzhao.top,https://www.zhenzhao.top
ENABLE_TEST_TOKEN=false
```

同时：

- `SECRET_KEY` 已换成随机字符串
- `VIDEO_STORAGE_DIR=/var/www/zhenzhao.top/video_storage`
- 前端 `.env.production` 中 `VITE_API_BASE_URL=/api`
- Nginx `/api/` 能正确转发到后端 `/video/feed`

## 六、遇到问题时发给我什么

如果某一步失败，直接发给我下面这些信息：

1. 你执行到哪一步
2. 你执行的命令
3. 完整报错
4. 浏览器页面现象
5. 浏览器控制台报错
6. 后端终端报错
