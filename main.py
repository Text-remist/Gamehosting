from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
import random
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
app.config['SECRET_KEY'] = 'thisisasecretkey'
db = SQLAlchemy(app)

wurm_unlimited = '366220'
rust = '252490'
ark = '346110'
zomboid = '108600'
daystodie = '251570'
csgo = '730'
factorio = '427520'
satisfactory = '526870'
valheim= '892970'
terraria = '105600'
server_name_bank = [
    "Avalon", "Titan", "Elysium", "Olympus", "Valhalla", "Haven", "Fortress", "Sanctuary", "Citadel", "Bastion",
    "Arcadia", "Eden", "Nirvana", "Utopia", "Shangri-La", "Asgard", "Atlantis", "Camelot", "Erebus", "El Dorado",
    "Frosthold", "Helios", "Hyperion", "Inferno", "Ironhold", "Leviathan", "Lumina", "Nebula", "Nexus", "Odyssey",
    "Orion", "Pandora", "Purgatory", "Ragnarok", "Solstice", "Starlight", "Terra", "Valiant", "Vanguard", "Vortex",
    "Zephyr", "Zenith", "Zion", "Aurora", "Blaze", "Celestial", "Chronos", "Cyclone", "Eclipse", "Equinox",
    "Evermore", "Genesis", "Horizon", "Mirage", "Nova", "Onyx", "Paragon", "Phoenix", "Radiance", "Serenity"
]
used_names = set()
server_list = []
for _ in range(20):
    while True:
        server_name = random.choice(server_name_bank)
        if server_name not in used_names:
            used_names.add(server_name)
            break
    server_status = random.choice(['online', 'offline','online'])
    player_count = random.randint(5, 100)
    game_id = random.choice([wurm_unlimited, rust, ark, zomboid, daystodie, csgo, factorio, satisfactory, valheim, terraria])

    server_list.append({
        'server_name': server_name.lower(),
        'server_status': server_status,
        'player_count': player_count,
        'game_id': game_id,
    })

# Combine the original and additional servers
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

with app.app_context():
    db.create_all()

class RegisterForm(FlaskForm):
    username = StringField(validators=[
        InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    email = StringField(validators=[
        InputRequired(), Length(min=8, max=60)], render_kw={"placeholder": "Email"})
    password = PasswordField(validators=[
        InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')
    def validate_email(self, email):
        existing_user_email = User.query.filter_by(
            email=email.data).first()
        if existing_user_email:
            raise ValidationError(
                'That username already exists. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField(validators=[
        InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[
        InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')
class SettingsForm(FlaskForm):
    username = StringField(validators=[
        InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "New Username"})
    email = StringField(validators=[
        InputRequired(), Length(min=8, max=60)], render_kw={"placeholder": "New Email"})
    password = PasswordField(validators=[
        InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "New Password"})
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            existing_user_username = User.query.filter_by(
                username=username.data).first()
            if existing_user_username:
                raise ValidationError(
                    'That username already exists. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            existing_user_email = User.query.filter_by(
                email=email.data).first()
            if existing_user_email:
                raise ValidationError(
                    'That email already exists. Please choose a different one.')

@app.route('/')
def home():

    return render_template('home.html', user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)
@app.route('/servers', methods=['GET', 'POST'])
def servers():
    print(server_list)
    return render_template('servers.html', user=current_user, server_list=server_list)
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = SettingsForm()
    if form.validate_on_submit():
        if form.username.data:
            current_user.username = form.username.data
        if form.email.data:
            current_user.email = form.email.data
        if form.password.data:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            current_user.password = hashed_password
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('settings.html', form=form)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

if __name__ == "__main__":
    app.run(debug=True, host='localhost',port=80)