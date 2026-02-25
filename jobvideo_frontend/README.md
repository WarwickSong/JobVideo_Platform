# JobVideo 前端平台

这是一个基于 Vue 3 + Vite 开发的求职视频平台前端项目。

## 项目结构

```
src/
├── api/           # API 调用相关
│   └── video.js   # 视频相关 API
├── components/    # 组件
│   └── VideoItem.vue  # 视频项组件
├── views/         # 页面视图
│   └── Feed.vue   # 视频流页面
├── App.vue        # 根组件
├── main.js        # 入口文件
└── style.css      # 全局样式
```

## 功能特性

- 使用 Vue 3 组合式 API (<script setup>)
- 视频流展示
- 上下滑切换视频功能
- 自动播放、循环播放视频
- 视频信息展示
- 视频点赞和收藏功能
- 实时显示点赞数和收藏数

## 技术栈

- Vue 3.5.25
- Vite 7.3.1
- Axios 1.13.5

## 安装与运行

### 安装依赖

```bash
npm install
```

### 开发环境运行

```bash
npm run dev
```

### 构建生产版本

```bash
npm run build
```

### 预览生产构建

```bash
npm run preview
```

## API 调用

项目使用 Axios 进行 API 调用，主要接口：

- `fetchVideoFeed()`: 获取视频流数据
- `toggleVideoLike(videoId)`: 切换视频点赞状态
- `toggleVideoFavorite(videoId)`: 切换视频收藏状态

## 组件说明

### VideoItem 组件

- 接收 `video` 对象作为 props
- 展示视频和相关信息
- 支持自动播放、静音、循环播放
- 显示视频标题和目标信息
- 包含点赞、收藏、分享按钮
- 实时更新点赞数和收藏数

### Feed 组件

- 展示视频流
- 从 API 获取视频数据
- 实现上下滑切换视频功能
- 支持向上滑看下一个视频
- 支持向下滑看上一个视频

## 项目配置

- Vite 构建工具
- Vue 3 插件
- 响应式视频布局
- 局域网访问支持 (`host: true`)
- API 代理配置

## 接口对接说明

### 后端 API 地址

- 开发环境: `http://localhost:8000`
- 接口前缀: `/api` (通过 Vite 代理自动转发)

### 认证方式

- 使用 JWT Token 认证
- 当前使用测试 Token: `test-token`
- 后端已支持测试 Token 直接登录

### 视频数据结构

前端期望的视频数据结构：

```javascript
{
  id: Number,           // 视频ID
  title: String,        // 视频标题
  filename: String,     // 文件名
  description: String,  // 视频描述
  file_path: String,    // 视频文件路径
  cover_path: String,   // 封面路径
  created_at: String,   // 创建时间
  upload_time: String,  // 上传时间
  owner_username: String, // 上传者用户名
  target_type: String,  // 目标类型
  target_id: Number,    // 目标ID
  target_summary: Object, // 目标摘要信息
  like_count: Number,   // 点赞数
  favorite_count: Number, // 收藏数
  is_liked_by_me: Boolean, // 当前用户是否点赞
  is_favorited_by_me: Boolean // 当前用户是否收藏
}
```

## 已知问题

1. **滑动触感问题**：上下滑的触感有点怪，有时感觉像是左右滑才有用
2. **点赞收藏更新问题**：点击点赞和收藏按钮后，数字会消失但不会立即显示更新后的数量

## 未来扩展

- 视频评论系统
- 用户认证和登录界面
- 视频上传功能
- 个人中心页面
- 视频分类和搜索功能
