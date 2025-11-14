# Flask-RESTful API 

---

##  Core Overview

### What is Flask-RESTful?

- **Flask**: Lightweight Python web framework with minimal boilerplate
- **REST**: Architectural style using HTTP methods for resource-based APIs
- **Flask-RESTful**: Extension that simplifies REST API development using Resource classes

### Why Use It?

- Reduces boilerplate code
- Organized structure with Resource classes
- Built-in request parsing and validation
- Perfect for microservices and APIs

---

## REST Fundamentals

### Resources

Entities exposed via API (User, Product, Order)

- Represented as Python classes
- Each resource has a unique identifier

### Endpoints

URL paths pointing to resources:

```
/api/users          → Collection
/api/users/123      → Specific resource
/api/users/123/orders → Nested resource
```

### HTTP Methods

|Method|Purpose|Idempotent|Safe|
|---|---|---|---|
|GET|Retrieve resource(s)|✅ Yes|✅ Yes|
|POST|Create new resource|❌ No|❌ No|
|PUT|Replace entire resource|✅ Yes|❌ No|
|PATCH|Partial update|❌ No|❌ No|
|DELETE|Remove resource|✅ Yes|❌ No|

> **Idempotent**: Multiple identical requests = same result **Safe**: Doesn't modify server state

### Representations

- Data format for request/response
- Usually JSON (application/json)
- Can be XML, HTML, etc.

---

## HTTP Status Codes (Must Know!)

### 2xx - Success

```
200 OK              → Request succeeded, data returned
201 Created         → Resource successfully created
204 No Content      → Success, no response body (DELETE)
```

### 4xx - Client Errors

```
400 Bad Request     → Invalid input/malformed request
401 Unauthorized    → Missing or invalid authentication
403 Forbidden       → Authenticated but lacks permission
404 Not Found       → Resource doesn't exist
409 Conflict        → Duplicate resource/constraint violation
422 Unprocessable   → Validation failed
```

### 5xx - Server Errors

```
500 Internal Error  → Unexpected server failure
502 Bad Gateway     → Invalid upstream response
503 Unavailable     → Server overloaded/maintenance
```

---

## Request Flow Diagram

```mermaid
sequenceDiagram
    autonumber
    participant Client
    participant Flask
    participant Resource
    participant Database
    
    Client->>Flask: HTTP Request (GET/POST/PUT/DELETE)
    Flask->>Resource: Route dispatch (/api/users/1)
    Resource->>Database: Query/Write operation
    Database-->>Resource: Data/Result
    Resource-->>Flask: JSON response + status code
    Flask-->>Client: HTTP Response
```

**Step-by-Step:**

1. Client sends HTTP request with method + data
2. Flask receives and routes to correct Resource class
3. Resource method executes business logic
4. Database operation (CRUD)
5. Resource returns JSON + appropriate status code
6. Flask packages and sends HTTP response

---

## Basic Implementation

### Minimal Example

```python
from flask import Flask, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

# In-memory storage (use DB in production)
USERS = {}

class UserResource(Resource):
    def get(self, uid):
        """Retrieve single user"""
        if uid in USERS:
            return USERS[uid], 200
        return {"error": "User not found"}, 404
    
    def put(self, uid):
        """Create/replace user"""
        data = request.get_json() or {}
        USERS[uid] = data
        return USERS[uid], 201
    
    def delete(self, uid):
        """Remove user"""
        if uid in USERS:
            del USERS[uid]
            return "", 204
        return {"error": "User not found"}, 404

# Register route
api.add_resource(UserResource, "/api/users/<string:uid>")

if __name__ == "__main__":
    app.run(debug=True)
```

---

##  Production-Ready Example

### Full Implementation with Best Practices

