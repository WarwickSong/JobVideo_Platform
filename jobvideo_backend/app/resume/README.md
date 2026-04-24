# resume 简历模块

## 数据表：resumes（简历表）

| 字段 | 类型 | 约束 | 说明 | 可能的功能用途 |
|------|------|------|------|---------------|
| id | Integer | PK, Index | 简历ID | 视频绑定的 target_id（当 target_type=resume 时）；简历详情页路由 |
| title | String | Index | 职位标题（求职意向） | 视频feed展示；与职位名称做匹配；搜索关键词 |
| skills | String | - | 技能列表（逗号分隔或JSON字符串） | 技能匹配度分析；技能标签展示；按技能搜索筛选 |
| experience_years | Integer | - | 工作经验年限 | 经验门槛筛选；匹配职位经验要求；按年限分类推荐 |
| major | String | - | 专业 | 专业匹配度分析；按专业分类；行业偏好推荐 |

## 功能用途总结

### 各字段的潜在用途

- **id**: 视频绑定的 target_id；可扩展为简历投递、简历管理
- **title**: 求职意向/目标职位，与 job 模块的 title 做双向匹配推荐
- **skills**: 技能关键词提取；技能标签云展示；与职位技能要求做交集/匹配度评分；可优化为独立的 Skill 表（多对多关系）
- **experience_years**: 工作经验分级（应届/1-3年/3-5年等）；匹配职位经验要求；筛选条件
- **major**: 专业对口匹配；按专业领域推荐职位；行业倾向分析

### 简历与视频的关系

```
resumes ──→ videos (target_type="resume", target_id=resumes.id)
    │                    │
    │                    └── 视频feed中展示简历摘要（title, skills, major, experience_years）
    │
    └── 当前模型未关联 user_id ──→ 可扩展关联 users.id (seeker角色)
```

### 可扩展的方向

| 功能 | 需要的扩展 | 说明 |
|------|-----------|------|
| 关联用户 | 新增 user_id 外键→users.id | 简历归属用户；"我的简历"管理（当前模型尚无用户关联） |
| 个人简介 | 新增 self_introduction/text 字段 | 自我介绍展示（resolvers.py 已引用，但 models.py 尚无） |
| 教育经历 | 新增 education 字段或 Education 表 | 学历背景展示（resolvers.py 已引用，但 models.py 尚无） |
| 描述/详情 | 新增 description/text 字段 | 详细简历内容（resolvers.py 已引用，但 models.py 尚无） |
| 创建时间 | 新增 created_at 字段 | 简历时效性（resolvers.py 已引用，但 models.py 尚无） |
| 技能结构化 | 新建 Skill 表 + 多对多关系 | 支持技能标签管理、按技能精确搜索 |
| 工作经历 | 新增 WorkExperience 模型 | 多段工作经历的详细描述 |
| 项目经历 | 新增 ProjectExperience 模型 | 项目作品的详细展示 |
| 期望薪资 | 新增 expected_salary 字段 | 与职位薪资范围做匹配 |
| 简历状态 | 新增 status 字段 | 公开/私密/已投递等状态管理 |
| 简历文件 | 新增 file_path 字段 | 上传 PDF/Word 格式简历附件 |

### 注意事项

- `resolvers.py` 中引用了 `description`、`education`、`self_introduction`、`created_at` 等字段，但这些在当前的 `models.py` 中尚未定义。如果需要完整的简历解析功能，需要先在 `models.py` 中添加这些字段
- `skills` 目前是用逗号分隔的字符串存储（如 "Python,Java,SQL"），查询时需用 `split(",")` 解析。如果后续有按技能筛选的需求，建议改为独立的 Skill 表
- 当前 resume 模块的 `routes.py` 是空的，尚未实现任何 API 接口。需要补充 CRUD 接口
- 当前简历模型没有关联到具体的用户（缺少 `user_id` 外键），这是最优先需要补充的字段，否则无法实现"我的简历"功能
- 如果实现"简历投递"功能，需要新增一个关联 job_posts 和 resumes 的中间表（或 Application 模型）
