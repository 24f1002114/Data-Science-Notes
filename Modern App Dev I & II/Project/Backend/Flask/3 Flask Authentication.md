# Flask Authentication: Interview-Ready Guide

## Core Concepts (Know These!)

|Term|Meaning|Example|
|---|---|---|
|**Authentication**|Verify identity|"Who are you?" → Login|
|**Authorization**|Check permissions|"Can you do this?" → Admin check|
|**Hashing**|One-way password encryption|`password123` → `pbkdf2:sha256:...`|
|**Session**|Track logged-in users|`session['user_id'] = 123`|

---

## The 3 Auth Methods You Must Know

### 1. Sessions (Flask Default) - For Web Apps

**Key Insight: Flask sessions are CLIENT-SIDE!**

```python
session['user_id'] = 123  
# ↓ Data stored IN the cookie, signed with secret_key
# NOT stored on server!
```

**How it works:**

1. You set session data → Flask signs it → Sends as cookie
2. Browser stores cookie with actual data + signature
3. Next request → Flask verifies signature → Reads data
4. No database lookup needed!

### 2. JWT (JSON Web Token) - For APIs

**Key Insight: JWT payload is READABLE by anyone!**

```
eyJhbGc.eyJ1c2VyX2lkIjoxMjN9.signature
  ↓          ↓                    ↓
Header    Payload              Signature
         (base64,              (prevents
         NOT encrypted!)       tampering)
```

```python
# ❌ NEVER store in JWT:
{'password': 'secret', 'api_key': 'sk-123'}

# ✅ Only store:
{'user_id': 123, 'role': 'admin', 'exp': 1234567890}
```

### 3. Flask-Security-Too - For Enterprise Apps

Pre-built everything: registration, email verification, 2FA, password reset, roles.

**Note:** Use `flask-security-too`, NOT `flask-security` (abandoned since 2017).

---

## Quick Comparison

|Feature|Sessions|JWT|Flask-Security-Too|
|---|---|---|---|
|**Storage**|Client cookie|Client token|Server-side|
|**State**|Stateless|Stateless|Stateful|
|**Best For**|Web apps|REST APIs|Enterprise|
|**Revoke**|Hard|Hard (need blacklist)|Easy|
|**Setup**|Built-in|`flask-jwt-extended`|Heavy config|

---

## Password Hashing (Must Know!)

```python
from werkzeug.security import generate_password_hash, check_password_hash

# Registration - Hash before storing
hash = generate_password_hash('password123')
# Returns: 'pbkdf2:sha256:600000$...'

# Login - Verify hash
if check_password_hash(stored_hash, user_input):
    session['user_id'] = user.id
```

**Why hash?**

- ❌ Plain: `password123` → If DB leaked, passwords exposed!
- ✅ Hashed: `pbkdf2:sha256:...` → Useless to attacker (one-way)

---

## Session Flow

```
Login → session['user_id'] = 123 → Cookie sent to browser
                                        ↓
Dashboard ← Check session['user_id'] ← Cookie returned
                                        ↓
Logout → session.clear() → Cookie deleted
```

---

## JWT Flow

```
Login → create_access_token(identity=user_id) → Token returned
                                                      ↓
API Call ← @jwt_required() verifies ← Token in header
                                      Authorization: Bearer <token>
```

---

## Protecting Routes

### With Sessions

```python
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated

@app.route('/dashboard')
@login_required
def dashboard():
    return "Protected content"
```

### With JWT

```python
from flask_jwt_extended import jwt_required, get_jwt_identity

@app.route('/api/data')
@jwt_required()
def data():
    user_id = get_jwt_identity()
    return {'user': user_id}
```

---

## Security Checklist

```python
# 1. Strong secret key
app.secret_key = os.urandom(32)

# 2. Secure cookies
app.config['SESSION_COOKIE_HTTPONLY'] = True   # No JS access
app.config['SESSION_COOKIE_SECURE'] = True     # HTTPS only
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF protection

# 3. Session fixation prevention
session.clear()  # Call before login

# 4. Password hashing (automatic salt)
generate_password_hash(password)

# 5. Rate limiting
from flask_limiter import Limiter
@limiter.limit("5 per minute")
```

