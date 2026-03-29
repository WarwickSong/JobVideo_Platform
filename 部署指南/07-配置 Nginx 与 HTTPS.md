# 配置 Nginx 与 HTTPS

## 目标

让用户通过域名访问：

- `/` 打开前端页面
- `/api` 访问后端
- `/videos` 访问视频文件

## 1. 创建 Nginx 配置

创建文件：

```text
/etc/nginx/sites-available/jobvideo
```

先写入这份内容：

```nginx
server {
    listen 80;
    server_name 你的域名 www.你的域名;

    root /var/www/jobvideo/frontend-dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /videos/ {
        alias /var/www/jobvideo/video_storage/;
        access_log off;
        expires 7d;
    }
}
```

## 2. 启用站点

```bash
sudo ln -s /etc/nginx/sites-available/jobvideo /etc/nginx/sites-enabled/jobvideo
sudo nginx -t
sudo systemctl reload nginx
```

如果 `nginx -t` 报错，不要继续，先把错误发给我。

## 3. 先验证 HTTP

浏览器打开：

```text
http://你的域名
```

如果页面能打开，说明 Nginx 基本通了。

## 4. 申请 HTTPS

```bash
sudo certbot --nginx -d 你的域名 -d www.你的域名
```

过程中按提示操作即可。

## 5. 申请成功后验证

浏览器打开：

```text
https://你的域名
```

## 6. 自动续期测试

```bash
sudo certbot renew --dry-run
```

如果这一条通过，说明续期机制基本没问题。
