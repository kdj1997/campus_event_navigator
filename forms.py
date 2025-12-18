from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length

# Форма для логина
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])  # Поле для email
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])  # Поле для пароля

# Форма для регистрации
class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])  # Поле для email
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])  # Поле для пароля
