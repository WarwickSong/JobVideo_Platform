# 本地 conda 环境验证

这份文档不是给公网服务器用的，是给你自己在本机开发环境里验证改动用的。

由于这个项目本来就是基于你自己的 `conda` 环境开发的，所以真正的运行验证应当以你的本地环境为准，而不是以沙盒环境为准。

## 这份文档解决什么问题

你现在已经有了：

- 公网部署相关配置改造
- 环境变量示例
- 部署步骤文档

但还需要确认一件事：

- 这些改动在你的本地 `conda` 环境里是否正常

## 建议验证顺序

请严格按这个顺序来。

1. 先验证后端能启动
2. 再验证前端能启动
3. 再验证前后端联通
4. 最后再验证登录、点赞、收藏

## 一、验证前先做什么

### 1. 进入项目根目录

```powershell
cd C:\Coding\JobVideo_Platform
```

### 2. 激活你的 conda 环境

把下面命令里的环境名改成你自己的：

```powershell
conda activate 你的环境名
```

### 3. 确认 Python 和 Node 是你预期的版本

```powershell
python --version
node --version
npm --version
```

如果这里就报错，先不要继续部署，先把本地环境修好。

## 二、后端验证

### 1. 进入后端目录

```powershell
cd C:\Coding\JobVideo_Platform\jobvideo_backend
```

### 2. 检查是否需要 `.env`

当前后端已经支持 `.env` 配置。

你可以先按仓库里的示例新建一个本地 `.env`：

- [jobvideo_backend/.env.example](/C:/Coding/JobVideo_Platform/jobvideo_backend/.env.example)

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

### 3. 启动后端

```powershell
uvicorn app.main:app --reload
```

### 4. 检查后端是否启动成功

浏览器打开：

```text
http://127.0.0.1:8000/docs
```

如果能打开 Swagger 页面，说明后端基本正常。

### 5. 检查几个关键接口

打开这些地址：

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/video/feed
```

如果 `video/feed` 直接报错，优先检查：

- 数据库文件是否存在
- 表结构是否完整
- `video_storage` 目录是否存在

## 三、前端验证

### 1. 新开一个终端窗口

还是先激活同一个 `conda` 环境。

### 2. 进入前端目录

```powershell
cd C:\Coding\JobVideo_Platform\jobvideo_frontend
```

### 3. 检查前端环境变量

参考：

- [jobvideo_frontend/.env.development.example](/C:/Coding/JobVideo_Platform/jobvideo_frontend/.env.development.example)

本地开发建议创建：

```text
.env.development
```

内容：

```env
VITE_API_BASE_URL=/api
VITE_DEV_BACKEND_URL=http://localhost:8000
```

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

这是这次改动的重点之一。

现在未登录用户应该也能加载 `feed`。

### 4. 点赞/收藏未登录提示

现在如果没有登录，点击点赞或收藏，应该提示：

- 点赞需要先登录
- 收藏需要先登录

### 5. 如果你想继续沿用测试 token

仅本地开发时可以：

- 确保后端 `.env` 里 `ENABLE_TEST_TOKEN=true`
- 然后你可以自己在浏览器开发者工具里写入 token

例如在浏览器控制台执行：

```javascript
localStorage.setItem('access_token', 'test-token')
```

刷新页面后，再测试点赞和收藏。

## 五、生产前必须再检查一次

正式上线前，你必须确认：

- 服务器 `.env` 中 `ENABLE_TEST_TOKEN=false`
- `FRONTEND_ORIGINS` 改成真实域名
- `SECRET_KEY` 已换成你自己的随机字符串

## 七、演示账号登录模式

当前前端已经支持演示账号登录。

页面会直接展示几个示例账号，用户可以直接点选登录，不需要先做注册功能。

但前提是后端数据库里已经存在这些账号。

### 1. 创建演示账号

先进入后端目录：

```powershell
cd C:\Coding\JobVideo_Platform\jobvideo_backend
```

然后在你自己的 `conda` 环境里执行：

```powershell
python create_demo_users.py
```

### 2. 当前内置演示账号

- `demo_seeker` / `Demo123456`
- `demo_employer` / `Demo123456`
- `demo_seeker_2` / `Demo123456`

### 3. 使用方式

启动前后端后，打开首页，左上角会出现演示登录面板。

用户只需要点击对应账号卡片，就会自动登录。

## 六、你遇到问题时发给我什么

如果某一步失败，你直接发给我下面这些信息：

1. 你执行到哪一步
2. 你执行的命令
3. 完整报错
4. 浏览器页面现象
5. 浏览器控制台报错
6. 后端终端报错

这样我可以继续精确帮你定位。