```python
from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
CORS(app)  # Handle cross-origin requests
api = Api(app)

# In-memory store (use database in production)
USERS = {}

# Input validation parser
user_parser = reqparse.RequestParser()
user_parser.add_argument('name', type=str, required=True, 
                         help='Name is required')
user_parser.add_argument('email', type=str, required=True, 
                         help='Email is required')
user_parser.add_argument('age', type=int)

class UserResource(Resource):
    """Handle single user operations"""
    
    def get(self, uid):
        """Retrieve single user by ID"""
        user = USERS.get(uid)
        if not user:
            return {"error": "User not found"}, 404
        return user, 200
    
    def put(self, uid):
        """Create or replace entire user"""
        try:
            args = user_parser.parse_args()
            USERS[uid] = {
                "id": uid,
                "name": args['name'],
                "email": args['email'],
                "age": args.get('age'),
                "created_at": datetime.utcnow().isoformat()
            }
            return USERS[uid], 201
        except Exception as e:
            return {"error": str(e)}, 400
    
    def patch(self, uid):
        """Partially update user"""
        if uid not in USERS:
            return {"error": "User not found"}, 404
        
        data = request.get_json() or {}
        USERS[uid].update(data)
        USERS[uid]['updated_at'] = datetime.utcnow().isoformat()
        return USERS[uid], 200
    
    def delete(self, uid):
        """Remove user"""
        if uid in USERS:
            del USERS[uid]
            return "", 204
        return {"error": "User not found"}, 404

class UserListResource(Resource):
    """Handle user collection operations"""
    
    def get(self):
        """List all users with pagination"""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Pagination logic
        start = (page - 1) * per_page
        end = start + per_page
        users = list(USERS.values())[start:end]
        
        return {
            "users": users,
            "page": page,
            "per_page": per_page,
            "total": len(USERS)
        }, 200
    
    def post(self):
        """Create new user with auto-generated ID"""
        try:
            args = user_parser.parse_args()
            uid = str(len(USERS) + 1)
            USERS[uid] = {
                "id": uid,
                "name": args['name'],
                "email": args['email'],
                "age": args.get('age'),
                "created_at": datetime.utcnow().isoformat()
            }
            return USERS[uid], 201
        except Exception as e:
            return {"error": str(e)}, 400

# Register routes with versioning
api.add_resource(UserListResource, "/api/v1/users")
api.add_resource(UserResource, "/api/v1/users/<string:uid>")

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return {"error": "Resource not found"}, 404

@app.errorhandler(500)
def internal_error(error):
    return {"error": "Internal server error"}, 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
```

---

## Project Structure (Production)

```
flask-api-project/
│
├── app.py                    # Application entry point
├── config.py                 # Configuration settings
├── requirements.txt          # Dependencies
├── .env                      # Environment variables
│
├── resources/                # API resources
│   ├── __init__.py
│   ├── users.py             # User endpoints
│   ├── products.py          # Product endpoints
│   └── orders.py            # Order endpoints
│
├── models/                   # Database models
│   ├── __init__.py
│   ├── user.py
│   └── product.py
│
├── schemas/                  # Validation schemas
│   ├── __init__.py
│   └── user_schema.py
│
├── utils/                    # Helper functions
│   ├── __init__.py
│   ├── validators.py
│   └── auth.py
│
└── tests/                    # Test files
    ├── __init__.py
    ├── test_users.py
    └── test_products.py
```

---

## Production Best Practices

### 1. API Versioning

```python
# URI versioning (most common)
api.add_resource(UserResource, "/api/v1/users/<uid>")
api.add_resource(UserResourceV2, "/api/v2/users/<uid>")

# Allows breaking changes without affecting existing clients
```

### 2. Input Validation (Marshmallow)

```python
from marshmallow import Schema, fields, validate, ValidationError

class UserSchema(Schema):
    name = fields.Str(
        required=True, 
        validate=validate.Length(min=1, max=100)
    )
    email = fields.Email(required=True)
    age = fields.Int(validate=validate.Range(min=0, max=150))
    role = fields.Str(validate=validate.OneOf(['user', 'admin']))

# Usage in Resource
def post(self):
    schema = UserSchema()
    try:
        data = schema.load(request.get_json())
        # Process validated data
    except ValidationError as err:
        return {"errors": err.messages}, 400
```

### 3. Authentication (JWT)

```python
from flask_jwt_extended import (
    JWTManager, jwt_required, 
    create_access_token, get_jwt_identity
)

app.config['JWT_SECRET_KEY'] = 'super-secret-key'
jwt = JWTManager(app)

class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        # Verify credentials (check database)
        if verify_user(data['username'], data['password']):
            access_token = create_access_token(
                identity=data['username']
            )
            return {"access_token": access_token}, 200
        return {"error": "Invalid credentials"}, 401

class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        return {"logged_in_as": current_user}, 200
```

### 4. Error Handling

```python
from flask import jsonify

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "error": "Bad Request",
        "message": str(error)
    }), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Not Found",
        "message": "Resource not found"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Internal Server Error",
        "message": "Something went wrong"
    }), 500

# Custom exception
class ResourceNotFound(Exception):
    pass

@app.errorhandler(ResourceNotFound)
def handle_not_found(error):
    return jsonify({"error": str(error)}), 404
```

### 5. CORS Configuration

```python
from flask_cors import CORS

# Basic CORS (allow all)
CORS(app)

# Controlled CORS (production)
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://yourdomain.com", "https://app.yourdomain.com"],
        "methods": ["GET", "POST", "PUT", "DELETE", "PATCH"],
        "allow_headers": ["Content-Type", "Authorization"],
        "expose_headers": ["Content-Range", "X-Content-Range"],
        "max_age": 3600
    }
})
```

### 6. Rate Limiting

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

class UserResource(Resource):
    decorators = [limiter.limit("10 per minute")]
    
    def get(self, uid):
        # This endpoint limited to 10 requests/minute
        pass
