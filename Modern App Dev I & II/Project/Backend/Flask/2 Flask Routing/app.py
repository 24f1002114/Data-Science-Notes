from flask import Flask, render_template, request, url_for, abort
from markupsafe import escape

app = Flask(__name__)

# Basic routes
@app.route('/')
def index():
    return '''
        <h1>Welcome</h1>
        <a href="{}">Login</a><br>
        <a href="{}">User Profile</a><br>
        <a href="{}">Post 42</a><br>
        <a href="{}">Files</a>
    '''.format(
        url_for('login'),
        url_for('profile', username='john'),
        url_for('post', post_id=42),
        url_for('files', filepath='example/path')
    )

# Variable rules with converters
@app.route('/user/<username>')
def profile(username):
    return f'<h1>User: {escape(username)}</h1>'

@app.route('/post/<int:post_id>')
def post(post_id):
    if post_id > 100:
        abort(404)
    return f'<h1>Post {post_id}</h1>'

@app.route('/files/<path:filepath>')
def files(filepath):
    return f'<h1>File: {escape(filepath)}</h1>'

# HTTP methods
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        return f'<h1>Welcome, {escape(username)}!</h1>'
    return '''
        <form method="post">
            <input name="username" placeholder="Username">
            <button>Login</button>
        </form>
    '''

# Error handling
@app.errorhandler(404)
def not_found(error):
    return '<h1>404 - Page Not Found</h1>', 404

if __name__ == '__main__':
    app.run(debug=True)