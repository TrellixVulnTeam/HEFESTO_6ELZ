from xml.dom import ValidationErr
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DecimalField, FloatField, IntegerField
from wtforms.validators import Length, Email, EqualTo, InputRequired, ValidationError
from app.models import User, Problem
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


mult_choices = {'power': ['M', 'k'], 'voltage': ['k', '%'], 'impedance': ['%', '']}
measurement_choices = {'power': ['VA', 'W'], 
                                'voltage': ['V', 'pu'], 
                                'comp_impedance': ['pu', 'ohm'],
                                'series_impedance': ['pu', 'ohm', 'ohm/km'], 
                                'shunt_impedance': ['pu', 'ohm', 'kohm*km']}

class PuGeneratorForm(FlaskForm):
    # Gerador
    power_mag = DecimalField('Potência')
    power_mult = SelectField('Potência Mult', choices=mult_choices['power'])
    power_measure = SelectField('Potência Medida', choices=measurement_choices['power'])
    voltage_mag = DecimalField('Tensão')
    voltage_mult = SelectField('Tensão Mult', choices=mult_choices['voltage'])
    voltage_measure = SelectField('Tensão Medida', choices=measurement_choices['voltage'])
    impedance_mag = DecimalField('Impedância')
    impedance_mult = SelectField('Impedância Mult', choices=mult_choices['impedance'])
    impedance_measure = SelectField('Impedância Medida', choices=measurement_choices['comp_impedance'])
    t0 = IntegerField('Terminal-0')
    t1 = IntegerField('Terminal-1')
    submit_gen = SubmitField('Gerador')


class PuTransformerForm(FlaskForm):
    # Transformador
    power_mag = DecimalField('Potência')
    power_mult = SelectField('Potência Mult', choices=mult_choices['power'])
    power_measure = SelectField('Potência Medida', choices=measurement_choices['power'])
    high_voltage_mag = DecimalField('Alta Tensão')
    high_voltage_mult = SelectField('Alta Tensão Mult', choices=mult_choices['voltage'])
    high_voltage_measure = SelectField('Alta Tensão Medida', choices=measurement_choices['voltage'])
    low_voltage_mag = DecimalField('Baixa Tensão')
    low_voltage_mult = SelectField('Baixa Tensão Mult', choices=mult_choices['voltage'])
    low_voltage_measure = SelectField('Baixa Tensão Medida', choices=measurement_choices['voltage'])
    impedance_mag = DecimalField('Impedância')
    impedance_mult = SelectField('Impedância Mult', choices=mult_choices['impedance'])
    impedance_measure = SelectField('Impedância Medida', choices=measurement_choices['comp_impedance'])
    t0 = IntegerField('Terminal-0')
    t1 = IntegerField('Terminal-1')
    submit_tran = SubmitField('Transformador')


class PuShortTlineForm(FlaskForm):
    # Linha de Transmissão Pequena
    series_impedance_mag = StringField('Impedância')
    series_impedance_mult = SelectField('Impedância Mult', choices=mult_choices['impedance'])
    series_impedance_measure = SelectField('Impedância Medida', choices=measurement_choices['series_impedance'])
    t0 = IntegerField('Terminal-0')
    t1 = IntegerField('Terminal-1')
    lenght = StringField('Comprimento')
    submit_stl = SubmitField('Linha de Transmissão Pequena')

    def validate_series_impedance_mag(self, series_impedance_mag):
        try:
            complex(series_impedance_mag.data)
        except:
            raise ValidationError('Formato: a+bj ou a-bj')
    
    def validate_lenght(self, lenght):
        for attr_len, value_len in lenght.__dict__.items():
            if attr_len == 'data' and value_len == '':
                for attr_z, value_z in self.series_impedance_measure.__dict__.items():
                    if attr_z == 'data' and value_z == 'ohm/km':
                        raise ValidationError('Para ohm/km o comprimento é obrigatório.')


class PuMediumTlineForm(FlaskForm):
    # Linha de Transmissão Média
    series_impedance_mag = StringField('Impedância')
    series_impedance_mult = SelectField('Impedância Mult', choices=mult_choices['impedance'])
    series_impedance_measure = SelectField('Impedância Medida', choices=measurement_choices['series_impedance'])
    shunt_impedance_mag = StringField('Impedância')
    shunt_impedance_mult = SelectField('Impedância Mult', choices=mult_choices['impedance'])
    shunt_impedance_measure = SelectField('Impedância Medida', choices=measurement_choices['shunt_impedance'])
    t0 = IntegerField('Terminal-0')
    t1 = IntegerField('Terminal-1')
    lenght = StringField('Comprimento')
    submit_mtl = SubmitField('Linha de Transmissão Média')

    # def validate_t0(self, t0):
    #     print(f"int(t0): {t0.__dict__.items()}", file=sys.stderr)
    #     for attr_t, value_t in t0.__dict__.items():
    #         if attr_t == 'data' and value_t == None or :


    def validate_series_impedance_mag(self, series_impedance_mag):
        try:
            complex(series_impedance_mag.data)
        except:
            raise ValidationError('Formato: a+bj ou a-bj')
    
    def validate_shunt_impedance_mag(self, shunt_impedance_mag):
        try:
            complex(shunt_impedance_mag.data)
        except:
            raise ValidationError('Formato: a+bj ou a-bj')            
            
    def validate_lenght(self, lenght):
        for attr_len, value_len in lenght.__dict__.items():
            if attr_len == 'data' and value_len == '':
                for attr_z, value_z in self.series_impedance_measure.__dict__.items():
                    if attr_z == 'data' and value_z == 'ohm/km':
                        raise ValidationError('Para ohm/km o comprimento é obrigatório.')
                for attr_z, value_z in self.shunt_impedance_measure.__dict__.items():
                    if attr_z == 'data' and value_z == 'kohm*km':
                        raise ValidationError('Para kohm*km o comprimento é obrigatório.')
            
# def validate_field(self, field):
#         if True:
#             raise ValidationError('Validation Message')