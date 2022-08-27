# from crypt import methods
# from turtle import title
from email.policy import default
from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LogInForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '47665f0caf395f8b7cfb54faac032245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)   
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg') 
    password = db.Column(db.String(60), nullable=False)
    creation_datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    problems = db.relationship('Problem', backref='author', lazy=True)

    def __repr__(self) -> str:
        return f"User('{self.username}', {self.email}, {self.image_file})"


class Problem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    creation_datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self) -> str:
        return f"Problem('{self.username}', {self.creation_datetime}, {self.content})"


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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Conta criada para {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template("puconversions.html", title=titles[0], form=form)

if __name__ == '__main__':
    app.run(debug=True)