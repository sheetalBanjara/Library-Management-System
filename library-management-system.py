# app.py
from flask import Flask, request, jsonify
import json
import secrets
from datetime import datetime, timedelta
import hashlib

app = Flask(__name__)

# In-memory storage (in production, you'd use a proper database)
books = []
members = []
tokens = {}  # Store active tokens
ITEMS_PER_PAGE = 5

# Helper functions
def generate_token():
    return secrets.token_hex(16)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_token(token):
    if token not in tokens or tokens[token]['expires'] < datetime.now():
        return None
    return tokens[token]['member_id']

def paginate(items, page):
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    return items[start:end]

# Book routes
@app.route('/api/books', methods=['GET'])
def get_books():
    page = int(request.args.get('page', 1))
    search_title = request.args.get('title')
    search_author = request.args.get('author')
    
    filtered_books = books
    
    if search_title:
        filtered_books = [b for b in filtered_books if search_title.lower() in b['title'].lower()]
    if search_author:
        filtered_books = [b for b in filtered_books if search_author.lower() in b['author'].lower()]
    
    paginated_books = paginate(filtered_books, page)
    return jsonify({
        'books': paginated_books,
        'total': len(filtered_books),
        'page': page,
        'total_pages': (len(filtered_books) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
    })

@app.route('/api/books', methods=['POST'])
def add_book():
    token = request.headers.get('Authorization')
    if not authenticate_token(token):
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    if not all(key in data for key in ['title', 'author', 'isbn']):
        return jsonify({'error': 'Missing required fields'}), 400
        
    book = {
        'id': len(books) + 1,
        'title': data['title'],
        'author': data['author'],
        'isbn': data['isbn'],
        'available': True
    }
    books.append(book)
    return jsonify(book), 201

@app.route('/api/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    token = request.headers.get('Authorization')
    if not authenticate_token(token):
        return jsonify({'error': 'Unauthorized'}), 401

    book = next((b for b in books if b['id'] == book_id), None)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
        
    data = request.get_json()
    book.update({
        'title': data.get('title', book['title']),
        'author': data.get('author', book['author']),
        'isbn': data.get('isbn', book['isbn'])
    })
    return jsonify(book)

@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    token = request.headers.get('Authorization')
    if not authenticate_token(token):
        return jsonify({'error': 'Unauthorized'}), 401

    book = next((b for b in books if b['id'] == book_id), None)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
        
    books.remove(book)
    return '', 204

# Member routes
@app.route('/api/members', methods=['POST'])
def register_member():
    data = request.get_json()
    if not all(key in data for key in ['username', 'password', 'email']):
        return jsonify({'error': 'Missing required fields'}), 400
        
    if any(m['username'] == data['username'] for m in members):
        return jsonify({'error': 'Username already exists'}), 400
        
    member = {
        'id': len(members) + 1,
        'username': data['username'],
        'password': hash_password(data['password']),
        'email': data['email']
    }
    members.append(member)
    return jsonify({k: v for k, v in member.items() if k != 'password'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if not all(key in data for key in ['username', 'password']):
        return jsonify({'error': 'Missing credentials'}), 400
        
    member = next((m for m in members if m['username'] == data['username'] and 
                  m['password'] == hash_password(data['password'])), None)
    if not member:
        return jsonify({'error': 'Invalid credentials'}), 401
        
    token = generate_token()
    tokens[token] = {
        'member_id': member['id'],
        'expires': datetime.now() + timedelta(hours=24)
    }
    return jsonify({'token': token})

if __name__ == '__main__':
    # Add some sample data
    books.extend([
        {'id': 1, 'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald', 'isbn': '978-0743273565', 'available': True},
        {'id': 2, 'title': '1984', 'author': 'George Orwell', 'isbn': '978-0451524935', 'available': True}
    ])
    app.run(debug=True)