---

## Interview Quick Answers

**Q: Authentication vs Authorization?**

> Auth**n** = Who are you? (login) | Auth**z** = What can you do? (permissions)

**Q: Where are Flask sessions stored?**

> Client-side in signed cookies. Data is IN the cookie, not on server!

**Q: Why hash passwords?**

> One-way encryption with salt. If DB leaks, hashes are useless to attackers.

**Q: Sessions vs JWT?**

> Sessions: Simple, for web apps. JWT: Stateless, for APIs/mobile.

**Q: Can you read JWT payload?**

> Yes! It's base64, NOT encrypted. Never store passwords/secrets in JWT.

**Q: How to revoke JWT?**

> Short expiry (15min) + refresh tokens, or maintain blacklist in Redis.

**Q: What's session fixation?**

> Attack where attacker pre-sets session ID. Prevent with `session.clear()` before login.

**Q: Flask-Security vs Flask-Security-Too?**

> Flask-Security abandoned (2017). Always use Flask-Security-Too (maintained fork).

---

## Decision Tree

```
Building what?
├── Simple Web App → Sessions (flask.session)
├── REST API → JWT (flask-jwt-extended)
├── Need registration/2FA/roles → Flask-Security-Too
└── Social Login → OAuth (authlib)
```

---

## External Resources

