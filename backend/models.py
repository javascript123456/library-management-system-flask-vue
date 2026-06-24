from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('admin', 'user'), default='user', nullable=False)
    phone = db.Column(db.String(20), default='')
    email = db.Column(db.String(100), default='')
    created_at = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role,
            'phone': self.phone,
            'email': self.email,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else ''
        }

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publisher = db.Column(db.String(100), default='')
    category = db.Column(db.String(50), default='')
    stock = db.Column(db.Integer, default=1)
    total_copies = db.Column(db.Integer, default=1)
    cover_url = db.Column(db.String(500), default='')
    description = db.Column(db.Text, default='')
    created_at = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id, 'isbn': self.isbn, 'title': self.title,
            'author': self.author, 'publisher': self.publisher,
            'category': self.category, 'stock': self.stock,
            'total_copies': self.total_copies, 'cover_url': self.cover_url,
            'description': self.description,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else ''
        }

class BorrowRecord(db.Model):
    __tablename__ = 'borrow_records'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    borrow_date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.Enum('borrowed', 'returned', 'overdue'), default='borrowed')

    book = db.relationship('Book', backref='borrow_records')
    user = db.relationship('User', backref='borrow_records')

    def to_dict(self):
        return {
            'id': self.id, 'book_id': self.book_id, 'user_id': self.user_id,
            'book_title': self.book.title if self.book else '',
            'username': self.user.username if self.user else '',
            'borrow_date': self.borrow_date.strftime('%Y-%m-%d') if self.borrow_date else '',
            'due_date': self.due_date.strftime('%Y-%m-%d') if self.due_date else '',
            'return_date': self.return_date.strftime('%Y-%m-%d') if self.return_date else '',
            'status': self.status
        }
