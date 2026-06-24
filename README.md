# 图书管理系统

基于 Flask + MySQL + Vue 3 的前后端分离图书管理系统。

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | Python Flask 2.x / Flask-SQLAlchemy / PyJWT / bcrypt |
| 数据库 | MySQL 8.0 |
| 前端 | Vue 3 (Composition API) / Vite 5 / Element Plus / Pinia |
| 认证 | JWT (JSON Web Token) |

## 快速启动

### 1. 环境要求
- Python 3.8+ / Node.js 18+ / MySQL 8.0

### 2. 数据库
```bash
mysql -u root -p < backend/schema.sql
```
> 默认管理员：**admin** / **admin123**

### 3. 后端
```bash
cd backend && pip install -r requirements.txt && python app.py
```

### 4. 前端
```bash
cd frontend && npm install && npm run dev
```

访问 http://localhost:3000 即可使用。
