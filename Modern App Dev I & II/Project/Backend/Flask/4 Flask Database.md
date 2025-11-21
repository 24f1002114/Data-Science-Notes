# Flask Database - SQLAlchemy & Migrations

## 1. Core Concepts

```mermaid
flowchart LR
    A[Python Class] -->|SQLAlchemy| B[Database Table]
    B -->|Query| C[Python Objects]
    
    D[Model Changes] -->|Flask-Migrate| E[Migration Files]
    E -->|Apply| F[Update Database]
    
    style A fill:#c8e6c9
    style B fill:#bbdefb
    style E fill:#fff9c4
```

|Concept|Description|
|---|---|
|**ORM**|Object-Relational Mapping (Python ↔ SQL)|
|**Model**|Python class = Database table|
|**Migration**|Track & apply database changes|
|**Query**|Retrieve data using Python (not SQL)|

---

## 2. SQLAlchemy vs Raw SQL

### Raw SQL (sqlite3)

```python
import sqlite3
conn = sqlite3.connect('db.sqlite')
cursor = conn.cursor()

# Create table
cursor.execute('''CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT,
    email TEXT
)''')

# Insert
cursor.execute('INSERT INTO users VALUES (?, ?, ?)', 
               (1, 'alice', 'alice@example.com'))

# Query
cursor.execute('SELECT * FROM users WHERE username = ?', ('alice',))
users = cursor.fetchall()
```

### SQLAlchemy (ORM)

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

# Define model (class = table)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))

# Create tables
db.create_all()

# Insert
user = User(username='alice', email='alice@example.com')
db.session.add(user)
db.session.commit()

# Query
users = User.query.filter_by(username='alice').all()
```

**Why ORM?**

- ✅ Write Python, not SQL
- ✅ Database agnostic (SQLite, PostgreSQL, MySQL)
- ✅ Automatic type conversion
- ✅ Built-in security (SQL injection prevention)
- ✅ Easier relationships (User.posts)

---

## 3. Setup & Configuration

### Installation

```bash
pip install flask-sqlalchemy flask-migrate
```

### Basic Setup

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable overhead

db = SQLAlchemy(app)
```

### Database URIs

```python
# SQLite (development)
'sqlite:///app.db'  # Relative path
'sqlite:////tmp/app.db'  # Absolute path

# PostgreSQL (production)
'postgresql://user:password@localhost/dbname'

# MySQL
'mysql://user:password@localhost/dbname'
```

---

## 4. Models (Defining Tables)

```mermaid
classDiagram
    class User {
        +int id
        +string username
        +string email
        +datetime created_at
        +__repr__()
    }
    
    class Post {
        +int id
        +string title
        +text content
        +int user_id
    }
    
    User "1" --> "*" Post : has many
```

### Basic Model

```python
from datetime import datetime

class User(db.Model):
    # Table name (optional, defaults to lowercase class name)
    __tablename__ = 'users'
    
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Representation (for debugging)
    def __repr__(self):
        return f'<User {self.username}>'
```

### Column Types

```python
db.Integer          # 1, 2, 3
db.String(80)       # 'alice' (max 80 chars)
db.Text             # Long text (no limit)
db.Boolean          # True/False
db.DateTime         # datetime.utcnow()
db.Float            # 3.14
db.JSON             # {'key': 'value'} (PostgreSQL/SQLite 3.9+)
```

### Column Options

```python
primary_key=True       # Primary key
unique=True            # No duplicates
nullable=False         # Required (NOT NULL)
default='value'        # Default value
index=True             # Create index (faster queries)
```

---

## 5. CRUD Operations

### Create

```python
# Create new user
user = User(username='alice', email='alice@example.com')

# Add to session
db.session.add(user)

# Save to database
db.session.commit()
```

### Read (Query)

