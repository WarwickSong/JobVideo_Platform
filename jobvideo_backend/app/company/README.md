# company 公司模块

## 数据表：companies（公司表）

| 字段 | 类型 | 约束 | 说明 | 可能的功能用途 |
|------|------|------|------|---------------|
| id | Integer | PK, Index | 公司ID | 视频绑定的 target_id（当 target_type=company_intro 时）；公司主页路由参数 |
| name | String | - | 公司名称 | 视频feed中公司介绍展示；公司搜索；品牌展示 |
| industry | String | - | 所属行业 | 按行业筛选职位/视频；行业分类推荐；行业趋势分析 |
| location | String | - | 公司地点 | 按地点筛选；地图展示；附近职位推荐 |

## 功能用途总结

### 各字段的潜在用途

- **id**: 视频绑定的 target_id（target_type=company_intro）；可扩展为公司详情页、公司相册、公司视频合集
- **name**: 职位卡片上的公司名展示；公司搜索；可扩展为公司认证、公司主页
- **industry**: 行业分类筛选；推荐相关行业的职位；行业匹配度计算
- **location**: 职位/视频的地域筛选；可扩展为地图模式、通勤时间计算

### 关联关系

```
companies  ←──  videos (target_type="company_intro" 时引用 company.id)
```

### 注意事项

- 当前模型较简单，仅包含基本信息。`resolvers.py` 中引用了一些尚未在模型中定义的字段（如 `size`、`description`、`logo`、`established_at`），如果需要使用这些字段，需先在 `models.py` 中添加
- 一个公司可以被多个视频绑定（多个视频的公司介绍）
- 公司信息目前是独立维护的，尚未与 employer 用户建立外键关联。如果后续需要"雇主管理公司资料"，可添加 `user_id` 外键
- 如果需要有"公司认证"功能，可扩展 `verified` 等字段
