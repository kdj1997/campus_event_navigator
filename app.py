from flask import Flask, request, render_template, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secret_key_hard_to_guess'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# ============ МОДЕЛИ ============
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

class Club(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    leader = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    office_hours = db.Column(db.String(200))
    instagram = db.Column(db.String(100))
    
    def __init__(self, name, description, leader, email, phone="", office_hours="", instagram=""):
        self.name = name
        self.description = description
        self.leader = leader
        self.email = email
        self.phone = phone
        self.office_hours = office_hours
        self.instagram = instagram

class Requirement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    club_id = db.Column(db.Integer, db.ForeignKey('club.id'), nullable=False)
    text = db.Column(db.String(200), nullable=False)
    position = db.Column(db.Integer, default=0)
    
    club = db.relationship('Club', backref=db.backref('requirements', lazy=True, cascade="all, delete-orphan"))

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_filename = db.Column(db.String(100), default='jobfair-card.png')
    date = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    price = db.Column(db.String(50), default='Free')
    
    def __init__(self, title, description, date, time, location, price='Free', image_filename='jobfair-card.png'):
        self.title = title
        self.description = description
        self.date = date
        self.time = time
        self.location = location
        self.price = price
        self.image_filename = image_filename

class EventHighlight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    text = db.Column(db.String(200), nullable=False)
    position = db.Column(db.Integer, default=0)
    
    event = db.relationship('Event', backref=db.backref('highlights', lazy=True, cascade="all, delete-orphan"))

# Создаем таблицы и добавляем начальные данные
with app.app_context():
    db.create_all()
    
    # Создаем админа по умолчанию если его нет
    if not User.query.filter_by(email='admin@campus.kz').first():
        admin = User(
            email='admin@campus.kz',
            password='admin123',
            name='Alma Karimova'
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user created: admin@campus.kz / admin123")
    
    # Создаем дефолтный Book Club если его нет
    if not Club.query.filter_by(name='Book Club').first():
        book_club = Club(
            name='Book Club',
            description='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam.',
            leader='Alma Karimova',
            email='alma_karimova@gmail.com',
            phone='+7 (700) 1234567',
            office_hours='Monday & Thursday, 15:00-17:00, Library Room 203',
            instagram='@sdu.bookclub'
        )
        db.session.add(book_club)
        db.session.commit()
        
        # Добавляем дефолтные требования
        requirements = [
            "Interest in reading, writing, or literature discussions.",
            "Attend at least two meetings per month.",
            "Contribute to at least one book review.",
            "Friendly attitude and willingness to share ideas."
        ]
        
        for i, req_text in enumerate(requirements):
            requirement = Requirement(
                club_id=book_club.id,
                text=req_text,
                position=i
            )
            db.session.add(requirement)
        
        db.session.commit()
        print("Default Book Club created")
    
    # Создаем дефолтное событие если его нет
    if not Event.query.filter_by(title='Job Fair').first():
        job_fair = Event(
            title='Job Fair',
            description='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
            date='October 10',
            time='15:00',
            location='SDU Life',
            price='Free',
            image_filename='jobfair-card.png'
        )
        db.session.add(job_fair)
        db.session.commit()
        
        # Добавляем дефолтные highlights
        highlights = [
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        ]
        
        for i, highlight_text in enumerate(highlights):
            highlight = EventHighlight(
                event_id=job_fair.id,
                text=highlight_text,
                position=i
            )
            db.session.add(highlight)
        
        db.session.commit()
        print("Default Job Fair event created")

# ============ ОСНОВНЫЕ РОУТЫ ============
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
                return redirect(url_for('admin_profile'))
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
    
    user = User.query.get(session['user_id'])
    if not user:
        flash('User not found', 'danger')
        return redirect(url_for('login'))
    
    # Разбиваем имя на first_name и last_name для отображения
    name_parts = user.name.split(' ', 1)
    first_name = name_parts[0]
    last_name = name_parts[1] if len(name_parts) > 1 else ""
    
    return render_template('admin_profile.html', 
                         first_name=first_name,
                         last_name=last_name,
                         email=user.email)

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('login'))
    return render_template('admin_dashboard.html')

@app.route('/admin_club', methods=['GET', 'POST'])
def admin_club():
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('login'))
    
    # Получаем клуб (предполагаем, что это Book Club)
    club = Club.query.filter_by(name='Book Club').first()
    if not club:
        flash('Club not found', 'danger')
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        # Определяем тип действия
        action = request.form.get('action')
        
        if action == 'update_club':
            # Обновляем основную информацию клуба
            club.description = request.form.get('description', '')
            club.leader = request.form.get('leader', '')
            club.email = request.form.get('email', '')
            club.phone = request.form.get('phone', '')
            club.office_hours = request.form.get('office_hours', '')
            club.instagram = request.form.get('instagram', '')
            
            db.session.commit()
            flash('Club information updated successfully!', 'success')
            
        elif action == 'add_requirement':
            # Добавляем новое требование
            new_req_text = request.form.get('new_requirement', '').strip()
            if new_req_text:
                # Находим максимальную позицию
                max_position = db.session.query(db.func.max(Requirement.position)).filter_by(club_id=club.id).scalar() or -1
                
                new_requirement = Requirement(
                    club_id=club.id,
                    text=new_req_text,
                    position=max_position + 1
                )
                db.session.add(new_requirement)
                db.session.commit()
                flash('Requirement added successfully!', 'success')
            
        elif action == 'delete_requirement':
            # Удаляем требование
            req_id = request.form.get('requirement_id')
            if req_id:
                requirement = Requirement.query.get(int(req_id))
                if requirement and requirement.club_id == club.id:
                    db.session.delete(requirement)
                    db.session.commit()
                    
                    # Перенумеровываем оставшиеся требования
                    remaining_reqs = Requirement.query.filter_by(club_id=club.id).order_by(Requirement.position).all()
                    for i, req in enumerate(remaining_reqs):
                        req.position = i
                    db.session.commit()
                    
                    flash('Requirement deleted successfully!', 'success')
        
        elif action == 'update_requirement':
            # Обновляем требование
            req_id = request.form.get('requirement_id')
            req_text = request.form.get('requirement_text', '').strip()
            
            if req_id and req_text:
                requirement = Requirement.query.get(int(req_id))
                if requirement and requirement.club_id == club.id:
                    requirement.text = req_text
                    db.session.commit()
                    flash('Requirement updated successfully!', 'success')
        
        elif action == 'delete_club':
            # Удаляем клуб (опционально)
            db.session.delete(club)
            # Каскадно удалятся все требования
            db.session.commit()
            flash('Club deleted successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        
        return redirect(url_for('admin_club'))
    
    # GET запрос - показываем текущие данные
    requirements = Requirement.query.filter_by(club_id=club.id).order_by(Requirement.position).all()
    
    return render_template('admin_club.html',
                         club=club,
                         requirements=requirements)

@app.route('/admin_events', methods=['GET', 'POST'])
def admin_events():
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('login'))
    
    # Получаем текущее событие (для простоты берем первое или Job Fair)
    event = Event.query.filter_by(title='Job Fair').first()
    if not event:
        # Если Job Fair нет, берем первое событие или создаем новое
        event = Event.query.first()
        if not event:
            flash('No events found', 'warning')
            # Здесь можно перенаправить на создание нового события
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'create_event':
            # Создание нового события
            new_event = Event(
                title='New Event',
                description='Enter event description here...',
                date='Date TBD',
                time='Time TBD',
                location='Location TBD',
                price='Free'
            )
            db.session.add(new_event)
            db.session.commit()
            
            flash('New event created!', 'success')
            return redirect(url_for('admin_events'))
            
        elif action == 'update_event':
            # Обновление информации о событии
            if event:
                event.title = request.form.get('title', event.title)
                event.description = request.form.get('description', event.description)
                event.date = request.form.get('date', event.date)
                event.time = request.form.get('time', event.time)
                event.location = request.form.get('location', event.location)
                event.price = request.form.get('price', event.price)
                
                db.session.commit()
                flash('Event updated successfully!', 'success')
            
        elif action == 'add_highlight':
            # Добавление нового highlight
            new_highlight_text = request.form.get('new_highlight', '').strip()
            if new_highlight_text and event:
                max_position = db.session.query(db.func.max(EventHighlight.position)).filter_by(event_id=event.id).scalar() or -1
                
                new_highlight = EventHighlight(
                    event_id=event.id,
                    text=new_highlight_text,
                    position=max_position + 1
                )
                db.session.add(new_highlight)
                db.session.commit()
                flash('Highlight added successfully!', 'success')
            
        elif action == 'delete_highlight':
            # Удаление highlight
            highlight_id = request.form.get('highlight_id')
            if highlight_id:
                highlight = EventHighlight.query.get(int(highlight_id))
                if highlight and highlight.event_id == event.id:
                    db.session.delete(highlight)
                    db.session.commit()
                    
                    # Перенумеровываем оставшиеся highlights
                    remaining_highlights = EventHighlight.query.filter_by(event_id=event.id).order_by(EventHighlight.position).all()
                    for i, hl in enumerate(remaining_highlights):
                        hl.position = i
                    db.session.commit()
                    
                    flash('Highlight deleted successfully!', 'success')
        
        elif action == 'update_highlight':
            # Обновление highlight
            highlight_id = request.form.get('highlight_id')
            highlight_text = request.form.get('highlight_text', '').strip()
            
            if highlight_id and highlight_text:
                highlight = EventHighlight.query.get(int(highlight_id))
                if highlight and highlight.event_id == event.id:
                    highlight.text = highlight_text
                    db.session.commit()
                    flash('Highlight updated successfully!', 'success')
        
        elif action == 'delete_event':
            # Удаление события
            if event:
                db.session.delete(event)
                db.session.commit()
                flash('Event deleted successfully!', 'success')
                return redirect(url_for('admin_events'))
        
        return redirect(url_for('admin_events'))
    
    # GET запрос - показываем текущие данные
    highlights = []
    if event:
        highlights = EventHighlight.query.filter_by(event_id=event.id).order_by(EventHighlight.position).all()
    
    return render_template('admin_events.html',
                         event=event,
                         highlights=highlights)

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

