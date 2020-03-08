from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,RadioField,FileField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo,Length
from app.models import User
from flask_wtf.file import FileAllowed,FileRequired

class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(),Length(min=1,max=15)])
    password = PasswordField('密码', validators=[DataRequired(),Length(min=1,max=15)])
    remember_me = BooleanField('记住我')
    verify_code = StringField('验证码', validators=[DataRequired(),Length(min=4,max=4)])
    submit = SubmitField('登录')

class RegistrationForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(),Length(min=1,max=15)])
    password = PasswordField('密码', validators=[DataRequired(),Length(min=1,max=15)])
    password = PasswordField('确认密码', validators=[DataRequired(), EqualTo('password'),Length(min=1,max=15)])
    mail_addr = StringField('邮件地址',validators=[DataRequired(),Length(min=7,max=64)])
    verify_code = StringField('验证码', validators=[DataRequired(),Length(min=4,max=4)])
    submit = SubmitField('注册')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

class EditProfileForm(FlaskForm):
    avatar = FileField('Avatar',validators = [FileAllowed(['jpg','jpeg','gif','png'])])
    gender = RadioField('Gender',
                        choices = [('1','Male'),('0','Female'),('2','?')],
                        validators=[DataRequired()])
    io = StringField('Self introduction',validators=[Length(max=128)])
    submit = SubmitField('Submit')