from flask import Blueprint, request, jsonify
from models import db, Book
from routes.auth import token_required, admin_required

books_bp = Blueprint('books', __name__, url_prefix='/api/books')

@books_bp.route('', methods=['GET'])
@token_required
def list_books():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    keyword = request.args.get('keyword', '')
    category = request.args.get('category', '')

    query = Book.query
    if keyword:
        keyword_filter = f'%{keyword}%'
        query = query.filter(
            db.or_(
                Book.title.like(keyword_filter),
                Book.author.like(keyword_filter),
                Book.isbn.like(keyword_filter)
            )
        )
    if category:
        query = query.filter(Book.category == category)

    pagination = query.order_by(Book.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        'items': [b.to_dict() for b in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'page': page
    })

@books_bp.route('/<int:book_id>', methods=['GET'])
@token_required
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    return jsonify(book.to_dict())

@books_bp.route('', methods=['POST'])
@admin_required
def add_book():
    data = request.get_json()
    if not data.get('isbn') or not data.get('title') or not data.get('author'):
        return jsonify({'error': 'ISBN、书名、作者不能为空'}), 400
    if Book.query.filter_by(isbn=data['isbn']).first():
        return jsonify({'error': 'ISBN已存在'}), 400

    book = Book(
        isbn=data['isbn'], title=data['title'], author=data['author'],
        publisher=data.get('publisher', ''), category=data.get('category', ''),
        stock=data.get('stock', 1), total_copies=data.get('total_copies', 1),
        cover_url=data.get('cover_url', ''), description=data.get('description', '')
    )
    db.session.add(book)
    db.session.commit()
    return jsonify({'message': '添加成功', 'book': book.to_dict()}), 201

@books_bp.route('/<int:book_id>', methods=['PUT'])
@admin_required
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    data = request.get_json()

    if data.get('isbn') and data['isbn'] != book.isbn:
        if Book.query.filter(Book.isbn == data['isbn'], Book.id != book_id).first():
            return jsonify({'error': 'ISBN已被其他图书使用'}), 400
        book.isbn = data['isbn']

    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.publisher = data.get('publisher', book.publisher)
    book.category = data.get('category', book.category)
    if 'stock' in data: book.stock = data['stock']
    if 'total_copies' in data: book.total_copies = data['total_copies']
    book.cover_url = data.get('cover_url', book.cover_url)
    book.description = data.get('description', book.description)
    db.session.commit()
    return jsonify({'message': '更新成功', 'book': book.to_dict()})

@books_bp.route('/<int:book_id>', methods=['DELETE'])
@admin_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': '删除成功'})

@books_bp.route('/categories', methods=['GET'])
@token_required
def list_categories():
    categories = db.session.query(Book.category).distinct().filter(Book.category != '').all()
    return jsonify([c[0] for c in categories])
