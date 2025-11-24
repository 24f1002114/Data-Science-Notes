from flask import Flask
from markupsafe import escape

app = Flask(__name__)

@app.route('/user/<username>')
def show_user_profile(username):
    # escape() prevents XSS by converting <script> to &lt;script&gt;
    return f'User {escape(username)}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # post_id is automatically converted to an integer
    return f'Post {post_id}'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # path accepts slashes (for file paths)
    return f'Subpath {escape(subpath)}'

if __name__ == "__main__":
    app.run(debug=True)

"""
Example URL	                                Output
http://127.0.0.1:5000/user/Anshul	        User Anshul
http://127.0.0.1:5000/post/10	            Post 10
http://127.0.0.1:5000/path/folder1/folder2	Subpath folder1/folder2

"""
