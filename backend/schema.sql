-- 图书管理系统数据库初始化脚本
CREATE DATABASE IF NOT EXISTS library_db DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE library_db;

DROP TABLE IF EXISTS borrow_records;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'user') NOT NULL DEFAULT 'user',
    phone VARCHAR(20) DEFAULT '',
    email VARCHAR(100) DEFAULT '',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE books (
    id INT PRIMARY KEY AUTO_INCREMENT,
    isbn VARCHAR(20) NOT NULL UNIQUE,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(100) NOT NULL,
    publisher VARCHAR(100) DEFAULT '',
    category VARCHAR(50) DEFAULT '',
    stock INT DEFAULT 1,
    total_copies INT DEFAULT 1,
    cover_url VARCHAR(500) DEFAULT '',
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE borrow_records (
    id INT PRIMARY KEY AUTO_INCREMENT,
    book_id INT NOT NULL,
    user_id INT NOT NULL,
    borrow_date DATE NOT NULL,
    due_date DATE NOT NULL,
    return_date DATE NULL,
    status ENUM('borrowed', 'returned', 'overdue') DEFAULT 'borrowed',
    FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 插入管理员账号 admin / admin123
INSERT INTO users (username, password_hash, role, email) VALUES
('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYfH97q1CXC', 'admin', 'admin@library.com');

-- 插入测试图书数据
INSERT INTO books (isbn, title, author, publisher, category, stock, total_copies, description) VALUES
('978-7-115-42844-3', 'Python编程：从入门到实践', 'Eric Matthes', '人民邮电出版社', '计算机', 3, 5, 'Python入门经典书籍'),
('978-7-111-54742-6', '算法导论（第3版）', 'Thomas H. Cormen', '机械工业出版社', '计算机', 2, 3, '算法领域经典教材'),
('978-7-121-17607-2', 'JavaScript高级程序设计', 'Nicholas C. Zakas', '电子工业出版社', '计算机', 2, 3, 'JS前端开发必读'),
('978-7-115-42880-1', 'Vue.js实战', '梁灏', '人民邮电出版社', '计算机', 2, 2, 'Vue.js 3框架学习指南'),
('978-7-111-52148-8', '深入理解计算机系统', 'Randal E. Bryant', '机械工业出版社', '计算机', 1, 2, '系统级理解计算机'),
('978-7-115-28583-0', '数据库系统概论', '王珊, 萨师煊', '人民邮电出版社', '计算机', 3, 4, '数据库基础理论教材'),
('978-7-04-044908-4', '数据结构（C语言版）', '严蔚敏, 吴伟民', '高等教育出版社', '计算机', 2, 3, '数据结构经典教材'),
('978-7-115-44795-6', '深度学习入门：基于Python的理论与实现', '斋藤康毅', '人民邮电出版社', '计算机', 2, 2, 'AI与深度学习入门书籍'),
('978-7-111-52152-5', '计算机网络：自顶向下方法', 'James F. Kurose', '机械工业出版社', '计算机', 2, 2, '网络协议经典教材'),
('978-7-115-44895-3', 'Flask Web开发实战', '李辉', '人民邮电出版社', '计算机', 2, 2, 'Flask框架Web开发指南');
