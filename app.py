from flask import Flask, render_template, request, redirect, url_for, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MongoDB Configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/mydatabase"
mongo = PyMongo(app)

# Collection
users_collection = mongo.db.users

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user', methods=['GET', 'POST'])
def user():
    return render_template('user.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users_collection.find_one({'username': username, 'password': password})
        if user:
            session['username'] = username
            return redirect(url_for('welcome'))
        else:
            return "Invalid credentials"
    return render_template('login.html')

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin_key = request.form['admin_key']
        if admin_key == 'admin_secret_key':
            session['admin'] = True
            return redirect(url_for('welcome'))
        else:
            return "Invalid admin key"
    return render_template('admin_login.html')

@app.route('/welcome')
def welcome():
    if 'username' in session or 'admin' in session:
        return render_template('welcome.html')
    else:
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
