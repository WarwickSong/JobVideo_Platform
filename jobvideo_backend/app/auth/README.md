# auth 认证模块

## 数据表：users（用户表）

| 字段 | 类型 | 约束 | 说明 | 可能的功能用途 |
|------|------|------|------|---------------|
| id | Integer | PK, Index | 用户ID | 所有业务表的外键关联；JWT令牌中存储的用户标识 |
| username | String | Unique, Index | 用户名 | 登录凭证；个人主页URL中的标识；展示用显示名 |
| phone | String(11) | Unique, Index | 手机号 | 注册验证；登录凭证（备用）；密码找回；短信通知 |
| password_hash | String | - | 密码哈希（bcrypt加密） | 登录密码验证；注意：只存哈希，不存明文 |
| role | Enum(seeker, employer) | Default: seeker | 用户角色：求职者/雇主 | 权限控制（如 `role_required` 依赖）；按角色过滤视频feed；区分"我发布的"和"我看过的" |

## 功能用途总结

### 各字段的潜在用途

- **id**: 作为 user_id 被所有交互表（点赞、收藏、浏览）引用；视频上传者关联；职位的发布者关联
- **username**: 视频封面展示"上传者"；评论或消息中的用户标识；搜索用户
- **phone**: 可扩展为短信登录、更换手机号、手机号搜索联系人等功能
- **role**: feed流按角色过滤（只看求职者/雇主发布的视频）；区分"招聘方"和"求职方"的界面展示；分别统计两类用户的数据
- **password_hash**: 暂仅用于登录，可扩展为修改密码、OAuth绑定等功能

### 用户角色（UserRole）的用途

```
seeker (求职者)
├── 发布简历视频
├── 浏览职位视频
├── 投递简历/申请职位
└── 收藏/点赞感兴趣的职位

employer (雇主)
├── 发布职位视频
├── 浏览简历视频
├── 查看求职者资料
└── 管理招聘流程
```

### 注意事项

- `phone` 字段固定11位，仅支持中国大陆手机号格式
- 密码使用 bcrypt 加密存储，不可逆向解密
- JWT token 过期时间由 `ACCESS_TOKEN_EXPIRE_MINUTES` 配置
- 测试环境可通过 `test-token` 跳过真实认证（由 `ENABLE_TEST_TOKEN` 控制）
- `employer_id` 字段在 job 模块中使用，关联 User.id
- `owner_id` 字段在 video 模块中使用，关联 User.id
