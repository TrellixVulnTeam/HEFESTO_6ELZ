from xml.dom import ValidationErr
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms.meta import DefaultMeta
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
characteristic = {'power_factor': ['Atrasado/Indutivo', 'Avançado/Capacitivo']}


class PuGeneratorForm(FlaskForm):
    # Gerador
    power_mag = StringField('Potência')
    power_mult = SelectField('Potência Mult', choices=mult_choices['power'])
    power_measure = SelectField('Potência Medida', choices=measurement_choices['power'])
    voltage_mag = StringField('Tensão')
    voltage_mult = SelectField('Tensão Mult', choices=mult_choices['voltage'])
    voltage_measure = SelectField('Tensão Medida', choices=measurement_choices['voltage'])
    impedance_mag = StringField('Impedância')
    impedance_mult = SelectField('Impedância Mult', choices=mult_choices['impedance'])
    impedance_measure = SelectField('Impedância Medida', choices=measurement_choices['comp_impedance'])
    t1 = IntegerField('power_factor_mag')
    submit_gen = SubmitField('Gerador')

    def validate_power_mag(self, power_mag):
        try:
            complex(power_mag.data)
        except:
            raise ValidationError('Formato: a+bj ou a-bj')

    def validate_voltage_mag(self, voltage_mag):
        try:
            complex(voltage_mag.data)
        except:
            raise ValidationError('Formato: a+bj ou a-bj')
    
    def validate_impedance_mag(self, impedance_mag):
        try:
            complex(impedance_mag.data)
        except:
            raise ValidationError('Formato: a+bj ou a-bj')
            
    def validate_t1(self, t1):
        for attr_t1, value_t1 in t1.__dict__.items():
            if attr_t1 == 'data' and isinstance(value_t1, int):
                if value_t1 == 0 :
                    raise ValidationError('A barra selecionével do gerador não pode ser a barra de referência, barra[0].')
                if value_t1 < 0:
                    raise ValidationError('Apenas inteiros positivos na numeração das barras.')

    def validate_submit_gen(self, submit_gen):
        if self.power_mag.errors or self.voltage_mag.errors or self.impedance_mag.errors or self.t1.errors:
            raise ValidationError('Corrija os campos acima.')

class PuTransformerForm(FlaskForm):
    # Transformador
    power_mag = StringField('Potência')
    power_mult = SelectField('Potência Mult', choices=mult_choices['power'])
    power_measure = SelectField('Potência Medida', choices=measurement_choices['power'])
    high_voltage_mag = StringField('Alta Tensão')
    high_voltage_mult = SelectField('Alta Tensão Mult', choices=mult_choices['voltage'])
    high_voltage_measure = SelectField('Alta Tensão Medida', choices=measurement_choices['voltage'])
    low_voltage_mag = StringField('Baixa Tensão')
    low_voltage_mult = SelectField('Baixa Tensão Mult', choices=mult_choices['voltage'])
    low_voltage_measure = SelectField('Baixa Tensão Medida', choices=measurement_choices['voltage'])
    impedance_mag = DecimalField('Impedância')
    impedance_mult = SelectField('Impedância Mult', choices=mult_choices['impedance'])
    impedance_measure = SelectField('Impedância Medida', choices=measurement_choices['comp_impedance'])
    t0 = IntegerField('Terminal-0')
    t1 = IntegerField('Terminal-1')
    submit_tran = SubmitField('Transformador')

    def validate_t0(self, t0):
        for ((attr_t0, value_t0), (attr_t1, value_t1)) in zip(t0.__dict__.items(), self.t1.__dict__.items()):
            if attr_t0 == 'data' and isinstance(value_t0, int) and isinstance(value_t1, int):
                if value_t0 < 0 or value_t1 < 0:
                    raise ValidationError('Os terminais de um transformador não podem estar conectados ao terra, barra[0].')
                if value_t0 == value_t1:
                    raise ValidationError('Os terminais de um transformador não podem ser os mesmos.')

    def validate_power_mag(self, power_mag):
        try:
            complex(power_mag.data)
        except:
            raise ValidationError('Formato: a+bj ou a-bj')

    def validate_high_voltage_mag(self, high_voltage_mag):
        try:
            complex(high_voltage_mag.data)
        except:
            raise ValidationError('Formato: a+bj ou a-bj')

    def validate_low_voltage_mag(self, low_voltage_mag):
        try:
            complex(low_voltage_mag.data)
        except:
            raise ValidationError('Formato: a+bj ou a-bj')

    def validate_impedance_mag(self, impedance_mag):
        try:
            complex(impedance_mag.data)
        except:
            raise ValidationError('Formato: a+bj ou a-bj')
            
    def validate_submit_tran(self, submit_tran):
        if self.power_mag.errors or self.high_voltage_mag.errors or self.low_voltage_mag.errors or self.impedance_mag.errors or self.t0.errors:
            raise ValidationError('Corrija os campos acima.')
            