```

### 7. Pagination Helper

```python
def paginate(query, page, per_page):
    """Generic pagination helper"""
    items = query[(page-1)*per_page : page*per_page]
    total = len(query)
    
    return {
        "items": items,
        "page": page,
        "per_page": per_page,
        "total": total,
        "pages": (total + per_page - 1) // per_page
    }

# Usage
def get(self):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    return paginate(list(USERS.values()), page, per_page), 200
```

### 8. Environment Variables

```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///dev.db')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    DEBUG = os.getenv('FLASK_ENV') == 'development'

app.config.from_object(Config)
```

### 9. Database Integration (SQLAlchemy)

```python
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at.isoformat()
        }

# Usage in Resource
class UserResource(Resource):
    def get(self, uid):
        user = User.query.get_or_404(uid)
        return user.to_dict(), 200
    
    def post(self):
        data = request.get_json()
        user = User(name=data['name'], email=data['email'])
        db.session.add(user)
        db.session.commit()
        return user.to_dict(), 201
```

### 10. Logging

```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler(
        'app.log', 
        maxBytes=10240, 
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('API startup')

# Usage
app.logger.info(f'User {uid} accessed')
app.logger.error(f'Failed to create user: {str(e)}')
```

---

##  Interview Questions & Answers

### Q1: What's the difference between PUT and PATCH?

**Answer:**

- **PUT**: Replaces the entire resource. Client must send all fields, even unchanged ones. Idempotent.
- **PATCH**: Applies partial updates. Client sends only changed fields. Not strictly idempotent.

**Example:**

```python
# PUT - Must send complete data
PUT /api/users/123
{"name": "John Doe", "email": "john@example.com", "age": 30}

# PATCH - Send only changed fields
PATCH /api/users/123
{"age": 31}
```

---

### Q2: Which HTTP methods are idempotent and why?

**Answer:** Idempotent methods: **GET, PUT, DELETE, HEAD, OPTIONS**

Making the same request multiple times produces the same result:

- GET: Reading same resource returns same data
- PUT: Replacing with same data gives same result
- DELETE: Deleting already-deleted resource still results in "not found"

**Not idempotent**: POST, PATCH

- POST: Creates new resource each time (different IDs)
- PATCH: May have side effects or conditional logic

---

### Q3: Explain REST statelessness

**Answer:** Each request from client to server must contain ALL information needed to understand and process it. Server doesn't store client session between requests.

**Implementation:**

- No server-side sessions
- Authentication via tokens (JWT) sent with each request
- Client maintains application state
- Enables horizontal scaling (any server can handle any request)

```python
# Stateless - Token in every request
headers = {"Authorization": "Bearer eyJhbGc..."}
requests.get("/api/users", headers=headers)

# NOT stateless - Server stores session
session['user_id'] = 123  # Bad for REST
```

---

### Q4: How do you handle API versioning?

**Answer:** Three common approaches:

1. **URI Versioning** (Most Popular)

```python
/api/v1/users
/api/v2/users
```

2. **Header Versioning**

```python
Accept: application/vnd.api.v1+json
```

3. **Query Parameter**

```python
/api/users?version=1
```

**Best Practice**: URI versioning - explicit, easy to document, works with browser testing.

---

### Q5: What's the difference between 401 and 403?

**Answer:**

- **401 Unauthorized**: Authentication required or failed
    - Missing token
    - Invalid credentials
    - Expired token
- **403 Forbidden**: Authenticated but lacks permission
    - Valid login, but not authorized for this resource
    - User role insufficient (e.g., regular user accessing admin endpoint)

```python
# 401 - No/invalid token
@jwt_required()
def get(self):
    pass  # Returns 401 if no token

# 403 - Valid token, insufficient role
@jwt_required()
def delete(self):
    user = get_jwt_identity()
    if user['role'] != 'admin':
        return {"error": "Admin only"}, 403
```

---

### Q6: How do you secure a Flask-RESTful API?

**Answer:**

1. **HTTPS**: Encrypt all traffic
2. **Authentication**: JWT tokens
3. **Input Validation**: Marshmallow/pydantic schemas
4. **Rate Limiting**: Prevent abuse (flask-limiter)
5. **CORS**: Control allowed origins
6. **SQL Injection**: Use ORM parameterized queries
7. **Secrets Management**: Environment variables, never hardcode
8. **Error Handling**: Don't leak stack traces
9. **Security Headers**: flask-talisman

```python
# Example secure setup
from flask_talisman import Talisman

Talisman(app, force_https=True)
limiter = Limiter(app, default_limits=["100/hour"])

@jwt_required()
@limiter.limit("10/minute")
def get(self):
    # Validate input
    schema = UserSchema()
    data = schema.load(request.get_json())
    # Use parameterized queries
    user = User.query.filter_by(id=data['id']).first()
```

---

### Q7: What's the difference between Flask and Flask-RESTful?

**Answer:**

|Feature|Flask|Flask-RESTful|
|---|---|---|
|**Purpose**|General web framework|REST API specific|
|**Routing**|`@app.route()` decorators|Resource classes|
|**Organization**|Function-based views|Class-based views|
|**Parsing**|Manual `request.get_json()`|Built-in `reqparse`|
|**Output**|Manual `jsonify()`|Automatic marshalling|

**Example:**

```python
# Pure Flask
@app.route('/users/<int:uid>', methods=['GET'])
def get_user(uid):
    return jsonify({"user": USERS[uid]}), 200

# Flask-RESTful
class UserResource(Resource):
    def get(self, uid):
        return USERS[uid], 200
```

Flask-RESTful reduces boilerplate and enforces REST conventions.

---

### Q8: How do you handle database connections?

**Answer:** Use **Flask-SQLAlchemy** for ORM:

```python
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@localhost/db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    
# Context manager ensures proper connection handling
with app.app_context():
    db.create_all()
```

**Benefits:**

- Connection pooling
- Automatic transaction management
- SQL injection prevention
- Database agnostic (switch DB easily)

---

### Q9: Explain HTTP status code ranges

**Answer:**

|Range|Meaning|Examples|
|---|---|---|
|**1xx**|Informational|101 Switching Protocols|
|**2xx**|Success|200 OK, 201 Created, 204 No Content|
|**3xx**|Redirection|301 Moved, 304 Not Modified|
|**4xx**|Client Error|400 Bad Request, 401 Unauthorized, 404 Not Found|
|**5xx**|Server Error|500 Internal Error, 503 Unavailable|

**Remember:**

- 2xx = Good job, client!
- 3xx = Look elsewhere
- 4xx = Client messed up
- 5xx = Server messed up

---

### Q10: How do you test Flask-RESTful APIs?

**Answer:**

**Using pytest + Flask test client:**

```python
import pytest
from app import app, db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_get_user(client):
    response = client.get('/api/v1/users/1')
    assert response.status_code == 200
    assert response.json['name'] == 'John'

def test_create_user(client):
    response = client.post('/api/v1/users',
        json={"name": "Jane", "email": "jane@example.com"},
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 201
    assert 'id' in response.json

def test_authentication(client):
    response = client.get('/api/v1/protected')
    assert response.status_code == 401  # No token
```

**Tools:**

- pytest: Test framework
- coverage: Code coverage
- Postman/Insomnia: Manual testing
- locust: Load testing

---

### Q11: What are common API design mistakes?

**Answer:**

1. **Not using proper status codes**
    - Bad: Always returning 200, even for errors
    - Good: 404 for not found, 400 for bad input
2. **Inconsistent naming**
    - Bad: `/getUsers`, `/user/delete`, `/update-product`
    - Good: `/users` (GET), `/users/{id}` (DELETE), `/products/{id}` (PUT)
3. **No versioning**
    - Bad: Breaking changes affect all clients
    - Good: `/api/v1/users` → `/api/v2/users`
4. **Exposing internal implementation**
    - Bad: `/api/database/users/select?id=1`
    - Good: `/api/users/1`
5. **No input validation**
    - Bad: Trusting all client input
    - Good: Schema validation, sanitization
6. **Poor error messages**
    - Bad: `{"error": "Error"}`
    - Good: `{"error": "Invalid email format", "field": "email"}`

---

### Q12: How do you implement pagination?

**Answer:**

**Query Parameters Approach:**

```python
class UserListResource(Resource):
    def get(self):
        # Get pagination params
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Calculate slice
        start = (page - 1) * per_page
        end = start + per_page
        
        # Get data
        all_users = list(USERS.values())
        users = all_users[start:end]
        
        return {
            "data": users,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total_items": len(all_users),
                "total_pages": (len(all_users) + per_page - 1) // per_page
            }
        }, 200

# Usage: GET /api/users?page=2&per_page=20
```

**With SQLAlchemy:**

```python
def get(self):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    pagination = User.query.paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )
    
    return {
        "data": [user.to_dict() for user in pagination.items],
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": pagination.total,
            "pages": pagination.pages
        }
    }, 200
