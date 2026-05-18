# 配置 Nginx 与 HTTPS

## 目标

让用户通过域名访问：

- `/` 打开前端页面
- `/api` 访问后端
- `/videos` 访问视频文件

当前目标域名是：

```text
zhenzhao.top
www.zhenzhao.top
```

## 1. 创建 Nginx 配置

创建文件：

```bash
sudo vim /etc/nginx/sites-available/zhenzhao.top
```

写入这份内容：

```nginx
server {
    listen 80;
    server_name zhenzhao.top www.zhenzhao.top;

    root /var/www/zhenzhao.top/frontend-dist;
    index index.html;

    client_max_body_size 200m;

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

- `root` 指向 `/var/www/zhenzhao.top/frontend-dist`
- `/api/` 的 `proxy_pass` 末尾必须有 `/`
- `/videos/` 的 `alias` 指向 `/var/www/zhenzhao.top/video_storage/`
- `client_max_body_size 200m` 用于支持视频上传

## 2. 启用站点

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

如果 `nginx -t` 报错，不要继续，先处理 Nginx 配置错误。

## 3. 先验证 HTTP

浏览器打开：

```text
http://zhenzhao.top
```

也可以检查接口代理：

```bash
curl http://zhenzhao.top/api/video/feed
```

## 4. 申请 HTTPS

确认域名 DNS 已解析到 `124.220.216.17` 后执行：

```bash
sudo certbot --nginx -d zhenzhao.top -d www.zhenzhao.top
```

过程中按提示操作即可。

## 5. 申请成功后验证

浏览器打开：

```text
https://zhenzhao.top
```

接口检查：

```bash
curl https://zhenzhao.top/api/video/feed
```

## 6. 自动续期测试

```bash
sudo certbot renew --dry-run
```

如果这一条通过，说明续期机制基本没问题。
