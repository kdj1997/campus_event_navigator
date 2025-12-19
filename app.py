from flask import Flask, request, render_template, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secret_key_hard_to_guess'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, email, password, name):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.is_admin = email == 'admin@campus.kz'
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

# Создаем таблицы
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Please login or use different email.', 'danger')
            return redirect(url_for('register'))

        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        if email == 'admin@campus.kz':
            flash('Admin registration successful! Please login.', 'success')
        else:
            flash('Registration successful! Please login.', 'success')
        
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['user_email'] = user.email
            session['is_admin'] = user.is_admin
            
            flash('Login successful!', 'success')
            
            if user.is_admin:
                return redirect(url_for('admin_profile'))  # Редирект на admin_profile
            else:
                return redirect(url_for('profile'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('login.html')

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        flash('Please login first', 'warning')
        return redirect(url_for('login'))
    return render_template('profile.html')

# ============ ОБЫЧНЫЕ ПОЛЬЗОВАТЕЛИ ============
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please login first', 'warning')
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/join_club')
def join_club():
    if 'user_id' not in session:
        flash('Please login first', 'warning')
        return redirect(url_for('login'))
    return render_template('join_club.html')

@app.route('/explore_events')
def explore_events():
    if 'user_id' not in session:
        flash('Please login first', 'warning')
        return redirect(url_for('login'))
    return render_template('explore_events.html')

@app.route('/my_events')
def my_events():
    if 'user_id' not in session:
        flash('Please login first', 'warning')
        return redirect(url_for('login'))
    return render_template('my_events.html')

@app.route('/notifications')
def notifications():
    if 'user_id' not in session:
        flash('Please login first', 'warning')
        return redirect(url_for('login'))
    return render_template('notifications.html')

@app.route('/book_club')
def book_club():
    if 'user_id' not in session:
        flash('Please login first', 'warning')
        return redirect(url_for('login'))
    return render_template('book_club.html')

@app.route('/event_concert')
def event_concert():
    if 'user_id' not in session:
        flash('Please login first', 'warning')
        return redirect(url_for('login'))
    return render_template('event_concert.html')

@app.route('/event_jobfair')
def event_jobfair():
    if 'user_id' not in session:
        flash('Please login first', 'warning')
        return redirect(url_for('login'))
    return render_template('event_jobfair.html')

@app.route('/edit_profile')
def edit_profile():
    if 'user_id' not in session:
        flash('Please login first', 'warning')
        return redirect(url_for('login'))
    return render_template('edit_profile.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('home'))

# ============ АДМИНСКИЕ РОУТЫ ============
@app.route('/admin_profile')
def admin_profile():
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('login'))
    return render_template('admin_profile.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('login'))
    return render_template('admin_dashboard.html')

@app.route('/admin_club')
def admin_club():
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('login'))
    return render_template('admin_club.html')

@app.route('/admin_events')
def admin_events():
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('login'))
    return render_template('admin_events.html')

@app.route('/admin_explore')
def admin_explore():
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('login'))
    return render_template('admin_explore.html')

@app.route('/admin_myevents')
def admin_myevents():
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('login'))
    return render_template('admin_myevents.html')

@app.route('/admin_notifications')
def admin_notifications():
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('login'))
    return render_template('admin_notifications.html')

@app.route('/admin_edit_profile')
def admin_edit_profile():
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('login'))
    return render_template('admin_edit_profile.html')

if __name__ == '__main__':
    app.run(debug=True)