```python
# Get all
users = User.query.all()

# Get by ID
user = User.query.get(1)              # Returns None if not found
user = User.query.get_or_404(1)       # Returns 404 error if not found

# Get first
user = User.query.first()             # First user or None
user = User.query.first_or_404()      # First user or 404 error

# Filter
users = User.query.filter_by(username='alice').all()
user = User.query.filter_by(username='alice').first()

# Complex filters
from sqlalchemy import or_, and_
users = User.query.filter(
    or_(User.username == 'alice', User.email.like('%@gmail.com'))
).all()

users = User.query.filter(User.id.in_([1, 2, 3])).all()  # IN clause

# Order
users = User.query.order_by(User.created_at.desc()).all()

# Limit & Offset
users = User.query.limit(10).all()
users = User.query.offset(5).limit(10).all()  # Skip 5, get 10

# Distinct
usernames = User.query.with_entities(User.username).distinct().all()

# Count
count = User.query.count()
```

### Update

```python
# Method 1: Get object, modify, commit
user = User.query.get(1)
user.email = 'newemail@example.com'
db.session.commit()

# Method 2: Bulk update
User.query.filter_by(username='alice').update({'email': 'new@example.com'})
db.session.commit()
```

### Delete

```python
# Method 1: Get object, delete, commit
user = User.query.get(1)
db.session.delete(user)
db.session.commit()

# Method 2: Bulk delete
User.query.filter_by(username='alice').delete()
db.session.commit()
```

---

## 6. Relationships

```mermaid
graph TB
    subgraph "One-to-Many"
        U1[User] -->|has many| P1[Post]
        U1 -->|has many| P2[Post]
        U1 -->|has many| P3[Post]
    end
    
    subgraph "Many-to-Many"
        S1[Student] -.->|enrolls| C1[Course]
        S1 -.->|enrolls| C2[Course]
        S2[Student] -.->|enrolls| C1
        S2 -.->|enrolls| C2
    end
    
    style U1 fill:#c8e6c9
    style P1 fill:#bbdefb
    style P2 fill:#bbdefb
    style P3 fill:#bbdefb
```

### One-to-Many (User → Posts)

```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    
    # Relationship
    posts = db.relationship('Post', backref='author', lazy=True)
    # backref: Post.author gives the User object
    # lazy=True: Load posts only when accessed


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    content = db.Column(db.Text)
    
    # Foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
```

**Usage:**

```python
# Create
user = User(username='alice')
post = Post(title='Hello', content='World', author=user)
db.session.add(post)
db.session.commit()

# Query
user = User.query.get(1)
print(user.posts)  # List of all posts by user

post = Post.query.get(1)
print(post.author)  # User object
print(post.author.username)  # 'alice'
```

### Many-to-Many (Students ↔ Courses)

```python
# Association table
enrollments = db.Table('enrollments',
    db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'))
)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    courses = db.relationship('Course', secondary=enrollments, backref='students')

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
```

**Usage:**

```python
# Create
student = Student(name='Alice')
course1 = Course(name='Math')
course2 = Course(name='Physics')

student.courses.append(course1)
student.courses.append(course2)
db.session.commit()

# Query
student = Student.query.get(1)
print(student.courses)  # [Math, Physics]

course = Course.query.get(1)
print(course.students)  # [Alice, Bob, ...]
```

---

## 7. Flask-Migrate (Database Migrations)

**Why?** Track database changes like Git for code.

```mermaid
flowchart LR
    A[Initial DB] -->|Add column| B[Migration 1]
    B -->|Add table| C[Migration 2]
    C -->|Modify column| D[Migration 3]
    
    E[Empty DB] -->|Apply migrations| D
    
    style A fill:#ffcdd2
    style D fill:#c8e6c9
```

### Setup

```python
from flask_migrate import Migrate

app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
```

### Commands

```bash
# 1. Initialize migrations folder (once)
flask db init

# 2. Create migration (after model changes)
flask db migrate -m "Add email column"

# 3. Apply migration to database
flask db upgrade

# 4. Undo last migration
flask db downgrade

# 5. Show migration history
flask db history

# 6. Show current version
flask db current
```

### Workflow Example

```bash
# 1. Create initial models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))

# 2. Initialize
flask db init

# 3. Create first migration
flask db migrate -m "Initial migration"
# Creates: migrations/versions/xxxx_initial_migration.py

# 4. Apply to database
flask db upgrade

# 5. Add new column
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))  # NEW!

# 6. Create migration for change
flask db migrate -m "Add email column"

# 7. Apply change
flask db upgrade
```

