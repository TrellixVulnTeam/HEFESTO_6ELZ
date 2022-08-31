from xml.dom import ValidationErr
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DecimalField
from wtforms.validators import Length, Email, EqualTo, InputRequired, ValidationError
from flask_app.models import User, Problem
import sys

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

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Este usuário já existe. Por favor escolha outro.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Este e-mail já está cadastrado. Por favor escolha outro.')


class LogInForm(FlaskForm):
    email = StringField('E-mail', 
                        validators=[InputRequired(), Email(message="Este não é um e-mail válido.")])
    password = PasswordField('Senha', 
                             validators=[Length(min=8, max=20, message="Este campo requer entre 8 e 20 caracteres.")])
    remember = BooleanField('Lembrar-me')
    submit = SubmitField('Iniciar Sessão')

    # def validate_email(self, email):
    #     if True:
    #         raise ValidationError('Validation Message')


mult_choices = ['k', 'M']
measurement_choices = ['VA', 'W']

class GeneratorForm(FlaskForm):
    power_mag = DecimalField('Potência')
    power_mult = SelectField('Mult', choices=mult_choices)
    power_measure = SelectField('Medida', choices=measurement_choices)
    submit = SubmitField('Adicionar')

    # def validate_submit(self, submit):
    #     if submit:
    #         raise ValidationError('Validation Message')

# def validate_field(self, field):
#         if True:
#             raise ValidationError('Validation Message')