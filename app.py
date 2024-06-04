from flask import Flask, render_template, request, redirect, url_for, flash
from forms import RegistrationForm, LoginForm, UpdateAccountForm, PersonalDateForm, RequestResetForm, ResetPasswordForm
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from flask_mail import Mail

# Это библиотека для почтового сервера. Она устарела поэтому нужно заменить на Authlib.
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


app = Flask(__name__)
app.config['SECRET_KEY'] = '5b0ef66f5e7c0ec1533c573a0a6400f9'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotel.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    personal_date = db.relationship('PersonalData', backref='user', lazy=True)
    bookings = db.relationship('Booking', backref='user', lazy=True)

    # Так же почтовый сервис

    # @staticmethod
    # def get_reset_token(self, expires_sec=1800):
    #     s = Serializer(app.config['SECRET_KEY'], expires_sec)
    #     return s.dumps({'user_id': self.id}).decode('utf-8')
    #
    # def verify_reset_token(token):
    #     s = Serializer(app.config['SECRET_KEY'])
    #     try:
    #         user_id = s.loads(token)['user_id']
    #     except:
    #         return None
    #     return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}','{self.email}')"


class PersonalData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.Integer, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Check_in_date = db.Column(db.DateTime, nullable=False)
    departure_date = db.Column(db.DateTime, nullable=False)
    room_number = db.Column(db.Integer, nullable=False)
    Number_of_people = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been update!')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('profile.html', title='Profile', form=form)


@app.route("/profile_HB")
def profile_hb():
    return render_template('profile_HB.html', title='Profile_HB')


@app.route("/profile_PD", methods=['GET', 'POST'])
def profile_pd():
    form = PersonalDateForm()

    if form.validate_on_submit():
        personal_date = PersonalData(first_name=form.name.data, last_name=form.lastname.data,
                                     phone_number=form.phone_number.data, user=current_user)
        db.session.add(personal_date)
        db.session.commit()
        flash('Your account has been updated!')
        return redirect(url_for('profile_pd'))
    if current_user.is_authenticated:
        personal_data = PersonalData.query.filter_by(user_id=current_user.id).first()
        if personal_data:
            form.name.data = personal_data.first_name
            form.lastname.data = personal_data.last_name
            form.phone_number.data = personal_data.phone_number
    return render_template('profile_PD.html', title='Profile_PD', form=form)


@app.route("/booking")
def booking():
    return render_template('booking.html', title='Booking')

    # Весь код дальше исключительно для почтового сервиса


# def send_reset_email(user):
#     pass
#
#
# @app.route("/reset_password", methods=['GET', 'POST'])
# def reset_request():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     form = RequestResetForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         send_reset_email(user)
#         flash('An email has been sent with instructions to reset your password')
#         return redirect(url_for('login'))
#     return render_template('reset_request.html', title='Reset Password', form=form)
#
#
# @app.route("/reset_password/<token>", methods=['GET', 'POST'])
# def reset_token(token):
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     user = User.verify_reset_token(token)
#     if user is None:
#         flash('That is an invalid or expired token')
#         return redirect(url_for('reset_request'))
#     form = ResetPasswordForm()
#     return render_template('reset_token.html', title='Reset Password', form=form)


if __name__ == "__main__":
    app.run(debug=True)