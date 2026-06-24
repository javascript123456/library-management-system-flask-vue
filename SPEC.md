# 图书管理系统 - 项目规格说明书

## 1. 项目概述

**项目名称**：图书管理系统（Library Management System）  
**项目类型**：前后端分离的 Web 应用  
**核心功能**：图书增删改查、借阅归还、用户管理、数据统计。  
**目标用户**：图书馆管理员，普通读者

## 2. 技术栈

- **后端**：Python Flask 2.x + Flask-SQLAlchemy + Flask-CORS
- **数据库**：MySQL 8.0
- **前端**：Vue 3 (Composition API) + Vite + Axios + Element Plus
- **认证**：JWT（JSON Web Token）

## 3. 功能模块

### 3.1 用户管理
- 用户注册、登录、登出
- 管理员与普通用户角色区分
- JWT token 认证

### 3.2 图书管理（管理员）
- 图书增删改查
- 分类筛选、分页

### 3.3 借阅管理
- 读者借书、归还图书
- 借阅状态：借出 / 已归还 / 逾期

### 3.4 普通用户
- 图书搜索、借书
- 查看自己的借阅记录

### 3.5 数据统计
- 管理员：图书总数、在架数量、借出数量、借阅排行榜
- 普通用户：累计借阅、当前借出、已逾期

## 4. 角色权限说明

| 功能 | 管理员 | 普通用户 |
|------|--------|---------|
| 登录/注册 | ✅ | ✅ |
| 图书搜索 | ✅ | ✅ |
| 新增/编辑/删除图书 | ✅ | ❌ |
| 图书页面借书 | ❌ | ✅ |
| 归还图书 | ✅ | 仅自己的 |
| 首页统计数据 | 全部 | 个人统计 |
| 用户管理 | ✅ | ❌ |

## 5. 数据库设计

### users
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT PK | 用户ID |
| username | VARCHAR(50) UNIQUE | 用户名 |
| password_hash | VARCHAR(255) | 密码（bcrypt） |
| role | ENUM('admin','user') | 角色 |
| phone | VARCHAR(20) | 手机号 |
| email | VARCHAR(100) | 邮箱 |
| created_at | DATETIME | 注册时间 |

### books
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT PK | 图书ID |
| isbn | VARCHAR(20) UNIQUE | ISBN |
| title | VARCHAR(200) | 书名 |
| author | VARCHAR(100) | 作者 |
| publisher | VARCHAR(100) | 出版社 |
| category | VARCHAR(50) | 分类 |
| stock | INT | 库存数量 |
| total_copies | INT | 总册数 |
| description | TEXT | 简介 |
| created_at | DATETIME | 入库时间 |

### borrow_records
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT PK | 记录ID |
| book_id | INT FK | 图书ID |
| user_id | INT FK | 读者ID |
| borrow_date | DATE | 借书日期 |
| due_date | DATE | 应还日期 |
| return_date | DATE | 实际归还日期 |
| status | ENUM | 状态 |

## 6. API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/auth/register | 注册 |
| POST | /api/auth/login | 登录 |
| GET | /api/auth/me | 当前用户 |
| GET | /api/books | 图书列表 |
| POST | /api/books | 新增图书 |
| PUT | /api/books/:id | 编辑图书 |
| DELETE | /api/books/:id | 删除图书 |
| GET | /api/books/categories | 分类列表 |
| POST | /api/borrow | 借书 |
| PUT | /api/borrow/:id/return | 归还 |
| GET | /api/borrow/records | 借阅记录（管理员） |
| GET | /api/borrow/my | 我的借阅 |
| GET | /api/stats/overview | 总览统计（管理员） |
| GET | /api/stats/top-books | 借阅排行（管理员） |
| GET | /api/stats/users | 用户列表（管理员） |
| GET | /api/stats/my | 个人统计（普通用户） |
