# from crypt import methods
from turtle import title
from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LogInForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '47665f0caf395f8b7cfb54faac032245'

titles = ['Pu Conversion Tool', 'Register', 'Login']

dummy_input = [
    {  
        'description': 'System base values',
        'power': '100MVA',
        'voltage': '13.8kV in Bar 1'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Conta criada para {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template("register.html", title=titles[1], form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LogInForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@gmail.com' and form.password.data == '12345678':
            flash(f'Seja bem vindo {form.email.data}!', 'success')
            return redirect(url_for('home'))
        else:
            flash(f"Sessão não pode ser iniciada, forneça e-mail e senha adequados!", 'danger')
    return render_template('login.html', title=titles[2], form=form)

@app.route("/puconversions")
def pu_conversion():
    return render_template('puconversions.html', pu_conversion_template_input=dummy_input, title=titles[0])

if __name__ == '__main__':
    app.run(debug=True)