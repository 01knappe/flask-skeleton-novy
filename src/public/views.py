"""
Logic for dashboard related routes
"""
from flask import Blueprint, render_template
from .forms import LogUserForm, secti,masoform, vstupnitestform, parentform, childform
from ..data.database import db
from ..data.models import LogUser, Parent, Child
blueprint = Blueprint('public', __name__)

@blueprint.route('/', methods=['GET'])
def index():
    return render_template('public/index.tmpl')

@blueprint.route('/loguserinput',methods=['GET', 'POST'])
def InsertLogUser():
    form = LogUserForm()
    if form.validate_on_submit():
        LogUser.create(**form.data)
    return render_template("public/LogUser.tmpl", form=form)

@blueprint.route('/loguserlist',methods=['GET'])
def ListuserLog():
    pole = db.session.query(LogUser).all()
    return render_template("public/listuser.tmpl",data = pole)

@blueprint.route('/secti', methods=['GET','POST'])
def scitani():
    form = secti()
    if form.validate_on_submit():
        return render_template('public/vystup.tmpl',hod1=form.hodnota1.data,hod2=form.hodnota2.data,suma=form.hodnota1.data+form.hodnota2.data)
    return render_template('public/secti.tmpl', form=form)

@blueprint.route('/maso', methods=['GET','POST'])
def masof():
    form = masoform()
    if form.validate_on_submit():
        return render_template('public/masovystup.tmpl',hod1=form.hodnota1.data,hod2=form.hodnota2.data,suma=form.hodnota1.data+form.hodnota2.data)
    return render_template('public/maso.tmpl', form=form)

@blueprint.route('/vstupni_test', methods=['GET','POST'])
def vstupnitest():
    from ..data.models import Vysledky
    from sqlalchemy import  func
    from flask import flash
    form = vstupnitestform()
    if form.validate_on_submit():
        vysledek=0
        if form.otazka1.data == 2:
            vysledek = vysledek + 1
        if form.otazka2.data == 0:
            vysledek = vysledek + 1
        if form.otazka3.data.upper() == "ELEPHANT" :
            vysledek = vysledek + 1
        i = Vysledky(username=form.Jmeno.data, hodnoce=vysledek)
        db.session.add(i)
        db.session.commit()
        dotaz = db.session.query(Vysledky.username,Vysledky.hodnoce).all()
        return render_template('public/vysledekvystup.tmpl', data=dotaz)
    return render_template('public/vstupnitest.tmpl', form=form)


@blueprint.route('/nactenijson', methods=['GET', 'POST'])
def nactenijson():
    from flask import jsonify
    import requests, os
    os.environ['NO_PROXY'] = '127.0.0.1'
    proxies = {
        "http": None,
        "https": "http://192.168.1.1:800",
    }

    response = requests.get("https://samples.openweathermap.org/data/2.5/forecast?id=524901&appid=b1b15e88fa797225412429c1c50c122a1", proxies=proxies)
    json_res = response.json()
    data = []
    for radek in json_res["list"]:
        data.append(radek["main"]["temp"])
    #return render_template("public/dataprint.tmpl",data=data)
    #return jsonify(json_res)
    return render_template('public/chart.tmpl', values=data, labels=data, legend="epidemie kurovce v Moskve")



@blueprint.route("/simple_chart",methods=['GET'])
def chart():
    legend = 'Monthly Data'
    labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
    values = [10, 6, 8, 7, 5, 4, 7, 8]
    return render_template('public/chart.tmpl', values=values, labels=labels, legend=legend)




@blueprint.route('/vstup-parent',methods=['GET', 'POST'])
def InsertParent():
    form = parentform()
    if form.is_submitted():
        Parent.create(**form.data)
    return render_template("public/parent.tmpl", form=form)


@blueprint.route('/vstup-child',methods=['GET', 'POST'])
def InsertChild():
    form = childform()
    form.parent_id.choices = db.session.query(Parent.id,Parent.prijmeni).all()
    if form.validate_on_submit():
        Child.create(**form.data)
    return render_template("public/child.tmpl", form=form)



