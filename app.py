from flask import Flask, render_template, json
import random
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required

app = Flask(__name__)
app.secret_key = 'my-super-secret-phrase-I-dont-tell-this-to-nobody'

with open("inf.json", "r") as f:
    contents = json.load(f)


@app.route('/')
def main():
    inf = 0
    return render_template('index.html', inf=inf)


@app.route('/goals/<int:goal>/')
def goal():
    return render_template('goal.html')


@app.route('/profiles/<int:id>/')
def profile(id):
    sim = 0
    for i in contents:
        if id in i.values():
            sim = i
    j = 0
    return render_template('profile.html', id=id, sim=sim, j=j)


@app.route('/request/')
def request():
    return render_template('request.html')


@app.route('/request_done/')
def r_done():
    b = {}
    return render_template("request_done.html", b=b, id=id)


class UserForm(FlaskForm):
    name = StringField("Вас зовут")
    phone = StringField("Ваш телефон")
    submit = SubmitField('Записаться на пробный урок')


@app.route('/booking/<int:id>/<day>/<int:time>/')
def booking(id, time, day):
    sim = 0
    for i in contents:
        if id in i.values():
            sim = i
    form = UserForm()
    days = {
        'fri': "Пятница", "wed": 'Среда',
        "sat": 'Суббота', "tue": 'Вторник',
        "mon": 'Понедельник', "thu": 'Четверг', "sun": "Воскресенье"
    }
    return render_template('booking.html', form=form, day=day, time=time, sim=sim, days=days)


@app.route('/booking_done/', methods=["GET", "POST"])
def b_done():
    form = UserForm()
    name = form.name.data
    phone = form.phone.data

    return render_template('booking_done.html', form=form, name=name, phone=phone)


if __name__ == '__main__':
    app.run()
