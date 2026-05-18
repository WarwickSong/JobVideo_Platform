# JobVideo_Platform 云服务器部署指南

## 项目信息

- **项目名称**：JobVideo_Platform
- **服务器环境**：Ubuntu 24.04 LTS
- **域名**：zhenzhao.top
- **服务器 IP**：124.220.216.17
- **部署根目录**：`/var/www/zhenzhao.top`
- **项目源码目录**：`/var/www/zhenzhao.top/app`
- **前端静态目录**：`/var/www/zhenzhao.top/frontend-dist`
- **视频存储目录**：`/var/www/zhenzhao.top/video_storage`
- **数据库目录**：`/var/www/zhenzhao.top/data`

## 第一阶段：环境准备

### 1.1 更新系统并安装基础工具

```bash
sudo apt update
sudo apt install -y curl wget git vim unzip lsof net-tools nginx python3 python3-venv python3-pip certbot python3-certbot-nginx ffmpeg
```

### 1.2 安装 Node.js

当前前端使用 Vite 7，要求 Node.js `^20.19.0` 或 `>=22.12.0`。建议安装 Node.js 22 LTS。

```bash
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt-get install -y nodejs
node --version
npm --version
```

不需要安装 Vue CLI，因为这个项目使用 Vite，不是 Vue CLI 项目。

### 1.3 启动 Nginx

```bash
sudo systemctl start nginx
sudo systemctl enable nginx
sudo systemctl status nginx
```

## 第二阶段：上传或拉取代码

### 2.1 创建部署目录

```bash
sudo mkdir -p /var/www/zhenzhao.top
sudo chown -R $USER:$USER /var/www/zhenzhao.top
cd /var/www/zhenzhao.top
mkdir -p frontend-dist video_storage data logs
```

### 2.2 拉取项目代码

如果你已经有 Git 仓库，推荐把整个 `JobVideo_Platform` 作为一个仓库拉取到服务器：

```bash
cd /var/www/zhenzhao.top
git clone <你的 JobVideo_Platform 仓库地址> app
```

拉取后目录应类似：

```text
/var/www/zhenzhao.top/app/jobvideo_backend
/var/www/zhenzhao.top/app/jobvideo_frontend
```

如果你不是用 Git，而是手动上传，也要保证上传后的目录结构与上面一致。

`data` 和 `video_storage` 不放在源码目录里，后续 `git pull` 或重新上传代码时不容易误覆盖运行数据。

## 第三阶段：部署后端 FastAPI

### 3.1 进入后端目录

```bash
cd /var/www/zhenzhao.top/app/jobvideo_backend
```

### 3.2 创建虚拟环境并安装依赖

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 3.3 创建生产环境配置 `.env`

在 `/var/www/zhenzhao.top/app/jobvideo_backend/.env` 写入：

```env
APP_ENV=production
SECRET_KEY=请替换成你自己的长随机字符串
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
DATABASE_URL=sqlite:////var/www/zhenzhao.top/data/jobvideo.db
VIDEO_STORAGE_DIR=/var/www/zhenzhao.top/video_storage
FRONTEND_ORIGINS=https://zhenzhao.top,https://www.zhenzhao.top
ENABLE_TEST_TOKEN=false
```

可以用下面命令生成随机密钥：

```bash
openssl rand -hex 32
```

### 3.4 准备视频存储目录权限

```bash
sudo mkdir -p /var/www/zhenzhao.top/video_storage /var/www/zhenzhao.top/data
sudo chown -R $USER:$USER /var/www/zhenzhao.top/video_storage /var/www/zhenzhao.top/data
sudo chmod -R 755 /var/www/zhenzhao.top/video_storage
sudo chmod 750 /var/www/zhenzhao.top/data
```

### 3.5 手动测试后端启动

```bash
cd /var/www/zhenzhao.top/app/jobvideo_backend
source .venv/bin/activate
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

新开一个终端检查：

```bash
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/video/feed
```

能返回 JSON 说明后端基础启动正常。测试完成后按 `Ctrl+C` 停止手动启动的服务。

### 3.6 创建 systemd 后端服务

创建服务文件：

```bash
sudo vim /etc/systemd/system/zhenzhao-backend.service
```

写入以下内容。如果服务器用户名不是 `ubuntu`，把 `User=ubuntu`、`Group=ubuntu` 改成你的实际用户名。

```ini
[Unit]
Description=JobVideo FastAPI Backend
After=network.target

