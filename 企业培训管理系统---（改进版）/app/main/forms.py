from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, ValidationError,HiddenField
from wtforms.validators import DataRequired, Length, Regexp
from ..models import User


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


class EditPorfileForm(FlaskForm):
    name = StringField('姓名')
    about_me = TextAreaField('一句话介绍自己')
    position = StringField('职位')
    submit = SubmitField('提交')


class EditProfileAdminForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),
                                                   Length(1, 64),
                                                   Regexp('^[A-Za-z][A-Za-z]*$', 0, '用户名必须为字母，数字')])
    name = StringField('真实姓名', validators=[Length(0, 64)])
    about_me = TextAreaField('一句话介绍自己')
    position = StringField('职位')
    submit = SubmitField('提交')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.user = user

    def validate_username(self, filed):
        if filed.data != self.user.username and User.query.filter_by(username=filed.data).first():
            raise ValidationError('用户名已存在！')


class PostForm(FlaskForm):
    title = TextAreaField('通知主题', validators=[DataRequired()])
    body = TextAreaField('通知主要内容', validators=[DataRequired()])
    submit = SubmitField('提交')


class CommentForm(FlaskForm):
    body = StringField("", validators=[DataRequired()])
    submit = SubmitField('提交')


class CourserForm(FlaskForm):
    couresename = StringField('课程：', validators=[DataRequired()])
    time = StringField('上课时间', validators=[DataRequired()])
    submit = SubmitField('提交')
