from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,RadioField,FileField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User
from flask_wtf.file import FileAllowed,FileRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
    verify_code = StringField('VerifyCode', validators=[DataRequired()])

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    mail_addr = StringField('Mail Address',validators=[DataRequired()])
    verify_code = StringField('VerifyCode', validators=[DataRequired()])

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

class EditProfileForm(FlaskForm):
    io = StringField('Self introduction')
    gender = RadioField('Gender',
                        choices = [('1','Male'),('0','Female'),('2','?')],
                        validators=[DataRequired()])

    avatar = FileField('Avatar',validators = [FileAllowed(['jpg','jpeg','gif','png'])])
    submit = SubmitField('Submit')