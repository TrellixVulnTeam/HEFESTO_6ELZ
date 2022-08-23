from turtle import title
from flask import Flask, render_template

app = Flask(__name__)

titles = ['Pu Conversion Tool']

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

@app.route("/puconversions")
def pu_conversion():
    return render_template('puconversions.html', pu_conversion_template_input=dummy_input, title=titles[0])

if __name__ == '__main__':
    app.run(debug=True)