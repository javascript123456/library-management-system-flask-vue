from flask import Blueprint, request, jsonify
from models import db, Book, BorrowRecord
from routes.auth import token_required, admin_required
from datetime import date, timedelta

borrow_bp = Blueprint('borrow', __name__, url_prefix='/api/borrow')

@borrow_bp.route('', methods=['POST'])
@token_required
def borrow_book():
    data = request.get_json()
    book_id = data.get('book_id')
    user_id = data.get('user_id') or request.current_user.id

    if request.current_user.role != 'admin' and user_id != request.current_user.id:
        return jsonify({'error': '无权限'}), 403

    book = db.session.get(Book, book_id)
    if not book:
        return jsonify({'error': '图书不存在'}), 404
    if book.stock <= 0:
        return jsonify({'error': '库存不足，该书已全部借出'}), 400

    active = BorrowRecord.query.filter_by(
        book_id=book_id, user_id=user_id, status='borrowed'
    ).first()
    if active:
        return jsonify({'error': '该用户已有此书的借阅记录未归还'}), 400

    borrow_date = date.today()
    due_date = borrow_date + timedelta(days=30)

    record = BorrowRecord(
        book_id=book_id, user_id=user_id,
        borrow_date=borrow_date, due_date=due_date, status='borrowed'
    )
    book.stock -= 1
    db.session.add(record)
    db.session.commit()
    return jsonify({'message': '借阅成功', 'record': record.to_dict()}), 201

@borrow_bp.route('/<int:record_id>/return', methods=['PUT'])
@token_required
def return_book(record_id):
    record = db.session.get(BorrowRecord, record_id)
    if not record:
        return jsonify({'error': '记录不存在'}), 404
    if record.status == 'returned':
        return jsonify({'error': '该书已归还'}), 400
    if request.current_user.role != 'admin' and record.user_id != request.current_user.id:
        return jsonify({'error': '无权限归还他人书籍'}), 403

    record.return_date = date.today()
    record.status = 'returned'
    record.book.stock += 1
    db.session.commit()
    return jsonify({'message': '归还成功', 'record': record.to_dict()})

@borrow_bp.route('/records', methods=['GET'])
@admin_required
def list_records():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status', '')

    query = BorrowRecord.query
    if status:
        query = query.filter(BorrowRecord.status == status)

    today = date.today()
    for r in query.filter(BorrowRecord.status == 'borrowed').all():
        if r.due_date < today:
            r.status = 'overdue'
    db.session.commit()

    pagination = query.order_by(BorrowRecord.borrow_date.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        'items': [r.to_dict() for r in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'page': page
    })

@borrow_bp.route('/my', methods=['GET'])
@token_required
def my_records():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    pagination = BorrowRecord.query.filter_by(user_id=request.current_user.id)\
        .order_by(BorrowRecord.borrow_date.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        'items': [r.to_dict() for r in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'page': page
    })
