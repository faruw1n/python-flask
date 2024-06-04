from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user


class RegistrationForm(FlaskForm):
    username = StringField('Никнейм', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Электронная почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтверждение пароля', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Регистрация')

    # Смотреть пункт 3 в файле с недоработками

    # def validate_username(self, username):
    #     user = User.query.filter_by(username=username.data).first()
    #     if user:
    #         raise ValidationError('That username is taken')
    #
    # def validate_email(self, email):
    #     user = User.query.filter_by(email=email.data).first()
    #     if user:
    #         raise ValidationError('That email is taken')


class UpdateAccountForm(FlaskForm):
    username = StringField('Никнейм', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Электронная почта', validators=[DataRequired(), Email()])
    submit = SubmitField('Обновить')


class PersonalDateForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired(), Length(min=3, max=20)])
    lastname = StringField('Фамилия', validators=[DataRequired(), Length(min=3, max=20)])
    phone_number = StringField('Номер телефона', validators=[DataRequired()])
    submit = SubmitField('Обновить')


class LoginForm(FlaskForm):
    email = StringField('Электронная почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RequestResetForm(FlaskForm):
    email = StringField('Электронная почта', validators=[DataRequired(), Email()])
    submit = SubmitField('Сбросить пароль')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтверждение пароля', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Сбросить пароль')