[Service]
Type=simple
User=ubuntu
Group=ubuntu
WorkingDirectory=/var/www/zhenzhao.top/app/jobvideo_backend
EnvironmentFile=/var/www/zhenzhao.top/app/jobvideo_backend/.env
ExecStart=/var/www/zhenzhao.top/app/jobvideo_backend/.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl daemon-reload
sudo systemctl enable zhenzhao-backend
sudo systemctl start zhenzhao-backend
sudo systemctl status zhenzhao-backend
```

查看日志：

```bash
sudo journalctl -u zhenzhao-backend -n 100 --no-pager
```

## 第四阶段：部署前端 Vue + Vite

### 4.1 进入前端目录

```bash
cd /var/www/zhenzhao.top/app/jobvideo_frontend
```

### 4.2 安装依赖

项目有 `package-lock.json`，生产构建建议使用：

```bash
npm ci
```

如果 `npm ci` 因锁文件问题失败，再改用：

```bash
npm install
```

### 4.3 创建前端生产环境配置

在 `/var/www/zhenzhao.top/app/jobvideo_frontend/.env.production` 写入：

```env
VITE_API_BASE_URL=/api
```

这样浏览器请求 `/api/video/feed` 时，会先到 Nginx，再由 Nginx 转发到后端真实接口 `/video/feed`。

### 4.4 构建并发布静态文件

```bash
npm run build
rm -rf /var/www/zhenzhao.top/frontend-dist/*
cp -r dist/* /var/www/zhenzhao.top/frontend-dist/
```

## 第五阶段：配置 Nginx

### 5.1 创建站点配置

```bash
sudo vim /etc/nginx/sites-available/zhenzhao.top
```

写入：

```nginx
server {
    listen 80;
    server_name zhenzhao.top www.zhenzhao.top;

    root /var/www/zhenzhao.top/frontend-dist;
    index index.html;

    client_max_body_size 500m;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8000/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300s;
        proxy_send_timeout 300s;
    }

    location /videos/ {
        alias /var/www/zhenzhao.top/video_storage/;
        access_log off;
        expires 7d;
        add_header Cache-Control "public";
    }

    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|webp)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
        try_files $uri =404;
    }
}
```

关键点：

- `proxy_pass http://127.0.0.1:8000/;` 末尾必须有 `/`，这样 `/api/video/feed` 才会转成后端的 `/video/feed`
- `/videos/` 指向 `VIDEO_STORAGE_DIR`，用于访问上传后的视频文件
- `client_max_body_size 500m` 与后端默认 500MB 上传限制保持一致，避免 Nginx 先拦截大视频
- `proxy_read_timeout` 和 `proxy_send_timeout` 用于给视频上传、转码等较慢请求留出更长时间

### 5.2 启用站点

```bash
sudo ln -s /etc/nginx/sites-available/zhenzhao.top /etc/nginx/sites-enabled/zhenzhao.top
sudo nginx -t
sudo systemctl reload nginx
```

如果默认站点占用了配置，可以禁用默认站点：

```bash
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx
```

### 5.3 可选：未备案时使用 IP + 8080 做临时测试

在腾讯云中国境内服务器上，未备案域名访问可能会被云厂商拦截，并且不一定只拦截 `80` 或 `443`。实践中，`http://zhenzhao.top:8080` 也可能提示“网站未完成备案”。

因此，`8080` 不能作为绕过备案的域名访问方案，只适合作为临时测试入口：

```text
http://124.220.216.17:8080
http://124.220.216.17:8080/api/video/feed
```

端口说明：

- `80`：HTTP 默认端口，对应 `http://zhenzhao.top`
- `443`：HTTPS 默认端口，对应 `https://zhenzhao.top`
- `8000`：后端服务内部端口，本指南中只监听 `127.0.0.1:8000`，不直接暴露到公网
- `8080`：临时 HTTP 测试端口，建议配合服务器公网 IP 使用

如果要使用 IP + 8080 临时测试，可以让 Nginx 监听 `8080`，后端仍然保持 `127.0.0.1:8000` 不变。

把站点配置里的：

```nginx
listen 80;
```

临时改成：

```nginx
listen 8080;
```

然后检查并重载 Nginx：

```bash
sudo nginx -t
sudo systemctl reload nginx
```

还需要在云服务器安全组、防火墙中放行 `8080` 端口。如果服务器启用了 `ufw`，执行：

```bash
sudo ufw allow 8080/tcp
sudo ufw status
```

此时优先使用公网 IP 访问：

```text
http://124.220.216.17:8080
http://124.220.216.17:8080/api/video/feed
```

如果访问 `http://zhenzhao.top:8080` 提示“网站未完成备案”，说明腾讯云已经按域名进行备案拦截，需要完成备案、使用已备案域名、切换到中国境外服务器，或者临时用公网 IP 测试。

使用 IP + 8080 时，前端 `.env.production` 仍然可以保持：

```env
VITE_API_BASE_URL=/api
```

因为前端页面和接口都走同一个 `http://124.220.216.17:8080` 来源，浏览器请求 `/api` 会继续由 Nginx 转发到本机后端 `127.0.0.1:8000`。

## 第六阶段：配置 HTTPS

确认域名 DNS 已解析到服务器 IP `124.220.216.17`，并且服务器允许使用 `443` 端口后执行：

```bash
sudo certbot --nginx -d zhenzhao.top -d www.zhenzhao.top
sudo certbot renew --dry-run
```

如果当前没有配置 HTTPS，或者 `443` 端口暂时不可用，第七阶段检查时先使用 `http://zhenzhao.top`。如果域名未备案被拦截，则临时使用 `http://124.220.216.17:8080` 做功能测试。

## 第七阶段：上线检查

### 7.1 检查服务状态

```bash
sudo systemctl status nginx
sudo systemctl status zhenzhao-backend
sudo ss -tlnp | grep -E '(:80|:443|:8000|:8080)'
```

### 7.2 检查后端接口

如果已经配置 HTTPS：

```bash
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/video/feed
curl https://zhenzhao.top/api/video/feed
```

如果暂时使用 HTTP 或 IP + 8080：

```bash
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/video/feed
curl http://zhenzhao.top/api/video/feed
curl http://124.220.216.17:8080/api/video/feed
```

### 7.3 检查前端页面

浏览器打开：

```text
https://zhenzhao.top
```

如果暂时使用 HTTP 或 IP + 8080，打开：

```text
http://zhenzhao.top
http://124.220.216.17:8080
```

如果前端能打开，并且视频流接口不再报错，说明部署链路基本正常。

### 7.4 检查日志

```bash
sudo journalctl -u zhenzhao-backend -f
sudo tail -f /var/log/nginx/error.log
```

## 第八阶段：后续更新流程

### 8.1 更新后端

```bash
cd /var/www/zhenzhao.top/app
git pull
cd jobvideo_backend
source .venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart zhenzhao-backend
```

### 8.2 更新前端

```bash
cd /var/www/zhenzhao.top/app/jobvideo_frontend
npm ci
npm run build
rm -rf /var/www/zhenzhao.top/frontend-dist/*
cp -r dist/* /var/www/zhenzhao.top/frontend-dist/
sudo systemctl reload nginx
```

## 常见问题

### 后端服务启动失败

```bash
sudo journalctl -u zhenzhao-backend -n 100 --no-pager
```

重点检查：

- `WorkingDirectory` 是否是 `/var/www/zhenzhao.top/app/jobvideo_backend`
- `ExecStart` 是否使用 `.venv/bin/uvicorn app.main:app`
- `.env` 是否存在
- `VIDEO_STORAGE_DIR` 目录是否存在且有写入权限

### 前端接口 404

优先检查 Nginx 的 `/api/` 配置：

```nginx
location /api/ {
    proxy_pass http://127.0.0.1:8000/;
}
```

这里 `proxy_pass` 末尾的 `/` 很重要。没有这个 `/` 时，请求可能会被转发成 `/api/video/feed`，但后端实际接口是 `/video/feed`。

### 视频无法播放

检查：

```bash
ls -lah /var/www/zhenzhao.top/video_storage
curl -I https://zhenzhao.top/videos/某个视频文件名.mp4
```

如果文件存在但无法访问，重点检查 Nginx 的 `/videos/` `alias` 配置和目录权限。

### 上传视频失败

检查 Nginx 是否配置了：

```nginx
client_max_body_size 500m;
```

当前后端默认允许最大 500MB 视频，Nginx 也建议保持为 `500m`。

## 与原指南相比必须改动的地方

1. **后端启动命令必须改**：不能用 `python app.py`，应使用 `uvicorn app.main:app --host 127.0.0.1 --port 8000`
2. **目录结构必须改**：项目不是前后端两个独立仓库，而是一个仓库下的 `jobvideo_backend` 和 `jobvideo_frontend`
3. **Node.js 版本建议改**：Vite 7 要求 Node.js 20.19+ 或 22.12+，原来的 Node.js 18 不适合
4. **Nginx `/api/` 代理必须改**：需要去掉 `/api` 前缀，否则前端请求无法匹配后端真实路由
5. **需要增加 `/videos/` 配置**：项目有视频存储与播放需求，不能只配置前端静态文件和 API
6. **需要增加 `.env` 生产配置**：特别是 `APP_ENV=production`、`FRONTEND_ORIGINS`、`VIDEO_STORAGE_DIR`、`ENABLE_TEST_TOKEN=false`
7. **不需要安装 Vue CLI、Flask、Django、Gunicorn**：当前项目没有使用这些组件
