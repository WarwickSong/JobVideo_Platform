# interactions 交互行为模块

## 数据表

### 1. video_views（视频浏览记录表）— 事件表

| 字段 | 类型 | 约束 | 说明 | 可能的功能用途 |
|------|------|------|------|---------------|
| id | BigInteger | PK, Index | 记录ID | 大数据量支持；浏览记录分页 |
| video_id | Integer | FK→videos.id, Index, CASCADE | 被浏览的视频ID | 统计视频总浏览量；热门视频排序 |
| user_id | Integer | FK→users.id, nullable, Index | 浏览者用户ID（支持未登录） | 用户浏览历史；个性化推荐依据 |
| created_at | DateTime(timezone) | Index | 浏览时间 | 浏览时间线展示；"最近浏览"功能；时间段热度分析 |

### 2. video_likes（视频点赞表）— 状态表

| 字段 | 类型 | 约束 | 说明 | 可能的功能用途 |
|------|------|------|------|---------------|
| id | Integer | PK, Index | 记录ID | - |
| video_id | Integer | FK→videos.id, Index, CASCADE | 被点赞的视频ID | 统计视频点赞数；热门/优质内容排序 |
| user_id | Integer | FK→users.id, Index, CASCADE | 点赞用户ID | 用户点赞列表；"我赞过的"功能 |
| created_at | DateTime(timezone) | - | 点赞时间 | 按时间排序的点赞列表 |
| **唯一约束** | (video_id, user_id) | `uniq_video_like` | 防止重复点赞 | toggle 逻辑的基础（存在=已赞，不存在=未赞） |

### 3. video_favorites（视频收藏表）— 状态表

| 字段 | 类型 | 约束 | 说明 | 可能的功能用途 |
|------|------|------|------|---------------|
| id | Integer | PK, Index | 记录ID | - |
| video_id | Integer | FK→videos.id, Index, CASCADE | 被收藏的视频ID | 统计视频收藏数；热门/优质内容排序 |
| user_id | Integer | FK→users.id, Index, CASCADE | 收藏用户ID | 用户收藏列表；"我的收藏"功能 |
| created_at | DateTime(timezone) | - | 收藏时间 | 按时间排序的收藏列表 |
| **唯一约束** | (video_id, user_id) | `uniq_video_favorite` | 防止重复收藏 | toggle 逻辑的基础（存在=已收，不存在=未收） |

## 功能用途总结

### 各表的定位

```
事件表（Event Table）：记录每次行为，不做去重
  └── video_views ──→ 适合做统计分析、推荐算法

状态表（State Table）：记录当前状态，做去重
  ├── video_likes ──→ 适合做"是否已赞"判断、计数
  └── video_favorites ──→ 适合做"是否已收"判断、计数
```

### 各字段的潜在用途

#### video_id（三个表共有）
- 视频详情页显示点赞数、收藏数、浏览量
- 热门视频排行榜（按点赞/收藏/浏览综合排序）
- 推荐算法的正反馈信号（点赞/收藏是强信号，浏览是弱信号）
- 视频创作者的数据面板

#### user_id（三个表共有）
- "我的"模块：我的点赞、我的收藏、浏览历史
- 用户行为画像：分析用户偏好标签
- 协同过滤推荐："看过这个视频的人也看了..."
- 防止重复推荐：已交互的视频不再推荐

#### created_at
- 时间线展示
- 热度衰减计算（新近的交互权重更高）
- 用户活跃时间段分析

### 可扩展的方向

| 功能 | 需要的扩展 | 可复用的字段/逻辑 |
|------|-----------|------------------|
| 评论系统 | 新增 Comment 模型 | 复用 video_id + user_id 关联模式 |
| 分享计数 | 新增 Share 模型或字段 | 复用事件表模式（不做去重） |
| 举报/拉黑 | 新增 Report/Block 模型 | 复用唯一约束模式 |
| 关注关系 | 新增 Follow 模型 | 复用状态表模式（(follower_id, followee_id)唯一约束） |
| 踩/不喜欢 | 新增 dislike 字段或表 | 复用 video_likes 的 toggle 逻辑 |
| 播放进度 | 新增 progress 字段 | 复用 video_views 的浏览记录 |

### 注意事项

- `video_views` 使用 BigInteger 主键，因为浏览记录量大
- `video_views` 中 `user_id` 可为空（支持未登录用户浏览）
- `video_likes` 和 `video_favorites` 的 `user_id` 不可为空（需要登录）
- 三个表的外键都设置了 `ON DELETE CASCADE`，视频/用户删除后关联记录自动删除
- 点赞和收藏是独立的操作，互不影响
- 在 `video/routes.py` 的 feed 接口中，使用批量查询（batch query）避免 N+1 问题
