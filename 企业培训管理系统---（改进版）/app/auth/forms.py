from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from ..models import User


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('登陆')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    phone = StringField('电话号码', validators=[DataRequired()])
    username = StringField('用户名', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('请输入密码', validators=[DataRequired(), EqualTo('password2',
                                                                          message='密码必须相同')])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField('注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValueError("该邮箱已被注册")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValueError("用户名已存在")

    def validate_phone(self, field):
        if User.query.filter_by(phone=field.data).first():
            raise ValueError("电话号码已存在")
