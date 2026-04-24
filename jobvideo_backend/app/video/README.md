# video 视频模块

## 数据表：videos（视频表）

| 字段 | 类型 | 约束 | 说明 | 可能的功能用途 |
|------|------|------|------|---------------|
| id | Integer | PK, Index | 视频ID | 视频详情页路由；被 interactions 模块引用作为 video_id |
| title | String | Index | 视频标题 | feed 流展示；搜索；推荐展示 |
| filename | String | Unique | 视频文件名（存储用唯一名） | 文件系统定位；URL 生成 |
| description | String | - | 视频描述 | 视频详情；SEO；内容理解 |
| file_path | String | - | 视频文件存储路径/URL | 前端播放器直接使用的视频源地址 |
| cover_path | String | nullable | 封面图路径 | 视频封面展示；feed 流缩略图 |
| created_at | DateTime | - | 创建时间 | feed 流排序；"最新"标签 |
| upload_time | DateTime | - | 上传时间 | 上传时间统计；与 created_at 可区分（预留编辑场景） |
| owner_id | Integer | FK→users.id | 上传者用户ID | 区分视频归属；用户个人主页展示"TA的视频" |
| target_type | Enum(job, resume, company_intro) | nullable | 视频绑定的目标类型 | 视频分类展示；按类型筛选 feed；差异化展示绑定内容 |
| target_id | Integer | nullable | 视频绑定的目标ID | 关联到具体的职位/简历/公司记录 |

## TargetType 枚举

```
TargetType.job = "job"              ──→ 职位招聘视频
TargetType.resume = "resume"        ──→ 个人简历/求职视频
TargetType.company_intro = "company_intro"  ──→ 公司介绍视频
```

## 功能用途总结

### 各字段的潜在用途

- **id**: 被 interactions 模块的三个表（likes/favorites/views）作为外键引用；视频详情 API 参数
- **title**: 在 feed 流中作为视频标题展示；搜索关键词匹配；推荐算法特征
- **filename**: 生成视频播放 URL；保证文件唯一性（UUID 命名避免冲突）
- **description**: 视频详情页完整展示；搜索关键词匹配；AI 内容分析
- **file_path**: 前端 `<video>` 标签的 src 属性直接使用；可扩展为 CDN 地址
- **cover_path**: 视频封面的缩略图展示；feed 流中吸引点击；可扩展为自动生成封面
- **created_at / upload_time**: feed 流按时间倒序排列；推荐算法的时间衰减因子
- **owner_id**: 与 auth.users 关联；"我的视频"列表；按上传者角色（seeker/employer）过滤 feed
- **target_type**: feed 流按类型筛选（只看职位/简历/公司介绍）；不同类型展示不同的摘要卡片
- **target_id**: 视频详情页展示绑定的职位/简历/公司信息；关联数据的联动更新

### 视频与各模块的关系

```
videos
  │
  ├── owner_id ──→ auth.users
  │
  ├── target_type="job", target_id ──→ job.job_posts
  │     └── feed 中展示：职位标题、地点、薪资范围
  │
  ├── target_type="resume", target_id ──→ resume.resumes
  │     └── feed 中展示：求职意向、技能列表、经验年限
  │
  ├── target_type="company_intro", target_id ──→ company.companies
  │     └── feed 中展示：公司名称、行业、地点
  │
  ├── interactions.video_likes (video_id)
  ├── interactions.video_favorites (video_id)
  └── interactions.video_views (video_id)
```

### Feed 流数据组装逻辑

视频列表接口 `GET /video/feed` 会批量查询以下数据并组装返回：

```
视频基础信息（videos 表）
  + 上传者信息（auth.users：username, role）
  + 交互数据（interactions 三表：点赞数、收藏数、当前用户状态）
  + 目标对象摘要（job/resume/company 三选一）
  = VideoWithTarget 响应
```

批量查询策略（避免 N+1 问题）：
1. 一次性查询视频列表
2. 提取所有 video_id，批量查询点赞数/收藏数/用户状态
3. 按 target_type 分组，分别批量查询 job/resume/company
4. 在内存中组装最终数据

### 可扩展的方向

| 功能 | 需要的扩展 | 说明 |
|------|-----------|------|
| 视频分类 | 新增 category_id 字段或 Category 表 | 按分类浏览视频（代码中有注释但未启用） |
| 视频标签 | 新增 Tag 关联表 | 多标签标注；精细化推荐 |
| 视频编辑 | update_time 更新 | 编辑视频标题/描述后的时间戳更新 |
| 视频删除 | 删除接口 + 文件清理 | 同时删除数据库记录和存储文件 |
| 视频转码进度 | 新增 transcode_status 字段 | 转码状态跟踪（pending/processing/done/failed） |
| 视频时长 | 新增 duration 字段 | 视频时长展示；feed 流中的时长筛选 |
| 视频尺寸/质量 | 新增 resolution/quality 字段 | 多码率自适应播放 |
| 封面自动生成 | 扩展 cover_path | 上传时自动截取关键帧作为封面 |
| 播放列表 | 新增 Playlist 模型 | 用户创建播放列表；系列内容组织 |

### 注意事项

- `target_id` 是**泛型外键**（无 ForeignKey 约束），需要应用层保证指向的目标对象存在
- 视频上传时支持的可选绑定：一个视频可以绑定一个职位/简历/公司介绍，也可以不绑定（纯内容视频）
- 视频格式支持：`mp4`、`mov`、`avi`（上传接口校验）；实际存储 Content-Type 支持：`video/mp4`、`video/webm`、`video/quicktime`
- 视频文件保存时：先以 UUID 命名保存，再用 ffmpeg 检查编码，非 H.264+AAC 的视频会自动转码
- `file_path` 存储的是相对 URL 路径（如 `/videos/uuid.mp4`），前端直接拼接域名使用
- 分页默认每页 10 条，最大 50 条
- feed 流支持 `target_type` 和 `owner_role` 两个过滤参数
