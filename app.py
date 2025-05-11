from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from forms import (
    MechanicsCalculatorForm,
    ElectromagnetismCalculatorForm,
    LoginForm,
    RegisterForm
)
import math

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-very-secret-key-123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///physics.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

csrf = CSRFProtect(app)
db = SQLAlchemy(app)


# Модель пользователя
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# База данных формул
FORMULAS = {
    'mechanics': [
        {
            'name': 'Второй закон Ньютона',
            'formula': 'F = m × a',
            'description': 'Сила равна произведению массы тела на его ускорение'
        },
        {
            'name': 'Кинетическая энергия',
            'formula': 'Eₖ = (m × v²)/2',
            'description': 'Энергия движущегося тела'
        },
        {
            'name': 'Потенциальная энергия',
            'formula': 'Eₚ = m × g × h',
            'description': 'Энергия положения тела в гравитационном поле'
        }
    ],
    'thermodynamics': [
        {
            'name': 'Уравнение Менделеева-Клапейрона',
            'formula': 'P × V = n × R × T',
            'description': 'Уравнение состояния идеального газа'
        },
        {
            'name': 'Первое начало термодинамики',
            'formula': 'ΔU = Q - A',
            'description': 'Изменение внутренней энергии системы'
        }
    ],
    'electromagnetism': [
        {
            'name': 'Закон Ома',
            'formula': 'I = U / R',
            'description': 'Сила тока на участке цепи'
        },
        {
            'name': 'Закон Кулона',
            'formula': 'F = k × (|q₁ × q₂|) / r²',
            'description': 'Сила взаимодействия точечных зарядов'
        }
    ],
    'optics': [
        {
            'name': 'Закон преломления',
            'formula': 'n₁ × sin(α) = n₂ × sin(β)',
            'description': 'Закон Снеллиуса'
        },
        {
            'name': 'Формула тонкой линзы',
            'formula': '1/F = 1/d + 1/f',
            'description': 'Связь между фокусным расстоянием и расстояниями'
        }
    ]
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/formulas/<section>')
def show_formulas(section):
    if section not in FORMULAS:
        flash('Раздел не найден', 'danger')
        return redirect(url_for('index'))
    return render_template(f'formulas/{section}.html',
                           formulas=FORMULAS[section],
                           section_name=section.capitalize())


@app.route('/calculator/mechanics', methods=['GET', 'POST'])
def mechanics_calculator():
    form = MechanicsCalculatorForm()
    result = None
    calculation_type = None

    if form.validate_on_submit():
        try:
            if form.calculate_force.data:
                mass = float(form.mass.data)
                acceleration = float(form.acceleration.data)
                result = mass * acceleration
                calculation_type = 'force'
            elif form.calculate_energy.data:
                mass = float(form.mass.data)
                velocity = float(form.velocity.data)
                result = 0.5 * mass * velocity ** 2
                calculation_type = 'energy'
        except (TypeError, ValueError):
            flash('Ошибка ввода данных', 'danger')

    return render_template('calculators/mechanics.html',
                           form=form,
                           result=result,
                           calculation_type=calculation_type)


@app.route('/calculator/electromagnetism', methods=['GET', 'POST'])
def electromagnetism_calculator():
    form = ElectromagnetismCalculatorForm()
    result = None
    calculation_type = None

    if form.validate_on_submit():
        try:
            if form.calculate_current.data:
                voltage = float(form.voltage.data)
                resistance = float(form.resistance.data)
                result = voltage / resistance
                calculation_type = 'current'
            elif form.calculate_force.data:
                q1 = float(form.charge1.data)
                q2 = float(form.charge2.data)
                distance = float(form.distance.data)
                k = 9e9  # Н·м²/Кл²
                result = k * abs(q1 * q2) / (distance ** 2)
                calculation_type = 'force'
        except (TypeError, ValueError):
            flash('Ошибка ввода данных', 'danger')

    return render_template('calculators/electromagnetism.html',
                           form=form,
                           result=result,
                           calculation_type=calculation_type)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if User.query.filter_by(username=username).first():
            flash('Имя пользователя уже занято', 'danger')
        else:
            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('Регистрация успешна. Теперь вы можете войти.', 'success')
            return redirect(url_for('login'))

    return render_template('auth/register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            flash('Вход выполнен успешно', 'success')
            return redirect(url_for('index'))
        else:
            flash('Неверное имя пользователя или пароль', 'danger')

    return render_template('auth/login.html', form=form)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)