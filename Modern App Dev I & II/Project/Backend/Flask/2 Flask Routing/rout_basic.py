from flask import Flask

app = Flask(__name__ )

@app.route('/')
def home():
    return "Welcome to the Home Page!"

@app.route('/about')
def about():    
    return "This is the About Page."

if __name__ == '__main__': # It runs your Flask app only when the file is executed directly
   app.run(debug=True)  # `debug=True` lets you auto-reload and see detailed error info.