@app.route('/admin_edit_profile', methods=['GET', 'POST'])
def admin_edit_profile():
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user:
        flash('User not found', 'danger')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Получаем данные из формы
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        
        # Валидация
        if not first_name:
            flash('First name is required', 'danger')
            # Разбиваем текущее имя для повторного отображения
            name_parts = user.name.split(' ', 1)
            current_first_name = name_parts[0]
            current_last_name = name_parts[1] if len(name_parts) > 1 else ""
            
            return render_template('admin_edit_profile.html',
                                 first_name=current_first_name,
                                 last_name=current_last_name,
                                 email=user.email,
                                 mobile="+7(777)7777777")  # Дефолтный телефон
        
        # Формируем полное имя
        full_name = f"{first_name} {last_name}".strip()
        
        # Обновляем данные пользователя
        user.name = full_name
        
        # Сохраняем в базу
        db.session.commit()
        
        # Обновляем данные в сессии
        session['user_name'] = full_name
        
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('admin_profile'))
    
    # GET запрос - показываем форму с текущими данными
    # Разбиваем имя на first_name и last_name
    name_parts = user.name.split(' ', 1)
    first_name = name_parts[0]
    last_name = name_parts[1] if len(name_parts) > 1 else ""
    
    return render_template('admin_edit_profile.html',
                         first_name=first_name,
                         last_name=last_name,
                         email=user.email,
                         mobile="+7(777)7777777")  # Дефолтный телефон

if __name__ == '__main__':
    app.run(debug=True)