class PuShortTlineForm(FlaskForm):
    # Linha de Transmissão Pequena
    series_impedance_mag = StringField('Impedância')
    series_impedance_mult = SelectField('Impedância Mult', choices=mult_choices['impedance'])
    series_impedance_measure = SelectField('Impedância Medida', choices=measurement_choices['series_impedance'])
    t0 = IntegerField('Terminal-0')
    t1 = IntegerField('Terminal-1')
    lenght = StringField('Comprimento')
    submit_stl = SubmitField('Linha de Transmissão Pequena')

    def validate_t0(self, t0):
        for ((attr_t0, value_t0), (attr_t1, value_t1)) in zip(t0.__dict__.items(), self.t1.__dict__.items()):
            if attr_t0 == 'data' and isinstance(value_t0, int) and isinstance(value_t1, int):
                if value_t0 < 0 or value_t1 < 0:
                    raise ValidationError('Os terminais de um Linha de Transmissão não podem estar conectados ao terra, barra[0].')
                if value_t0 == value_t1:
                    raise ValidationError('Os terminais de um Linha de Transmissão não podem ser os mesmos.')
            
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

    def validate_submit_stl(self, submit_stl):
        if self.series_impedance_mag.errors or self.t0.errors or self.lenght.errors:
            raise ValidationError('Corrija os campos acima.')


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
    
    def validate_t0(self, t0):
        for ((attr_t0, value_t0), (attr_t1, value_t1)) in zip(t0.__dict__.items(), self.t1.__dict__.items()):
            if attr_t0 == 'data' and isinstance(value_t0, int) and isinstance(value_t1, int):
                if value_t0 < 0 or value_t1 < 0:
                    raise ValidationError('Os terminais de um Linha de Transmissão não podem estar conectados ao terra, barra[0].')
                if value_t0 == value_t1:
                    raise ValidationError('Os terminais de um Linha de Transmissão não podem ser os mesmos.')
            
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

    def validate_submit_mtl(self, submit_mtl):
        if self.series_impedance_mag.errors or self.shunt_impedance_mag.errors or self.t0.errors or self.lenght.errors:
            raise ValidationError('Corrija os campos acima.')
            

class PuSystemBasisForm(FlaskForm):
    power_mag = StringField('Potência')
    power_mult = SelectField('Potência Mult', choices=mult_choices['power'])
    power_measure = SelectField('Potência Medida', choices=measurement_choices['power'])
    voltage_mag = StringField('Tensão')
    voltage_mult = SelectField('Tensão Mult', choices=mult_choices['voltage'])
    voltage_measure = SelectField('Tensão Medida', choices=measurement_choices['voltage'])
    bar = IntegerField('Barra')
    submit_sb = SubmitField('Bases do Sistema')

    def validate_power_mag(self, power_mag):
        try:
            complex(power_mag.data)
        except:
            raise ValidationError('Formato: a+bj ou a-bj')

    def validate_voltage_mag(self, voltage_mag):
        try:
            complex(voltage_mag.data)
        except:
            raise ValidationError('Formato: a+bj ou a-bj')
            
    def validate_bar(self, bar):
        for attr_bar, value_bar in bar.__dict__.items():
            if attr_bar == 'data' and isinstance(value_bar, int):
                if value_bar == 0:
                    raise ValidationError('A tensão de base do sistema não pode ser dada na barra Terra, barra[0].')
                if value_bar < 0:
                    raise ValidationError('Apenas inteiros positivos na numeração das barras.')

    def validate_submit_sb(self, submit_sb):
        if self.power_mag.errors or self.voltage_mag.errors or self.bar.errors:
            raise ValidationError('Corrija os campos acima.')


class PuLoadForm(FlaskForm):
    # Carga
    power_mag = StringField('Potência')
    power_mult = SelectField('Potência Mult', choices=mult_choices['power'])
    power_measure = SelectField('Potência Medida', choices=measurement_choices['power'])
    power_factor_mag = StringField('Fator de Potência')
    power_factor_characteristic = SelectField('Característica Fator de Potência', choices=characteristic['power_factor'])
    t1 = IntegerField('Terminal-1')
    submit_ld = SubmitField('Carga')

    def validate_power_mag(self, power_mag):
        try:
            complex(power_mag.data)
        except:
            raise ValidationError('Formato: a+bj ou a-bj')
            
    def validate_power_factor_mag(self, power_factor_mag):
        try:
            float(power_factor_mag.data)
        except:
            raise ValidationError(f'{power_factor_mag.data} não é um fator de potência válido. ]0, 1]')

    def validate_t1(self, t1):
        for attr_t1, value_t1 in t1.__dict__.items():
            if attr_t1 == 'data' and isinstance(value_t1, int):
                if value_t1 == 0 :
                    raise ValidationError('A barra selecionével da carga não pode ser a barra de referência, barra[0].')
                if value_t1 < 0:
                    raise ValidationError('Apenas inteiros positivos na numeração das barras.')

    def validate_submit_ld(self, submit_ld):
        if self.power_mag.errors or self.power_factor_mag.errors or self.t1.errors:
            raise ValidationError('Corrija os campos acima.')


class PuForm(FlaskForm):
    # Finalizar entrada
    submit_pu = SubmitField('Converter a PU')


class ClearObjForm(FlaskForm):
    submit_clear = SubmitField('Novo Problema PU')

class EditAccountForm(FlaskForm):
    submit_edit = SubmitField('Editar')
    

class UpdateAccountForm(FlaskForm):
    username = StringField('Nome')
    email = StringField('E-mail')
    picture = FileField('Imagem de Perfil', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Atualizar')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Este usuário já existe. Por favor escolha outro.')

    def validate_email(self, email):
        if email.data != current_user.email:    
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Este e-mail já está cadastrado. Por favor escolha outro.')