# Library Management System API

A simple Flask-based REST API for managing a library system. This API provides CRUD operations for books and members, along with search functionality and token-based authentication.

## Features

- CRUD operations for books
- Member registration and authentication
- Token-based authentication
- Search functionality for books by title or author
- Pagination support
- No third-party dependencies (except Flask)

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Flask

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/library-management-system.git
cd library-management-system
```

2. Install Flask:
```bash
pip install flask
```

3. Run the application:
```bash
python app.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### Books

- `GET /api/books` - Get all books (with pagination and search)
  - Query parameters:
    - `page`: Page number (default: 1)
    - `title`: Search by title
    - `author`: Search by author
- `POST /api/books` - Add a new book (requires authentication)
- `PUT /api/books/<id>` - Update a book (requires authentication)
- `DELETE /api/books/<id>` - Delete a book (requires authentication)

### Members

- `POST /api/members` - Register a new member
- `POST /api/login` - Login and get authentication token

## Design Choices

1. **Data Storage**: Using in-memory storage (Python lists) for simplicity. In a production environment, this should be replaced with a proper database.

2. **Authentication**: 
   - Token-based authentication using secure random tokens
   - Tokens expire after 24 hours
   - Passwords are hashed using SHA-256 (in production, use a proper password hashing algorithm like bcrypt)

3. **Pagination**: 
   - Implemented server-side pagination
   - Default page size of 5 items
   - Returns total count and total pages for client-side handling

4. **Search**: 
   - Case-insensitive search for books by title or author
   - Simple string matching (could be improved with more sophisticated search algorithms)

## Limitations and Assumptions

1. **Data Persistence**: 
   - Data is stored in memory and will be lost when the server restarts
   - No backup or recovery mechanisms

2. **Security**:
   - Basic token-based authentication
   - No rate limiting
   - No HTTPS support (should be added in production)
   - Simple password hashing (should use more secure methods in production)

3. **Scalability**:
   - In-memory storage limits the amount of data that can be handled
   - No caching mechanisms
   - Single server implementation

4. **Error Handling**:
   - Basic error handling implemented
   - No detailed error logging
   - No input validation beyond required fields

## Future Improvements

1. Implement a proper database (e.g., PostgreSQL)
2. Add more robust error handling and logging
3. Implement proper password hashing with salt
4. Add rate limiting
5. Add book borrowing functionality
6. Implement proper API documentation using OpenAPI/Swagger
7. Add unit tests and integration tests

## Contributing

Feel free to submit issues and enhancement requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
