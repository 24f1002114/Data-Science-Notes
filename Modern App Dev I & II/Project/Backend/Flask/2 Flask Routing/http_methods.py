from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle form submission
        username = request.form.get('username')
        return f'Logging in as {username}...'
    else:
        # Show login form
        return '''
            <form method="post">
                <input name="username" type="text">
                <input type="submit" value="Login">
            </form>
        '''

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify({'data': 'value'})

@app.route('/api/user', methods=['POST'])
def create_user():
    return jsonify({'message': 'User created'}), 201

if __name__ == "__main__":
    app.run(debug=True)
