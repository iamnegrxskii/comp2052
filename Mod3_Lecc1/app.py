from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Cambia esto por una clave segura

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Fake database
users = {
    "admin": {
        "password": generate_password_hash("admin123"),
        "role": "admin"
    },
    "user": {
        "password": generate_password_hash("user123"),
        "role": "user"
    }
}

class User(UserMixin):
    def __init__(self, username):
        self.id = username
        self.role = users[username]["role"]

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id)
    return None

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and check_password_hash(users[username]['password'], password):
            user = User(username)
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            return 'Credenciales inválidas'
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.id, role=current_user.role)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)