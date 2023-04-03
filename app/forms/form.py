from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models.model import User


class RegisterForm(FlaskForm):
    username = StringField('账号', validators=[DataRequired(), Length(min=6, max=20, message="账号长度必须大于6并且小于20")])
    email = StringField('邮箱', validators=[DataRequired(), Email(message="邮箱格式不正确")])
    password = PasswordField('密码', validators=[DataRequired(), Length(min=3, max=10, message="密码长度必须大于3并且小于10")])
    confirm = PasswordField('确认密码', validators=[DataRequired(), EqualTo('password', message="两次输入密码不一致")])
    #recaptcha = RecaptchaField()
    submit = SubmitField('注册')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('账号已被注册')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('邮箱已被注册')


class LoginForm(FlaskForm):
    username = StringField('账号', validators=[DataRequired(), Length(min=6, max=20, message="账号长度必须大于6并且小于20")])
    password = PasswordField('密码', validators=[DataRequired(), Length(min=3, max=10, message="密码长度必须大于3并且小于10")])
    verify_code = StringField('验证码', validators=[DataRequired()])
    remember = BooleanField('记住我')
    submit = SubmitField('登录')

    @staticmethod
    def is_authenticated(self):
        return True


class PasswordResetRequestForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Email(message="邮箱格式不正确")])
    submit = SubmitField('发送')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('邮箱不存在')


class ResetPasswordForm(FlaskForm):

    password = PasswordField('密码', validators=[DataRequired(), Length(min=3, max=10, message="密码长度必须大于3并且小于10")])
    confirm = PasswordField('确认密码', validators=[DataRequired(), EqualTo('password', message="两次输入密码不一致")])
    submit = SubmitField('确认')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('旧密码', validators=[DataRequired(), Length(min=3, max=10, message="密码长度必须大于3并且小于10")])
    password = PasswordField('新密码', validators=[DataRequired(), Length(min=3, max=10, message="密码长度必须大于3并且小于10")])
    confirm = PasswordField('确认密码', validators=[DataRequired(), EqualTo('password', message="两次输入密码不一致")])
    submit = SubmitField('确认')