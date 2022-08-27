from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired


class RegistrationForm(FlaskForm):
    username = StringField('Nome', 
                            validators=[Length(min=8, max=20, message="Este campo requer entre 8 e 20 caracteres.")])
    email = StringField('E-mail', 
                        validators=[InputRequired(), Email(message="Este não é um e-mail válido.")])
    password = PasswordField('Senha', 
                             validators=[Length(min=8, max=20, message="Este campo requer entre 8 e 20 caracteres.")])
    confirm_password = PasswordField('Confirmar Senha',
                                    validators=[EqualTo('password', message="Este campo precisa ser igual à senha.")])
    submit = SubmitField('Registrar')


class LogInForm(FlaskForm):
    email = StringField('E-mail', 
                        validators=[InputRequired(), Email(message="Este não é um e-mail válido.")])
    password = PasswordField('Senha', 
                             validators=[Length(min=8, max=20, message="Este campo requer entre 8 e 20 caracteres.")])
    remember = BooleanField('Lembrar-me')
    submit = SubmitField('Iniciar Sessão')