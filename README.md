# 图书管理系统

基于 Flask + MySQL + Vue 3 的前后端分离图书管理系统。

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | Python Flask 2.x / Flask-SQLAlchemy / PyJWT / bcrypt |
| 数据库 | MySQL 8.0 |
| 前端 | Vue 3 (Composition API) / Vite 5 / Element Plus / Pinia |
| 认证 | JWT (JSON Web Token) |

## 项目结构

```
library_system/
├── backend/               # Flask 后端
│   ├── app.py            # 主入口
│   ├── models.py         # 数据模型（User/Book/BorrowRecord）
│   ├── config.py          # 数据库配置
│   ├── schema.sql         # 建表 SQL + 初始化数据
│   ├── requirements.txt   # Python 依赖
│   └── routes/
│       ├── auth.py       # 认证（注册/登录/JWT）
│       ├── books.py      # 图书 CRUD
│       ├── borrow.py     # 借阅/归还
│       └── stats.py      # 统计（含普通用户统计）
├── frontend/             # Vue 3 前端
│   ├── src/
│   │   ├── views/        # 7个页面组件
│   │   ├── router/      # 路由配置（含权限守卫）
│   │   ├── stores/       # Pinia 状态管理
│   │   └── api/          # Axios API 封装
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
├── SPEC.md               # 项目规格说明书
└── README.md
```

## 快速启动

### 1. 环境要求

- Python 3.8+
- Node.js 18+
- MySQL 8.0

### 2. 数据库配置

在 MySQL 中执行建表脚本：

```bash
mysql -u root -p < backend/schema.sql
```

> 默认管理员账号：**admin** / **admin123**

### 3. 后端启动

```bash
cd backend
pip install -r requirements.txt
python app.py
```

后端运行在 http://localhost:5000

### 4. 前端启动

```bash
cd frontend
npm install
npm run dev
```

前端运行在 http://localhost:3000（API 请求自动代理到后端 5000）

### 5. 访问系统

打开浏览器访问 http://localhost:3000，使用管理员账号登录。

## 功能模块

| 模块 | 功能 |
|------|------|
| 首页概览 | 管理员：图书总数、在架数量、借出数量、逾期数量、借阅排行榜；普通用户：累计借阅、当前借出、已逾期 |
| 图书管理 | 搜索（书名/作者/ISBN）、分类筛选、分页；管理员：新增/编辑/删除；普通用户：直接借书 |
| 借阅管理 | 办理借书、归还图书、借阅记录查询（按状态筛选） |
| 我的借阅 | 当前用户借阅历史 |
| 用户管理 | 查看所有用户（仅管理员） |

## 角色权限说明

| 功能 | 管理员 | 普通用户 |
|------|--------|---------|
| 登录/注册 | ✅ | ✅ |
| 图书搜索 | ✅ | ✅ |
| 新增/编辑/删除图书 | ✅ | ❌ |
| 图书页面借书 | ❌ | ✅ |
| 归还图书 | ✅ | 仅自己的 |
| 首页统计数据 | 全部 | 个人统计 |
| 借阅排行榜 | ✅ | ❌ |
| 用户管理 | ✅ | ❌ |

## API 接口一览

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/auth/register | 用户注册 |
| POST | /api/auth/login | 登录 |
| GET | /api/auth/me | 当前用户信息 |
| GET | /api/books | 图书列表（分页+搜索） |
| POST | /api/books | 新增图书 |
| PUT | /api/books/:id | 编辑图书 |
| DELETE | /api/books/:id | 删除图书 |
| GET | /api/books/categories | 获取分类 |
| POST | /api/borrow | 借书 |
| PUT | /api/borrow/:id/return | 归还 |
| GET | /api/borrow/records | 借阅记录（管理员） |
| GET | /api/borrow/my | 我的借阅记录 |
| GET | /api/stats/overview | 总览统计（管理员） |
| GET | /api/stats/top-books | 借阅排行榜（管理员） |
| GET | /api/stats/users | 用户列表（管理员） |
| GET | /api/stats/my | 个人统计（普通用户） |
