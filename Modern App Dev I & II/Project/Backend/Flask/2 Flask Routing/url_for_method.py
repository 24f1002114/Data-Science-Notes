from flask import Flask, url_for, render_template

app = Flask(__name__)

# render_template usage example
@app.route('/<username>/<int:page>')
def index(username, page):
    return render_template('index.html', username=username, page=page)

@app.route('/login')
def login():
    return 'login page'

@app.route('/user/<username>')
def profile(username):
    return f'{username}\'s profile'

# Test URL generation
with app.test_request_context():
    print(url_for('login'))                                 # /login
    print(url_for('login', next='/'))                       # /login?next=/
    print(url_for('profile', username='John Doe'))          # /user/John%20Doe
    print(url_for('profile', username='alice', page=2))     # /user/alice?page=2 

if __name__ == "__main__":
    app.run(debug=True)