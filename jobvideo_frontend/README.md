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
- 自动播放、循环播放视频
- 视频信息展示

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

## 组件说明

### VideoItem 组件

- 接收 `video` 对象作为 props
- 展示视频和相关信息
- 支持自动播放、静音、循环播放

### Feed 组件

- 展示视频流
- 从 API 获取视频数据
- 当前只展示单个视频，可通过扩展支持多视频切换

## 项目配置

- Vite 构建工具
- Vue 3 插件
- 响应式视频布局

## 未来扩展

- 视频切换功能
- 视频点赞、评论功能
- 用户认证系统
- 视频上传功能
- 分类筛选功能
