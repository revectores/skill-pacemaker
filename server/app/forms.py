from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, FileField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User
from flask_wtf.file import FileAllowed, FileRequired


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(min=1, max=15)])
    password = PasswordField('密码', validators=[DataRequired(), Length(min=1, max=15)])
    remember_me = BooleanField('记住我')
    verify_code = StringField('验证码', validators=[DataRequired(), Length(min=4, max=4)])
    submit = SubmitField('登录')


class RegistrationForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(min=1, max=15)])
    password = PasswordField('密码', validators=[DataRequired(), Length(min=1, max=15)])
    password = PasswordField('确认密码', validators=[DataRequired(), EqualTo('password'), Length(min=1, max=15)])
    mail_addr = StringField('邮件地址', validators=[DataRequired(), Length(min=7, max=64)])
    verify_code = StringField('验证码', validators=[DataRequired(), Length(min=4, max=4)])
    submit = SubmitField('注册')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')


class EditProfileForm(FlaskForm):
    avatar = FileField('头像', validators=[FileAllowed(['jpg', 'jpeg', 'gif', 'png'])])
    gender = RadioField('性别',
                        choices=[('1', '男'), ('0', '女'), ('2', '神秘生物')],
                        validators=[DataRequired()])
    io = TextAreaField('自我介绍', validators=[Length(max=128)])
    submit = SubmitField('完成更改')

class EditorForm(FlaskForm):
    body = TextAreaField(u'正文', validators=[DataRequired(u'内容不能为空！')])
    submit = SubmitField('提交')

class MaterialForm(FlaskForm):
    body = TextAreaField(u'正文', validators=[DataRequired(u'内容不能为空！')])
    file = FileField('文件', validators=[FileAllowed(['md', 'doc','docx'])])
    submit = SubmitField('提交')