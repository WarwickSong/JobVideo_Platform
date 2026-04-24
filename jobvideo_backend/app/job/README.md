# job 职位模块

## 数据表：job_posts（职位表）

| 字段 | 类型 | 约束 | 说明 | 可能的功能用途 |
|------|------|------|------|---------------|
| id | Integer | PK, Index | 职位ID | 视频绑定的 target_id（当 target_type=job 时）；职位详情页路由 |
| title | String | Index | 职位标题 | 视频feed中展示；关键词搜索；推荐匹配 |
| description | Text | - | 职位描述 | 职位详情页展示；AI 解析提取关键词；JD 匹配度分析 |
| salary_min | Float | nullable | 最低薪资 | 薪资筛选范围；职位卡片展示；按薪资排序 |
| salary_max | Float | nullable | 最高薪资 | 薪资筛选范围；职位卡片展示；按薪资排序 |
| location | String | nullable | 工作地点 | 地域筛选；通勤距离计算；地图展示 |
| status | Enum(open, closed) | Default: open | 职位状态：招聘中/已关闭 | feed 流只展示 open 的职位；已关闭的自动隐藏；招聘进度管理 |
| created_at | DateTime | - | 创建时间 | 按发布时间排序；"最新发布"标签 |
| employer_id | Integer | FK→users.id | 发布职位的雇主ID | 雇主管理自己的职位列表；区分"我发布的"职位 |

## 功能用途总结

### 各字段的潜在用途

- **id**: 视频绑定的 target_id；可扩展为职位申请/投递功能
- **title**: 与简历 title 做匹配推荐；搜索关键词；feed 流卡片标题
- **description**: AI 提取技能要求、经验要求、学历要求；与简历做匹配度评分
- **salary_min / salary_max**: 薪资范围筛选；与求职者期望薪资匹配；薪资分布统计
- **location**: 根据用户位置推荐附近职位；通勤时间计算
- **status**: 控制职位的可见性（已关闭的职位不在 feed 展示）
- **created_at**: 新职位优先展示；"7日内新发布"等时间标签
- **employer_id**: 与 auth.users 关联，区分发布者；雇主后台管理

### 职位与视频的关系

```
job_posts ──→ videos (target_type="job", target_id=job_posts.id)
     │                    │
     │                    └── 视频feed中展示职位摘要（title, location, salary）
     │
     └── employer_id ──→ users.id (角色为 employer 的用户)
```

### 可扩展的方向

| 功能 | 需要的扩展 | 说明 |
|------|-----------|------|
| 职位申请 | 新增 Application 模型 | 关联 job_id + user_id(seeker)，记录投递状态 |
| 技能要求 | 新增 skills 字段或 Skill 表 | 精细化的技能匹配（当前 models.py 中尚无） |
| 学历要求 | 新增 education 字段 | 学历门槛过滤（resolvers.py 已引用，但 models.py 尚无） |
| 经验要求 | 新增 experience_years 字段 | 经验年限过滤（resolvers.py 已引用，但 models.py 尚无） |
| 职位分类 | 新增 category_id 字段或 Category 表 | 按行业/职能分类浏览 |
| 公司关联 | 新增 company_id 外键 | 职位归属于公司（当前只有 employer_id） |
| 投递数量限制 | 新增 max_applications 字段 | 控制职位接收的简历数量 |

### 注意事项

- `resolvers.py` 中引用了 `experience_years`、`education`、`skills`、`posted_at` 等字段，但这些在当前的 `models.py` 中尚未定义。如果需要完整的职位解析功能，需要先在 `models.py` 中添加这些字段
- 搜索功能目前只支持按 title 模糊搜索（`ilike`），可扩展为全文搜索或 ES 搜索引擎
- 薪资字段为 Float 类型，可考虑用 Integer 存储（以千元为单位）避免浮点精度问题
- employer_id 外键未设置级联删除策略，删除用户时需注意
