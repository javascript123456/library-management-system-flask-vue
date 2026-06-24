from flask import Blueprint, request, jsonify
from models import db, Book, BorrowRecord
from routes.auth import admin_required, token_required
from sqlalchemy import func
from datetime import date, datetime

stats_bp = Blueprint('stats', __name__, url_prefix='/api/stats')

@stats_bp.route('/overview', methods=['GET'])
@admin_required
def overview():
    total_books = Book.query.count()
    total_copies = db.session.query(func.sum(Book.total_copies)).scalar() or 0
    in_stock = db.session.query(func.sum(Book.stock)).scalar() or 0
    borrowed = int(total_copies) - int(in_stock)
    today = date.today()
    overdue_count = BorrowRecord.query.filter(
        BorrowRecord.status.in_(['borrowed', 'overdue']),
        BorrowRecord.due_date < today
    ).count()
    month_start = datetime(today.year, today.month, 1).date()
    new_this_month = Book.query.filter(Book.created_at >= month_start).count()
    return jsonify({
        'total_books': total_books,
        'total_copies': int(total_copies),
        'in_stock': int(in_stock),
        'borrowed': borrowed,
        'overdue_count': overdue_count,
        'new_this_month': new_this_month
    })

@stats_bp.route('/top-books', methods=['GET'])
@admin_required
def top_books():
    results = db.session.query(
        Book.id, Book.title, Book.author,
        func.count(BorrowRecord.id).label('borrow_count')
    ).join(BorrowRecord, Book.id == BorrowRecord.book_id)\
     .group_by(Book.id)\
     .order_by(func.count(BorrowRecord.id).desc())\
     .limit(10).all()
    return jsonify([{
        'id': r[0], 'title': r[1], 'author': r[2], 'borrow_count': r[3]
    } for r in results])

@stats_bp.route('/users', methods=['GET'])
@admin_required
def user_list():
    from models import User
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])

@stats_bp.route('/my', methods=['GET'])
@token_required
def my_stats():
    user_id = request.current_user.id
    total = BorrowRecord.query.filter_by(user_id=user_id).count()
    borrowed = BorrowRecord.query.filter_by(user_id=user_id, status='borrowed').count()
    overdue = BorrowRecord.query.filter(
        BorrowRecord.user_id == user_id,
        BorrowRecord.status.in_(['borrowed', 'overdue']),
        BorrowRecord.due_date < date.today()
    ).count()
    returned = BorrowRecord.query.filter_by(user_id=user_id, status='returned').count()
    return jsonify({
        'total': total, 'borrowed': borrowed, 'overdue': overdue, 'returned': returned
    })