---

## 8. Complete Example App

```python
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# ============= MODELS =============
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    posts = db.relationship('Post', backref='author', lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f'<Post {self.title}>'

# ============= ROUTES =============
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    user = User(username=data['username'], email=data['email'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'id': user.id, 'username': user.username}), 201

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': u.id, 'username': u.username} for u in users])

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify({
        'id': user.id,
        'username': user.username,
        'posts': [{'id': p.id, 'title': p.title} for p in user.posts]
    })

@app.route('/posts', methods=['POST'])
def create_post():
    data = request.json
    post = Post(title=data['title'], content=data['content'], 
                user_id=data['user_id'])
    db.session.add(post)
    db.session.commit()
    return jsonify({'id': post.id, 'title': post.title}), 201

if __name__ == '__main__':
    app.run(debug=True)
```

### Run Instructions

```bash
# 1. Install
pip install flask flask-sqlalchemy flask-migrate

# 2. Initialize migrations
flask db init

# 3. Create migration
flask db migrate -m "Initial migration"

# 4. Apply migration
flask db upgrade

# 5. Run app
python app.py

# 6. Test API
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"username":"alice", "email":"alice@example.com"}'
```

---

## 9. Common Patterns

### Get or Create

```python
def get_or_create(model, **kwargs):
    instance = model.query.filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        db.session.add(instance)
        db.session.commit()
        return instance

user = get_or_create(User, username='alice', email='alice@example.com')
```

### Pagination

```python
@app.route('/users')
def users():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    users = User.query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'users': [{'id': u.id, 'username': u.username} for u in users.items],
        'total': users.total,
        'pages': users.pages,
        'current_page': users.page
    })
```

### Search

```python
@app.route('/search')
def search():
    query = request.args.get('q', '')
    users = User.query.filter(
        User.username.like(f'%{query}%')
    ).all()
    return jsonify([u.username for u in users])
```

---

## 10. Interview Q&A

**Q: What is ORM?**

> Object-Relational Mapping. Converts between Python objects and database tables. Write Python code instead of SQL.

**Q: SQLAlchemy vs raw SQL?**

> SQLAlchemy is database-agnostic, prevents SQL injection, easier relationships. Raw SQL is faster for complex queries.

**Q: What is db.session?**

> Transaction manager. Groups database operations. `commit()` saves changes, `rollback()` undoes them.

**Q: Why use migrations?**

> Track database schema changes over time. Like Git for database structure. Easy to deploy changes to production.

**Q: What is backref?**

> Two-way relationship. `User.posts` and `Post.author` both work.

**Q: Lazy loading?**

> Load related data only when accessed. `lazy=True` (default): load on access. `lazy='subquery'`: load with one query.

**Q: How to handle large datasets?**

> Use pagination (`paginate()`), limit queries, index columns, use `yield_per()` for streaming.

**Q: db.create_all() vs migrations?**

> `create_all()`: Simple, no history, can't modify tables. Migrations: Track changes, can update existing tables.

**Q: What is cascade?**

> Defines what happens to related objects. `cascade='all, delete-orphan'`: Delete posts when user deleted.

**Q: How to optimize queries?**

> Use `joinedload()` for eager loading, add indexes, avoid N+1 queries, use `with_entities()` for specific columns.

---

## 11. Quick Reference

```python
# SETUP
db = SQLAlchemy(app)

# MODEL
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

# CREATE
user = User(name='alice')
db.session.add(user)
db.session.commit()

# READ
User.query.all()
User.query.get(1)
User.query.filter_by(name='alice').first()

# UPDATE
user = User.query.get(1)
user.name = 'bob'
db.session.commit()

# DELETE
db.session.delete(user)
db.session.commit()

# RELATIONSHIP
posts = db.relationship('Post', backref='author')
user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# MIGRATIONS
flask db init
flask db migrate -m "message"
flask db upgrade
```

---

**Last Updated**: November 2025  
**Status**: Interview Ready ✅