```

---

### Q13: What is HATEOAS?

**Answer:** **HATEOAS** (Hypermedia As The Engine Of Application State) - REST constraint where responses include links to related resources.

```python
def get(self, uid):
    user = USERS.get(uid)
    if not user:
        return {"error": "Not found"}, 404
    
    # Add hypermedia links
    return {
        "id": user['id'],
        "name": user['name'],
        "email": user['email'],
        "_links": {
            "self": f"/api/v1/users/{uid}",
            "orders": f"/api/v1/users/{uid}/orders",
            "update": {
                "href": f"/api/v1/users/{uid}",
                "method": "PUT"
            },
            "delete": {
                "href": f"/api/v1/users/{uid}",
                "method": "DELETE"
            }
        }
    }, 200
```

**Benefits:**

- Self-documenting API
- Client doesn't need to construct URLs
- Server can change URLs without breaking clients

---

### Q14: How do you handle file uploads in REST API?

**Answer:**

```python
from werkzeug.utils import secure_filename
import os

app.config['UPLOAD_FOLDER'] = '/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

class FileUploadResource(Resource):
    def post(self):
        # Check if file in request
        if 'file' not in request.files:
            return {"error": "No file provided"}, 400
        
        file = request.files['file']
        
        # Check if file selected
        if file.filename == '':
            return {"error": "No file selected"}, 400
        
        # Validate file type
        allowed_extensions = {'pdf', 'png', 'jpg', 'jpeg'}
        if not ('.' in file.filename and 
                file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
            return {"error": "Invalid file type"}, 400
        
        # Secure filename and save
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        return {
            "message": "File uploaded successfully",
            "filename": filename,
            "url": f"/uploads/{filename}"
        }, 201

# Testing with curl:
# curl -X POST -F "file=@document.pdf" http://localhost:5000/api/upload
```

---

### Q15: Explain Content Negotiation

**Answer:** Server provides different representations based on client's `Accept` header.

```python
from flask import request

class UserResource(Resource):
    def get(self, uid):
        user = USERS.get(uid)
        if not user:
            return {"error": "Not found"}, 404
        
        # Check Accept header
        accept = request.headers.get('Accept', 'application/json')
        
        if 'application/xml' in accept:
            # Return XML
            xml = f"<user><id>{user['id']}</id><name>{user['name']}</name></user>"
            return Response(xml, mimetype='application/xml')
        
        elif 'application/json' in accept:
            # Return JSON (default)
            return user, 200
        
        else:
            return {"error": "Unsupported media type"}, 415

# Usage:
# curl -H "Accept: application/xml" http://localhost:5000/api/users/1
# curl -H "Accept: application/json" http://localhost:5000/api/users/1
```

---

## Setup & Testing Commands

### Windows Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install flask flask-restful flask-cors flask-sqlalchemy flask-jwt-extended marshmallow

# Create requirements.txt
pip freeze > requirements.txt

# Run application
python app.py

# Run with environment variables
set FLASK_ENV=development
set FLASK_APP=app.py
flask run

# Run on specific port
python app.py --port 8000
```

### Linux/Mac Setup

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install flask flask-restful flask-cors flask-sqlalchemy flask-jwt-extended marshmallow

# Run with environment variables
export FLASK_ENV=development
export FLASK_APP=app.py
flask run
```

### Testing with curl (Windows/Linux/Mac)

#### GET Requests

```bash
# Get single user
curl http://127.0.0.1:5000/api/v1/users/123

# Get all users
curl http://127.0.0.1:5000/api/v1/users

# Get with pagination
curl "http://127.0.0.1:5000/api/v1/users?page=2&per_page=10"

# Get with authentication
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" http://127.0.0.1:5000/api/v1/users/123
```

#### POST Requests (Create)

```bash
# Create user
curl -X POST http://127.0.0.1:5000/api/v1/users \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"John Doe\",\"email\":\"john@example.com\",\"age\":30}"

# Create with authentication
curl -X POST http://127.0.0.1:5000/api/v1/users \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d "{\"name\":\"Jane\",\"email\":\"jane@example.com\"}"

# Login (get JWT token)
curl -X POST http://127.0.0.1:5000/api/v1/login \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"admin\",\"password\":\"secret\"}"
```

#### PUT Requests (Replace)

```bash
# Replace entire user
curl -X PUT http://127.0.0.1:5000/api/v1/users/123 \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"Jane Doe\",\"email\":\"jane@example.com\",\"age\":25}"
```

#### PATCH Requests (Partial Update)

```bash
# Update only name
curl -X PATCH http://127.0.0.1:5000/api/v1/users/123 \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"Jane Smith\"}"

# Update only age
curl -X PATCH http://127.0.0.1:5000/api/v1/users/123 \
  -H "Content-Type: application/json" \
  -d "{\"age\":31}"
```

#### DELETE Requests

```bash
# Delete user
curl -X DELETE http://127.0.0.1:5000/api/v1/users/123

# Delete with authentication
curl -X DELETE http://127.0.0.1:5000/api/v1/users/123 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

#### Testing File Upload

```bash
# Upload file
curl -X POST http://127.0.0.1:5000/api/v1/upload \
  -F "file=@/path/to/document.pdf"

# Upload with metadata
curl -X POST http://127.0.0.1:5000/api/v1/upload \
  -F "file=@image.jpg" \
  -F "description=Profile picture"
```

---

## Testing with Python Requests Library

```python
import requests

BASE_URL = "http://127.0.0.1:5000/api/v1"

# GET request
response = requests.get(f"{BASE_URL}/users/123")
print(response.status_code)
print(response.json())

# POST request
data = {"name": "John", "email": "john@example.com"}
response = requests.post(f"{BASE_URL}/users", json=data)
print(response.json())

# PUT request
data = {"name": "Jane", "email": "jane@example.com", "age": 25}
response = requests.put(f"{BASE_URL}/users/123", json=data)

# PATCH request
data = {"age": 26}
response = requests.patch(f"{BASE_URL}/users/123", json=data)

# DELETE request
response = requests.delete(f"{BASE_URL}/users/123")

# With authentication
headers = {"Authorization": "Bearer YOUR_JWT_TOKEN"}
response = requests.get(f"{BASE_URL}/users/123", headers=headers)

# File upload
files = {"file": open("document.pdf", "rb")}
response = requests.post(f"{BASE_URL}/upload", files=files)
```

---

##  Testing with Pytest

### Basic Test Structure

```python
# tests/test_users.py
import pytest
from app import app, db, USERS

@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Seed test data
            USERS['1'] = {'id': '1', 'name': 'Test User', 'email': 'test@example.com'}
        yield client
        with app.app_context():
            db.drop_all()
            USERS.clear()

def test_get_user_success(client):
    """Test successful user retrieval"""
    response = client.get('/api/v1/users/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'Test User'
    assert data['email'] == 'test@example.com'

def test_get_user_not_found(client):
    """Test user not found"""
    response = client.get('/api/v1/users/999')
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data

def test_create_user(client):
    """Test user creation"""
    payload = {
        'name': 'New User',
        'email': 'new@example.com',
        'age': 25
    }
    response = client.post(
        '/api/v1/users',
        json=payload,
        content_type='application/json'
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == 'New User'
    assert 'id' in data

def test_create_user_validation_error(client):
    """Test validation on user creation"""
    payload = {'name': 'John'}  # Missing required email
    response = client.post('/api/v1/users', json=payload)
    assert response.status_code == 400

def test_update_user(client):
    """Test user update"""
    payload = {'name': 'Updated Name'}
    response = client.patch('/api/v1/users/1', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'Updated Name'

def test_delete_user(client):
    """Test user deletion"""
    response = client.delete('/api/v1/users/1')
    assert response.status_code == 204
    
    # Verify deletion
    response = client.get('/api/v1/users/1')
    assert response.status_code == 404

def test_list_users_pagination(client):
    """Test pagination"""
    # Add more users
    for i in range(2, 12):
        USERS[str(i)] = {'id': str(i), 'name': f'User {i}'}
    
    response = client.get('/api/v1/users?page=1&per_page=5')
    assert response.status_code == 200
    data = response.get_json()
    assert data['page'] == 1
    assert data['per_page'] == 5
    assert len(data['users']) == 5

def test_authentication_required(client):
    """Test protected endpoint without token"""
    response = client.get('/api/v1/protected')
    assert response.status_code == 401

# Run tests
# pytest tests/test_users.py -v
# pytest tests/test_users.py --cov=app --cov-report=html
```

---

##  Performance & Optimization Tips

### 1. Database Query Optimization

```python
# Bad - N+1 Query Problem
def get(self):
    users = User.query.all()
    for user in users:
        user.orders  # Triggers separate query for each user
    
# Good - Eager Loading
def get(self):
    users = User.query.options(
        db.joinedload(User.orders)
    ).all()
```

### 2. Caching

```python
from flask_caching import Cache

cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': 'redis://localhost:6379/0'
})

class UserResource(Resource):
    @cache.cached(timeout=300, query_string=True)
    def get(self, uid):
        # Cached for 5 minutes
        return USERS.get(uid), 200
    
    def put(self, uid):
        USERS[uid] = request.get_json()
        cache.delete(f'view//api/v1/users/{uid}')  # Invalidate cache
        return USERS[uid], 201
```

### 3. Response Compression

```python
from flask_compress import Compress

Compress(app)  # Automatically compresses responses > 500 bytes
```

### 4. Connection Pooling

```python
# PostgreSQL with connection pool
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@localhost/db'
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,
    'pool_recycle': 3600,
    'pool_pre_ping': True
}
```

### 5. Async Support (Flask 2.0+)

```python
from flask import Flask
import asyncio

app = Flask(__name__)

class UserResource(Resource):
    async def get(self, uid):
        # Async database query
        user = await fetch_user_async(uid)
        return user, 200
```

---

##  Security Checklist

### Essential Security Measures

```python
# 1. HTTPS Only (Production)
from flask_talisman import Talisman
Talisman(app, force_https=True)

# 2. Security Headers
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response

# 3. CSRF Protection for stateful endpoints
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)

# 4. Rate Limiting
from flask_limiter import Limiter
limiter = Limiter(
    app=app,
    key_func=lambda: request.headers.get('X-API-Key', 'anonymous'),
    default_limits=["1000 per day", "100 per hour"]
)

# 5. Input Sanitization
from bleach import clean

def sanitize_input(text):
    return clean(text, tags=[], strip=True)

# 6. SQL Injection Prevention (Use ORM)
# Bad
query = f"SELECT * FROM users WHERE id = {user_id}"  # NEVER DO THIS

# Good
user = User.query.filter_by(id=user_id).first()

# 7. Password Hashing
from werkzeug.security import generate_password_hash, check_password_hash

hashed = generate_password_hash('password123')
is_valid = check_password_hash(hashed, 'password123')

# 8. Sensitive Data in Environment
# .env file
SECRET_KEY=your-secret-key-here
DATABASE_URI=postgresql://user:pass@localhost/db
JWT_SECRET_KEY=jwt-secret

# Load in app
from dotenv import load_dotenv
load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
```

---

## Monitoring & Logging

### Structured Logging

```python
import logging
from logging.handlers import RotatingFileHandler
import json
from datetime import datetime

# JSON formatter
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        if hasattr(record, 'user_id'):
            log_data['user_id'] = record.user_id
        return json.dumps(log_data)

# Setup logging
handler = RotatingFileHandler('app.log', maxBytes=10000000, backupCount=5)
handler.setFormatter(JsonFormatter())
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

# Usage in endpoints
class UserResource(Resource):
    def get(self, uid):
        app.logger.info(f'User {uid} retrieved', extra={'user_id': uid})
        return USERS.get(uid), 200
    
    def delete(self, uid):
        try:
            del USERS[uid]
            app.logger.info(f'User {uid} deleted', extra={'user_id': uid})
            return "", 204
        except Exception as e:
            app.logger.error(f'Delete failed: {str(e)}', extra={'user_id': uid})
            return {"error": "Delete failed"}, 500
```

### Request/Response Logging Middleware

```python
from time import time

@app.before_request
def log_request():
    request.start_time = time()
    app.logger.info(f'{request.method} {request.path}', extra={
        'ip': request.remote_addr,
        'user_agent': request.user_agent.string
    })

@app.after_request
def log_response(response):
    duration = time() - request.start_time
    app.logger.info(f'Response: {response.status_code}', extra={
        'duration_ms': round(duration * 1000, 2),
        'path': request.path
    })
    return response
```

### Health Check Endpoint

```python
class HealthCheckResource(Resource):
    def get(self):
        """Check API health"""
        checks = {
            'api': 'ok',
            'timestamp': datetime.utcnow().isoformat()
        }
        
        # Check database
        try:
            db.session.execute('SELECT 1')
            checks['database'] = 'ok'
        except Exception as e:
            checks['database'] = 'error'
            checks['database_error'] = str(e)
            return checks, 503
        
        return checks, 200

api.add_resource(HealthCheckResource, '/health')
```

---

## Common Patterns & Solutions

### 1. Soft Delete Pattern

```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    deleted_at = db.Column(db.DateTime, nullable=True)
    
    @property
    def is_deleted(self):
        return self.deleted_at is not None

class UserResource(Resource):
    def get(self, uid):
        user = User.query.filter_by(id=uid, deleted_at=None).first()
        if not user:
            return {"error": "Not found"}, 404
        return user.to_dict(), 200
    
    def delete(self, uid):
        user = User.query.get_or_404(uid)
        user.deleted_at = datetime.utcnow()  # Soft delete
        db.session.commit()
        return "", 204
```

### 2. Filtering & Search

```python
class UserListResource(Resource):
    def get(self):
        # Get query parameters
        name = request.args.get('name')
        email = request.args.get('email')
        min_age = request.args.get('min_age', type=int)
        max_age = request.args.get('max_age', type=int)
        sort_by = request.args.get('sort_by', 'id')
        order = request.args.get('order', 'asc')
        
        # Build query
        query = User.query
        
        if name:
            query = query.filter(User.name.ilike(f'%{name}%'))
        if email:
            query = query.filter(User.email.ilike(f'%{email}%'))
        if min_age:
            query = query.filter(User.age >= min_age)
        if max_age:
            query = query.filter(User.age <= max_age)
        
        # Sorting
        if order == 'desc':
            query = query.order_by(db.desc(getattr(User, sort_by)))
        else:
            query = query.order_by(getattr(User, sort_by))
        
        users = query.all()
        return [user.to_dict() for user in users], 200

# Usage: GET /api/users?name=john&min_age=25&sort_by=age&order=desc
```

### 3. Nested Resources

```python
# Get user's orders: GET /api/users/123/orders
class UserOrdersResource(Resource):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        orders = Order.query.filter_by(user_id=user_id).all()
        return {
            'user': user.to_dict(),
            'orders': [order.to_dict() for order in orders]
        }, 200
    
    def post(self, user_id):
        user = User.query.get_or_404(user_id)
        data = request.get_json()
        order = Order(user_id=user_id, **data)
        db.session.add(order)
        db.session.commit()
        return order.to_dict(), 201

api.add_resource(UserOrdersResource, '/api/v1/users/<int:user_id>/orders')
```

### 4. Bulk Operations

```python
class BulkUserResource(Resource):
    def post(self):
        """Create multiple users at once"""
        data = request.get_json()
        users_data = data.get('users', [])
        
        created_users = []
        errors = []
        
        for idx, user_data in enumerate(users_data):
            try:
                schema = UserSchema()
                validated = schema.load(user_data)
                user = User(**validated)
                db.session.add(user)
                created_users.append(user)
            except ValidationError as e:
                errors.append({'index': idx, 'errors': e.messages})
        
        if errors:
            db.session.rollback()
            return {'errors': errors}, 400
        
        db.session.commit()
        return {
            'created': len(created_users),
            'users': [u.to_dict() for u in created_users]
        }, 201
    
    def delete(self):
        """Delete multiple users"""
        data = request.get_json()
        user_ids = data.get('ids', [])
        
        deleted = User.query.filter(User.id.in_(user_ids)).delete(synchronize_session=False)
        db.session.commit()
        
        return {'deleted': deleted}, 200

api.add_resource(BulkUserResource, '/api/v1/users/bulk')
```

### 5. API Documentation (Swagger/OpenAPI)

```python
from flask_restx import Api, Resource, fields

api = Api(
    app,
    version='1.0',
    title='User API',
    description='A simple User API',
    doc='/docs'  # Swagger UI at /docs
)

ns = api.namespace('users', description='User operations')

user_model = api.model('User', {
    'id': fields.Integer(readonly=True, description='User ID'),
    'name': fields.String(required=True, description='User name'),
    'email': fields.String(required=True, description='User email'),
    'age': fields.Integer(description='User age')
})

@ns.route('/')
class UserListResource(Resource):
    @ns.doc('list_users')
    @ns.marshal_list_with(user_model)
    def get(self):
        """List all users"""
        return list(USERS.values())
    
    @ns.doc('create_user')
    @ns.expect(user_model)
    @ns.marshal_with(user_model, code=201)
    def post(self):
        """Create a new user"""
        return api.payload, 201

# Access docs at: http://localhost:5000/docs
```

---

## Deployment Checklist

### Production Configuration

```python
# config.py
import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'

class ProductionConfig(Config):
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_POOL_RECYCLE = 3600

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}

# app.py
env = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[env])
```

### Requirements.txt (Production)

```
Flask==3.0.0
Flask-RESTful==0.3.10
Flask-SQLAlchemy==3.1.1
Flask-JWT-Extended==4.6.0
Flask-CORS==4.0.0
Flask-Limiter==3.5.0
Flask-Caching==2.1.0
marshmallow==3.20.1
python-dotenv==1.0.0
psycopg2-binary==2.9.9
gunicorn==21.2.0
redis==5.0.1
```

### Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - DATABASE_URI=postgresql://user:pass@db:5432/mydb
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - db
      - redis
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=mydb
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

### WSGI Server (Gunicorn)

```bash
# Run with gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 app:app

# gunicorn_config.py
bind = "0.0.0.0:5000"
workers = 4
worker_class = "sync"
timeout = 120
accesslog = "-"
errorlog = "-"
loglevel = "info"
```

---

## Quick Reference Summary

### HTTP Methods

|Method|Action|Idempotent|Body|Success Code|
|---|---|---|---|---|
|GET|Read|✅|❌|200|
|POST|Create|❌|✅|201|
|PUT|Replace|✅|✅|200/201|
|PATCH|Update|❌|✅|200|
|DELETE|Remove|✅|❌|204|

### Status Codes Cheatsheet

- **200**: OK
- **201**: Created
- **204**: No Content
- **400**: Bad Request
- **401**: Unauthorized
- **403**: Forbidden
- **404**: Not Found
- **409**: Conflict
- **422**: Validation Failed
- **500**: Server Error

### Key Concepts

- **Resource**: Entity (User, Product)
- **Endpoint**: URL path (/api/users)
- **Stateless**: No server-side session
- **Idempotent**: Same request = same result
- **HATEOAS**: Include links in responses
- **Content Negotiation**: Different formats (JSON/XML)

---

##  Interview Pro Tips

1. **Always mention error handling** - Interviewers love candidates who think about edge cases
2. **Security first** - Bring up authentication, validation, HTTPS without being asked
3. **Explain trade-offs** - "PUT is simpler but PATCH is more efficient for large objects"
4. **Real-world examples** - "In my last project, we used JWT for stateless auth across microservices"
5. **Ask clarifying questions** - "Are we optimizing for read or write performance?"
6. **Show scalability thinking** - Mention caching, connection pooling, async
7. **Know the basics cold** - Status codes, HTTP methods, REST constraints
8. **Be specific** - Don't just say "validation" - mention Marshmallow, pydantic, reqparse


---
**Last Updated**: November 2025
**Status**: Interview Ready ✅
