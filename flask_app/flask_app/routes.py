
from multiprocessing.spawn import import_main_path
from flask import render_template, url_for, flash, redirect, request
from flask_app import app, db, bcrypt
from flask_app.forms import RegistrationForm, LogInForm, PuGeneratorForm, PuTransformerForm
from flask_app.models import User, Problem
from flask_login import login_user, current_user, logout_user, login_required
import flask_app.puconvertions as pucv
import sys

db.create_all()
titles = ['Pu Conversion Tool', 'Register', 'Login']

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Conta criada para {form.username.data}! Você pode agora iniciar uma sessão.', 'success')
        return redirect(url_for('login'))
    return render_template("register.html", title=titles[1], form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LogInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f"Seja bem vindo {user.username}", 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f"Sessão não pode ser iniciada, cheque e-mail e senha!", 'danger')
    return render_template('login.html', title=titles[2], form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Minha Conta')

@app.route("/puconversions", methods=['GET', 'POST'])
@login_required
def pu_conversion():
    component_list = pucv.FormToObj.get_components()
    gen_form = PuGeneratorForm()
    tran_form = PuTransformerForm()
    if gen_form.validate_on_submit():
        component_list = pucv.FormToObj.generator(gen_form)
    if tran_form.validate_on_submit():
        component_list = pucv.FormToObj.transformer(tran_form)
    return render_template("puconversions.html", title='Conversão Pu', gen_form=gen_form, tran_form=tran_form, component_list=component_list)