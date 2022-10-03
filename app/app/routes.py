from fileinput import filename
from multiprocessing.spawn import import_main_path
from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt
from app.forms import RegistrationForm, LogInForm, PuSystemBasisForm, PuGeneratorForm, PuTransformerForm, PuShortTlineForm, PuMediumTlineForm, PuLoadForm, PuForm, ClearObjForm, UpdateAccountForm, EditAccountForm
from app.models import User, Problem
from flask_login import login_user, current_user, logout_user, login_required
import app.puconvertions as pucv
import sys
import secrets
import os

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

def save_picture(form_picture):
    random_hex  =secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pic', picture_fn)
    form_picture.save(picture_path)
    return picture_fn 

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    edit_account_form = EditAccountForm()
    update_account_form = UpdateAccountForm()
    image_file = url_for('static', filename='profile_pic/' + current_user.image_file)

    if update_account_form.validate_on_submit() and update_account_form.submit.data:
        user_query_username = User.query.filter_by(username=update_account_form.username.data).first()
        user_query_email = User.query.filter_by(email=update_account_form.email.data).first()   
        if current_user == user_query_username and current_user == user_query_email:
            return redirect(url_for('account'))
        else:
            if update_account_form.picture:
                picture_file = save_picture(update_account_form.picture.data)
                current_user.image_file = picture_file
            current_user.username = update_account_form.username.data
            current_user.email = update_account_form.email.data 
            db.session.commit()
            flash(f'Conta atualizada!', 'success')
            return redirect(url_for('account'))
    elif edit_account_form.submit_edit.data:
        update_account_form.username.data = current_user.username
        update_account_form.email.data = current_user.email
    elif update_account_form.errors:
        edit_account_form.submit_edit.data = True
    

    return render_template('account.html', title='Minha Conta', image_file=image_file, 
                            edit_account_form=edit_account_form, update_account_form=update_account_form, 
                            current_user=current_user)

@app.route("/puconversions", methods=['GET', 'POST'])
@login_required
def pu_conversion():
    valid_submit = False
    valid_system_connections = True
    component_list = pucv.FormToObj.get_components()
    sb_form = PuSystemBasisForm()
    gen_form = PuGeneratorForm()
    tran_form = PuTransformerForm()
    short_tline_form = PuShortTlineForm()
    medium_tline_form = PuMediumTlineForm()
    load_form = PuLoadForm()
    pu_form = PuForm()
    clear_obj_form = ClearObjForm()

    if sb_form.validate_on_submit() and sb_form.submit_sb.data:
        valid_submit = True
        component_list = pucv.FormToObj.pu_conv_sb(sb_form)
        # print(f'/routes -> sb_form.validate -> component_list = {component_list}', file=sys.stderr)
    if gen_form.validate_on_submit() and gen_form.submit_gen.data:
        valid_submit = True
        component_list = pucv.FormToObj.generator(gen_form)
        # print(f'/routes -> gen_form.validate -> component_list = {component_list}', file=sys.stderr)
    if tran_form.validate_on_submit() and tran_form.submit_tran.data:
        valid_submit = True
        component_list = pucv.FormToObj.transformer(tran_form)
        # print(f'/routes -> tran_form.validate -> component_list = {component_list}', file=sys.stderr)
    if short_tline_form.validate_on_submit() and short_tline_form.submit_stl.data:
        valid_submit = True
        component_list = pucv.FormToObj.short_tline(short_tline_form)
        # print(f'/routes -> short_tline_form.validate -> component_list = {component_list}', file=sys.stderr)
    if medium_tline_form.validate_on_submit() and medium_tline_form.submit_mtl.data:
        valid_submit = True
        component_list = pucv.FormToObj.medium_tline(medium_tline_form)
        # print(f'/routes -> medium_tline_form.validate -> component_list = {component_list}', file=sys.stderr)
    if load_form.validate_on_submit() and load_form.submit_ld.data:
        valid_submit = True
        component_list = pucv.FormToObj.load(load_form)
        # print(f'/routes -> load_form.validate -> component_list = {component_list}', file=sys.stderr)
    if pu_form.submit_pu.data:
        valid_system_connections = pucv.Validation.validate_system_connections(component_list)
        if valid_system_connections:
            component_list = pucv.run(component_list)
            return redirect(url_for('pu_conversion_results'))

    if valid_submit:
        return redirect(url_for("pu_conversion"))
    elif not valid_system_connections:
        flash(f"Falha de continuidade, verifique a numeração dos terminais.", 'danger')
        return redirect(url_for("pu_conversion"))
    else:
        return render_template("puconversions.html", title='Conversão Pu', sb_form=sb_form, pu_form=pu_form,
                                gen_form=gen_form, tran_form=tran_form, 
                                short_tline_form=short_tline_form, medium_tline_form=medium_tline_form,
                                load_form=load_form, component_list=component_list)


@app.route("/puconversionresults", methods=['GET', 'POST'])
@login_required
def pu_conversion_results():
    clear_obj_form = ClearObjForm()
    component_list = pucv.FormToObj.get_components()
    if clear_obj_form.submit_clear.data:
        component_list = pucv.FormToObj.del_components()
        return redirect(url_for('pu_conversion'))
    return render_template("puconversionresults.html", title='Conversão Pu - Resultados', 
                            clear_obj_form=clear_obj_form, component_list=component_list)