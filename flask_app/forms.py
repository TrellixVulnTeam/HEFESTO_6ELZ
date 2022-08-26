from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired


class RegistrationForm(FlaskForm):
    username = StringField('Nome', 
                            validators=[InputRequired('saduajbda'), Length(min=8, max=20, message='asdsafdsfd')])
    email = StringField('E-mail', 
                        validators=[DataRequired(), Email()])
    password = PasswordField('Senha', 
                            validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirmar Senha',
                                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrar')


class LogInForm(FlaskForm):
    email = StringField('E-mail', 
                        validators=[DataRequired(), Email()])
    password = PasswordField('Senha', 
                            validators=[DataRequired(), Length(min=8)])
    remember = BooleanField('Lembrar-me')
    submit = SubmitField('Iniciar Sessão')