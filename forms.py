from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    FloatField,
    PasswordField,
    SubmitField
)
from wtforms.validators import (
    DataRequired,
    Length,
    EqualTo,
    NumberRange
)

class MechanicsCalculatorForm(FlaskForm):
    mass = FloatField('Масса (кг)', validators=[
        DataRequired(),
        NumberRange(min=0.01, message='Масса должна быть положительной')
    ])
    acceleration = FloatField('Ускорение (м/с²)', validators=[
        NumberRange(min=0, message='Ускорение не может быть отрицательным')
    ])
    velocity = FloatField('Скорость (м/с)', validators=[
        NumberRange(min=0, message='Скорость не может быть отрицательной')
    ])
    calculate_force = SubmitField('Рассчитать силу')
    calculate_energy = SubmitField('Рассчитать энергию')

class ElectromagnetismCalculatorForm(FlaskForm):
    voltage = FloatField('Напряжение (В)', validators=[
        NumberRange(min=0, message='Напряжение не может быть отрицательным')
    ])
    resistance = FloatField('Сопротивление (Ом)', validators=[
        DataRequired(),
        NumberRange(min=0.1, message='Сопротивление должно быть положительным')
    ])
    charge1 = FloatField('Заряд 1 (Кл)')
    charge2 = FloatField('Заряд 2 (Кл)')
    distance = FloatField('Расстояние (м)', validators=[
        NumberRange(min=0.01, message='Расстояние должно быть положительным')
    ])
    calculate_current = SubmitField('Рассчитать ток')
    calculate_force = SubmitField('Рассчитать силу')

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[
        DataRequired(),
        Length(min=4, max=25)
    ])
    password = PasswordField('Пароль', validators=[
        DataRequired(),
        Length(min=6)
    ])
    submit = SubmitField('Войти')

class RegisterForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[
        DataRequired(),
        Length(min=4, max=25)
    ])
    password = PasswordField('Пароль', validators=[
        DataRequired(),
        Length(min=6)
    ])
    confirm_password = PasswordField('Подтвердите пароль', validators=[
        DataRequired(),
        EqualTo('password', message='Пароли должны совпадать')
    ])
    submit = SubmitField('Зарегистрироваться')