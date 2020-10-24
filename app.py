from flask import Flask
from flask import render_template
from flask import json
from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import InputRequired, Length
import random

app = Flask(__name__)
app.secret_key = 'my-super-secret-phrase-I-do-not-tell-this-to-nobody'

with open("inf.json", "r") as f:
    contents = json.load(f)
goales = contents[0]
contents = contents[1]

days = {
    'fri': "Пятница", "wed": 'Среда',
    "sat": 'Суббота', "tue": 'Вторник',
    "mon": 'Понедельник', "thu": 'Четверг', "sun": "Воскресенье"
}


@app.route('/')
def main():
    inf = random.sample(contents, 6)

    return render_template('index.html', inf=inf,goales=goales)


@app.route('/goals/<goal>/')
def goal(goal):
    teachers = []
    for i in contents:
         if goal in i.get("goals"):
            teachers.append(i)
    return render_template('goal.html', teachers=teachers, goal=goal, goales=goales)


@app.route('/profiles/<int:id>/')
def profile(id):
    sim = 0
    for i in contents:
        if id in i.values():
            sim = i

    return render_template('profile.html', id=id, sim=sim, goales=goales)


'''class UserChoice(FlaskForm):
    goal = RadioField("", choices=[("travel", "Для путешествий"), ("study", "Для учебы"),
                                   ("work", "Для работы"),
                                   ("relocate", "Для переезда")])
    hours = RadioField("",
                       choices=[("1-2", "1-2 часа в неделю"), ("3-4", "3-4 часа в неделю"),
                                ("5-6", "5-6 часов в неделю"),
                                ("7-8", "7-8 часов в неделю")])
    name = StringField("Вас зовут", [InputRequired(message="Введите имя"), Length(min=2, max=30)])
    phone = StringField("Ваш телефон", [InputRequired(message="Введите телефон"), Length(min=6, max=20)])
    submit = SubmitField('Найдите мне проподавателя')'''


@app.route('/request/', methods=["GET"])
def request():
    '''form = UserChoice()'''
    form=request.form()
    return render_template('request.html',form=form)


@app.route('/request_done/', methods=["POST"])
def r_done():
    '''g={}; dat=[]
    form = UserChoice()
    names = form.name.data
    phones = form.phone.data
    goals = form.goal.data
    hours = form.hours.data
    g["time"]=hours; g["number"] = phones; g['goal'] = goals
    dat.append(g)'''
    hours = request.form.get("time")
    goals = request.form.get("goal")
    phones = request.form.get("phone")
    names = request.form.get("name")
    if form.validate_on_submit():
        '''json_data = json.load(open("request.json", encoding='utf-8'))
        json_data[names]=dat
        with open("request.json", "w") as f:
            json.dump(json_data, f)
        f.close()'''
        return render_template("request_done.html", goales=goales, hours=hours, phones=phones, names=names, goals=goals, form=form)
    return 'Вернитесь назад'


class UserForm(FlaskForm):
    day = 0
    time = 0
    name = StringField("Вас зовут", [InputRequired(message="Введите имя"), Length(min=2, max=30)])
    phone = StringField("Ваш телефон", [InputRequired(message="Введите телефон"), Length(min=6, max=20)])
    submit = SubmitField('Записаться на пробный урок')


@app.route('/booking/<int:id>/<day>/<time>/')
def render_form(id, time, day):
    sim = 0
    for i in contents:
        if id in i.values():
            sim = i
    form = UserForm()
    UserForm.day = day
    UserForm.time = time
    return render_template("booking.html", day=day, days=days, form=form, sim=sim, time=time)


# принимаем форму
@app.route("/booking_done/", methods = ['POST', 'GET'])
def render_save():
    form = UserForm()
    if form.validate_on_submit():
        dat = []; g={}
        name = form.name.data
        phone = form.phone.data
        day = form.day
        time = form.time
        g["time"] = time; g['phone']=phone; g['day']=day;
        dat.append(g)
        json_data = json.load(open("booking.json", encoding='utf-8'))
        json_data[name] = dat
        with open("booking.json", "w") as f:
            json.dump(json_data, f)
        f.close()
        return render_template("booking_done.html", time=time, day=day, days=days, name=name, phone=phone)
    return 'Вернитесь назад и внимательно заполните поля: имя - минимум 2 символа, телефон - 6'


if __name__ == '__main__':
    app.run()