- [Flask Sessions Docs](https://flask.palletsprojects.com/en/latest/quickstart/#sessions)
- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/)
- [Flask-Security-Too](https://flask-security-too.readthedocs.io/)
- [Werkzeug Security](https://werkzeug.palletsprojects.com/en/latest/utils/#module-werkzeug.security)
- [JWT.io](https://jwt.io/) - Decode & debug JWTs

```python
"""
Flask Authentication Complete Example
Covers: Sessions, Password Hashing, Login/Logout, Protected Routes
"""

from flask import Flask, request, redirect, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import sqlite3

app = Flask(__name__)
app.secret_key = 'change-this-in-production'  # Signs session cookies

# Secure cookie settings
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# ============ DATABASE ============
def get_db():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )''')
    # Create default admin user
    try:
        conn.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)',
                    ('admin', generate_password_hash('admin123')))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # User exists
    conn.close()

# ============ DECORATOR ============
def login_required(f):
    """Protect routes - redirect to login if not authenticated"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first')
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated

# ============ ROUTES ============
@app.route('/')
def index():
    if 'user_id' in session:
        return f'''
            <h2>Welcome {session["username"]}!</h2>
            <a href="/dashboard">Dashboard</a> | <a href="/logout">Logout</a>
        '''
    return '<a href="/login">Login</a> | <a href="/register">Register</a>'

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register new user with hashed password"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if len(password) < 6:
            flash('Password must be at least 6 characters')
            return redirect('/register')
        
        conn = get_db()
        try:
            # Hash password before storing
            hash = generate_password_hash(password)
            conn.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)',
                        (username, hash))
            conn.commit()
            flash('Registered! Please login.')
            return redirect('/login')
        except sqlite3.IntegrityError:
            flash('Username already exists')
        finally:
            conn.close()
    
    return '''
        <h2>Register</h2>
        <form method="post">
            <input name="username" placeholder="Username" required><br><br>
            <input name="password" type="password" placeholder="Password" required><br><br>
            <button>Register</button>
        </form>
        <p><a href="/login">Already have account? Login</a></p>
    '''

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Verify credentials and create session"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE username = ?',
                           (username,)).fetchone()
        conn.close()
        
        # Verify password hash
        if user and check_password_hash(user['password_hash'], password):
            session.clear()  # Prevent session fixation
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Logged in successfully!')
            return redirect('/dashboard')
        
        flash('Invalid username or password')
    
    return '''
        <h2>Login</h2>
        <form method="post">
            <input name="username" placeholder="Username" required><br><br>
            <input name="password" type="password" placeholder="Password" required><br><br>
            <button>Login</button>
        </form>
        <p><a href="/register">Need account? Register</a></p>
        <p><small>Default: admin / admin123</small></p>
    '''

@app.route('/dashboard')
@login_required
def dashboard():
    """Protected route - requires login"""
    return f'''
        <h2>Dashboard</h2>
        <p>Welcome, {session["username"]}! (ID: {session["user_id"]})</p>
        <p>This is a protected page.</p>
        <a href="/">Home</a> | <a href="/logout">Logout</a>
    '''

@app.route('/logout')
def logout():
    """Clear session and redirect"""
    session.clear()
    flash('Logged out successfully')
    return redirect('/login')

# ============ API ENDPOINTS (For testing) ============
@app.route('/api/session')
def api_session():
    """Debug: View current session data"""
    return jsonify({
        'logged_in': 'user_id' in session,
        'user_id': session.get('user_id'),
        'username': session.get('username')
    })

# ============ RUN ============
if __name__ == '__main__':
    init_db()
    print("\n🔐 Flask Auth Demo Running!")
    print("=" * 40)
    print("Routes:")
    print("  /            - Home")
    print("  /register    - Create account")
    print("  /login       - Login (admin/admin123)")
    print("  /dashboard   - Protected page")
    print("  /logout      - Logout")
    print("  /api/session - Debug session")
    print("=" * 40)
    app.run(debug=True, port=5000)

```

# Setup & Testing Instructions

## Quick Setup (3 Steps)

### Step 1: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install flask
```

### Step 3: Run the App

```bash
python app.py
```

Open `http://127.0.0.1:5000` in browser.

---

## Test the App

### Browser Testing

1. Go to `http://127.0.0.1:5000`
2. Click **Register** → Create account
3. Click **Login** → Use your credentials (or `admin`/`admin123`)
4. Access **Dashboard** → Protected content!
5. Click **Logout** → Session cleared

### curl Testing

#### Check Session (Not logged in)

```bash
curl http://127.0.0.1:5000/api/session
# Returns: {"logged_in": false, "user_id": null}
```

#### Register User

```bash
curl -X POST http://127.0.0.1:5000/register \
  -d "username=testuser&password=testpass123" \
  -c cookies.txt
```

#### Login (Save Cookie)

```bash
curl -X POST http://127.0.0.1:5000/login \
  -d "username=admin&password=admin123" \
  -c cookies.txt -L
```

#### Access Protected Route (With Cookie)

```bash
curl http://127.0.0.1:5000/dashboard \
  -b cookies.txt
```

#### Check Session (Logged in)

```bash
curl http://127.0.0.1:5000/api/session \
  -b cookies.txt
# Returns: {"logged_in": true, "user_id": 1, "username": "admin"}
```

#### Logout

```bash
curl http://127.0.0.1:5000/logout \
  -b cookies.txt -c cookies.txt -L
```

---

## Expected Behavior

|Action|Result|
|---|---|
|Visit `/dashboard` without login|Redirects to `/login`|
|Login with wrong password|"Invalid username or password"|
|Login with correct credentials|Redirects to `/dashboard`|
|Visit `/dashboard` after login|Shows protected content|
|Logout|Clears session, redirects to login|

---

## Concepts Demonstrated

✅ **Password Hashing** - `generate_password_hash()` / `check_password_hash()`  
✅ **Client-Side Sessions** - Data stored in signed cookie  
✅ **Login/Logout Flow** - Session creation and clearing  
✅ **Protected Routes** - `@login_required` decorator  
✅ **Session Fixation Prevention** - `session.clear()` before login  
✅ **Secure Cookies** - HttpOnly, SameSite flags

---

## Add JWT Support (Optional)

```bash
pip install flask-jwt-extended
```

Add to your app:

```python
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

app.config['JWT_SECRET_KEY'] = 'jwt-secret-key'
jwt = JWTManager(app)

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    # Verify user...
    token = create_access_token(identity=user_id)
    return {'token': token}

@app.route('/api/protected')
@jwt_required()
def api_protected():
    return {'message': 'Access granted'}
```

---

## File Structure

```
your-project/
├── app.py          # Main application
├── users.db        # SQLite database (auto-created)
└── cookies.txt     # For curl testing (auto-created)
```