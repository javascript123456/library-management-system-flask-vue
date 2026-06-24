# 图书管理系统 - 项目规格说明书

## 1. 项目概述

**项目名称**：图书管理系统（Library Management System）
**项目类型**：前后端分离的 Web 应用
**核心功能**：对图书馆的图书进行数字化管理，包括图书的增删改查、借阅归还、用户管理、数据统计和 AI 智能服务。
**目标用户**：图书馆管理员、普通读者

## 2. 技术栈

- **后端**：Python Flask 2.x + Flask-SQLAlchemy + Flask-CORS
- **数据库**：MySQL 8.0
- **前端**：Vue 3 (Composition API) + Vite + Axios + Element Plus + Pinia
- **认证**：JWT（JSON Web Token）
- **AI**：阿里云百炼千问（qwen-max）+ 协同过滤推荐算法

## 3. 功能模块

### 3.1 用户管理
- 用户注册、登录、登出
- 管理员与普通用户角色区分
- 个人信息查看
- JWT token 认证

### 3.2 图书管理（管理员）
- 图书增加（ISBN、书名、作者、出版社、分类、库存数量、封面图）
- 图书列表查看（分页、搜索、分类筛选）
- 图书信息编辑
- 图书删除（物理删除）
- AI 简介生成（千问大模型，自动缓存到 description 字段）

### 3.3 借阅管理
- 读者借书（按图书 ID + 读者 ID，记录借阅日期，自动计算应还日期）
- 查看借阅记录（全部 / 按状态）
- 归还图书（填实际归还日期）
- 普通用户自助归还（我的借阅页面）
- 逾期未还自动标记
- 借阅状态：借出 / 已归还 / 逾期

### 3.4 图书检索（普通用户）
- 按书名、作者、ISBN 模糊搜索
- 按分类筛选
- 查看图书详情（当前库存、是否可借）
- 直接发起借书

### 3.5 数据统计
- **管理员**：图书总数、在架数量、借出数量、逾期未还数量、借阅排行榜（Top 10）、当月新增图书、分类分布、借阅趋势（近 N 天）
- **普通用户**：累计借阅、当前借出、已逾期、已归还

### 3.6 AI 智能服务
- **个性化推荐**（`/api/ai/recommend`）：基于用户借阅历史的协同过滤算法，有历史则推荐相似用户喜欢的书，无历史则 fallback 到热门图书。无 AI key 时也能工作。
- **馆藏 AI 助手**（`/api/ai/ask`）：每次提问时实时查询 MySQL 馆藏数据（种类数、总册数、可借册数、分类列表）作为上下文注入 prompt，再发给千问，答案基于实时馆藏。
- **AI 图书简介**（`/api/ai/summary`）：调用千问生成 80-150 字简介，结果自动回写 `Book.description` 缓存，节省 token。

## 4. 数据库设计

### 4.1 表结构

**users**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT PK AUTO_INCREMENT | 用户ID |
| username | VARCHAR(50) UNIQUE | 用户名 |
| password_hash | VARCHAR(255) | 密码（bcrypt） |
| role | ENUM('admin','user') | 角色 |
| phone | VARCHAR(20) | 手机号 |
| email | VARCHAR(100) | 邮箱 |
| created_at | DATETIME | 注册时间 |

**books**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT PK AUTO_INCREMENT | 图书ID |
| isbn | VARCHAR(20) UNIQUE | ISBN |
| title | VARCHAR(200) | 书名 |
| author | VARCHAR(100) | 作者 |
| publisher | VARCHAR(100) | 出版社 |
| category | VARCHAR(50) | 分类 |
| stock | INT | 当前库存 |
| total_copies | INT | 总册数 |
| cover_url | VARCHAR(500) | 封面图URL |
| description | TEXT | 简介（AI生成后缓存） |
| created_at | DATETIME | 入库时间 |

**borrow_records**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT PK AUTO_INCREMENT | 记录ID |
| book_id | INT FK | 图书ID |
| user_id | INT FK | 读者ID |
| borrow_date | DATE | 借书日期 |
| due_date | DATE | 应还日期（借书日期+30天） |
| return_date | DATE NULL | 实际归还日期 |
| status | ENUM('borrowed','returned','overdue') | 状态 |

## 5. API 接口设计

### 认证
- `POST /api/auth/register` - 注册
- `POST /api/auth/login` - 登录
- `GET /api/auth/me` - 获取当前用户信息

### 图书
- `GET /api/books` - 图书列表（分页、搜索、分类筛选）
- `GET /api/books/:id` - 图书详情
- `POST /api/books` - 新增图书（管理员）
- `PUT /api/books/:id` - 编辑图书（管理员）
- `DELETE /api/books/:id` - 删除图书（管理员）

### 借阅
- `POST /api/borrow` - 借书
- `PUT /api/borrow/:id/return` - 归还
- `GET /api/borrow/records` - 借阅记录列表
- `GET /api/borrow/my` - 我的借阅记录

### 统计
- `GET /api/stats/overview` - 总览统计
- `GET /api/stats/top-books` - 借阅排行
- `GET /api/stats/category-distribution` - 分类分布
- `GET /api/stats/borrow-trend?days=N` - 借阅趋势
- `GET /api/stats/users` - 用户列表
- `GET /api/stats/my` - 个人统计

### AI 智能
- `GET /api/ai/recommend?limit=N` - 个性化推荐
- `GET /api/ai/summary?book_id=N` - AI 图书简介生成
- `POST /api/ai/ask` - 馆藏 AI 助手问答

## 6. 项目结构

```
library_system/
├── backend/              # Flask 后端
│   ├── app.py           # 主入口
│   ├── models.py        # 数据模型
│   ├── config.py        # 配置（多环境）
│   ├── routes/
│   │   ├── auth.py       # 认证
│   │   ├── books.py      # 图书 CRUD
│   │   ├── borrow.py     # 借阅管理
│   │   ├── stats.py      # 统计
│   │   └── ai.py         # AI 智能服务
│   ├── utils/
│   │   ├── response.py   # 统一响应封装
│   │   ├── validators.py # 参数校验
│   │   └── logger.py     # 日志系统
│   ├── schema.sql       # 数据库建表 SQL
│   └── requirements.txt
├── frontend/            # Vue 3 前端
│   ├── src/
│   │   ├── views/       # 页面组件（7个）
│   │   ├── api/         # Axios API 封装
│   │   ├── router/      # 路由（含权限守卫）
│   │   └── stores/      # Pinia 状态管理
│   └── package.json
└── README.md
```

## 7. 验收标准

- [x] 后端 API 全部可访问，返回正确的统一 JSON 格式
- [x] 前端页面能正常登录、注册
- [x] 管理员可完成图书的增删改查
- [x] 读者可搜索图书、发起借阅
- [x] 借阅记录完整，归还功能正常
- [x] 普通用户可在"我的借阅"页面自助归还
- [x] 统计数据页面正常显示
- [x] AI 个性化推荐（协同过滤 + 热门保底）
- [x] AI 馆藏助手（实时数据库上下文 + 千问）
- [x] AI 图书简介（千问生成 + description 缓存）
- [x] 后端测试 14/14 全通过
