from flask import Flask, render_template, json
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField

app = Flask(__name__)
app.secret_key = 'my-super-secret-phrase-I-dont-tell-this-to-nobody'

with open("inf.json", "r") as f:
    contents = json.load(f)
goals = contents[0]
contents=contents[1]


days = {
        'fri': "Пятница", "wed": 'Среда',
        "sat": 'Суббота', "tue": 'Вторник',
        "mon": 'Понедельник', "thu": 'Четверг', "sun": "Воскресенье"
    }

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

    return render_template('profile.html', id=id, sim=sim)


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
def render_form(id, time, day):

    sim = 0
    for i in contents:
        if id in i.values():
            sim = i
    form = UserForm()

    return render_template("booking.html",day=day, days=days, form=form, sim=sim, time=time)

# принимаем форму
@app.route("/booking_done/", methods=["POST"])
def render_save():
    dat=[]
    inform=[]
    form = UserForm()
    name = form.name.data
    phone = form.phone.data
    dat.append(name)
    dat.append(phone)
    inform.append(dat)
    print(inform)
    f=open('booking.json')
    with open("booking.json", "a") as f:
        f.dump(inform)
    f.close()
    return render_template("booking_done.html",days=days, name=name, phone=phone)


if __name__ == '__main__':
    app.run()
