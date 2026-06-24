# 图书管理系统

基于 Flask + MySQL + Vue 3 的前后端分离图书管理系统。

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | Python Flask 2.x / Flask-SQLAlchemy / PyJWT / bcrypt |
| 数据库 | MySQL 8.0 |
| 前端 | Vue 3 (Composition API) / Vite 5 / Element Plus / Pinia |
| 认证 | JWT (JSON Web Token) |
| AI | 阿里云百炼千问（qwen-max）|

## 项目结构

```
library_system/
├── backend/               # Flask 后端
│   ├── app.py           # 主入口
│   ├── models.py        # 数据模型（User / Book / BorrowRecord）
│   ├── config.py        # 配置（多环境支持）
│   ├── schema.sql       # 建表 SQL + 初始化数据
│   ├── requirements.txt  # Python 依赖
│   └── routes/
│       ├── auth.py       # 认证（注册/登录/JWT）
│       ├── books.py      # 图书 CRUD
│       ├── borrow.py     # 借阅/归还
│       ├── stats.py      # 统计
│       └── ai.py         # AI 智能服务（推荐/简介/问答）
├── frontend/             # Vue 3 前端
│   ├── src/
│   │   ├── views/       # 页面组件
│   │   ├── router/      # 路由（含权限守卫）
│   │   ├── stores/      # Pinia 状态管理
│   │   └── api/          # Axios 封装
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

在 MySQL 中执行建表脚本（会自动创建库和表，并插入测试数据）：

```bash
mysql -u root -p < backend/schema.sql
```

> 默认管理员账号：**admin** / **admin123**

### 3. 后端启动

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env   # 复制配置（生产环境修改 SECRET_KEY 和数据库密码）
python app.py
```

后端运行在 http://localhost:5000

### 4. 前端启动

```bash
cd frontend
npm install
npm run dev
```

前端运行在 http://localhost:5173（API 请求自动代理到后端 5000）

### 5. 访问系统

打开浏览器访问 http://localhost:5173，使用管理员账号登录。

## 功能模块

| 模块 | 功能 |
|------|------|
| 首页概览 | 管理员：图书总数、在架数量、借出数量、逾期数量、借阅排行榜；普通用户：累计借阅、当前借出、已逾期 |
| 图书管理 | 搜索（书名/作者/ISBN）、分类筛选、分页；管理员：新增/编辑/删除；普通用户：直接借书 |
| 借阅管理 | 办理借书、归还图书、借阅记录查询（按状态筛选） |
| 我的借阅 | 当前用户借阅历史（含自助归还） |
| 用户管理 | 查看所有用户（仅管理员） |
| AI 智能推荐 | 基于协同过滤的个性化图书推荐（Dashboard 首页） |
| AI 简介生成 | 千问大模型生成图书简介（图书管理页每本书） |
| 馆藏 AI 助手 | 基于馆藏实时数据的智能问答（首页入口） |

## AI 智能功能说明

### 数据联动机制

AI 功能的每一次回答，都是**和 MySQL 实时联动**的：

1. **馆藏 AI 助手（`/api/ai/ask`）**：每次提问时，后端先从数据库实时查询当前馆藏数据（图书种类数、总册数、可借册数、分类列表），注入 prompt 作为上下文，再发给千问。所以图书入库、借出、归还后，下一次 AI 回答的馆藏数字会同步更新。

2. **AI 图书简介（`/api/ai/summary`）**：调用千问生成后，会自动回写 `Book.description` 字段缓存，相同图书再次请求直接返回缓存内容，节省 token。

3. **个性化推荐（`/api/ai/recommend`）**：基于用户的借阅历史做协同过滤（找相似用户 → 找他们借过但当前用户没借过的书），无历史时 fallback 到热门图书。无 AI key 时也能工作。

### 配置千问 API

在 `backend/.env` 中配置（参考 `.env.example`）：

```bash
QIANWEN_API_KEY=sk-ws-xxxxxxxxxxxx   # 阿里云百炼 API Key
QIANWEN_MODEL=qwen-max               # 模型名称
QIANWEN_BASE_URL=https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation
```

申请地址：https://dashscope.console.aliyun.com/

> 未配置 API Key 时，AI 简介返回模板简介，馆藏助手返回馆藏统计数字，均不影响核心功能使用。

## 角色权限说明

| 功能 | 管理员 | 普通用户 |
|------|--------|---------|
| 登录/注册 | ✅ | ✅ |
| 图书搜索 | ✅ | ✅ |
| 新增/编辑/删除图书 | ✅ | ❌ |
| 图书页面借书 | ❌ | ✅ |
| 归还图书 | ✅ | 仅自己的 |
| AI 推荐/问答 | ✅ | ✅ |
| 首页统计数据 | 全部 | 个人统计 |
| 借阅排行榜 | ✅ | ❌ |
| 用户管理 | ✅ | ❌ |

## API 接口一览

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/auth/register | 用户注册 |
| POST | /api/auth/login | 登录 |
| GET | /api/auth/me | 当前用户信息 |
| GET | /api/books | 图书列表（分页+搜索+分类筛选） |
| GET | /api/books/:id | 图书详情 |
| POST | /api/books | 新增图书（管理员） |
| PUT | /api/books/:id | 编辑图书（管理员） |
| DELETE | /api/books/:id | 删除图书（管理员） |
| GET | /api/books/categories | 获取所有分类 |
| POST | /api/borrow | 借书 |
| PUT | /api/borrow/:id/return | 归还 |
| GET | /api/borrow/records | 借阅记录列表（管理员） |
| GET | /api/borrow/my | 我的借阅记录 |
| GET | /api/stats/overview | 总览统计（管理员） |
| GET | /api/stats/top-books | 借阅排行榜（管理员） |
| GET | /api/stats/category-distribution | 分类分布（管理员） |
| GET | /api/stats/borrow-trend | 借阅趋势（管理员） |
| GET | /api/stats/users | 用户列表（管理员） |
| GET | /api/stats/my | 个人统计（普通用户） |
| GET | /api/ai/recommend | AI 个性化推荐 |
| GET | /api/ai/summary | AI 图书简介生成 |
| POST | /api/ai/ask | 馆藏 AI 助手问答 |
