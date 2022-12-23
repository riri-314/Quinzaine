from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from quinzaine import *
app = Flask(__name__)

@app.route('/', methods=["POST", "GET"])
def dashbord():
    return render_template("dashbord.html")

@app.route("/scanner")
def scanner():
    return render_template("scanner.html")

@app.route("/gestion_stock")
def gestion_stock():
    return render_template("gestion_stock.html")

@app.route("/gestion_carte",  methods=["POST", "GET"])
def gestion_carte():
    return render_template("gestion_carte.html")


@app.route("/gestion_15n", methods=["POST", "GET"])
def gestion_15n():
    
    error_message = ""
    quinzaines = get15n_id()
    last_15n = quinzaines[-1] + 1
    texte = "créer "+str(last_15n)+" éme 15n"
    quinzaines.append(texte)
    
    if request.method == 'POST':
        SelectedQuinzaineId = request.form["15n_id"]
        print(((SelectedQuinzaineId)))
        #Chef_15n = request.form["chef_15n"]
        #print(Chef_15n)
        #annee = request.form["annee"]
        if (SelectedQuinzaineId == "Choisissez une Quinzaine"):
            return render_template("gestion_15n.html", quinzaines = quinzaines, error_message = "Erreur veuillez selectionner une 15n ou en créer une", last_15n = last_15n)
        try:
            int(SelectedQuinzaineId)
        except:
            return render_template("gestion_15n.html", quinzaines = quinzaines, error_message = "Créer nouvelle 15n.html", last_15n = last_15n)
        switch_15n(SelectedQuinzaineId)
        print("selected switch 15n")
        
        return render_template("gestion_15n.html", quinzaines = quinzaines, error_message = error_message, last_15n = last_15n)
    else:
        print("other")
        return render_template("gestion_15n.html", quinzaines = quinzaines, error_message = error_message, last_15n = last_15n)

@app.route("/gestion_15n/add_15n", methods=["POST", "GET"])
def add_15n():
    return render_template("add_15n.html")



if __name__ == '__main__':
#    app.run(host="0.0.0.0")
    app.run()


#{% extends "layout.html" %}
#{% block title %}Gestion 15n{% endblock %}
#{% block css %}
#    <link rel="stylesheet" href="{{ url_for('static', filename= 'dashbord.css') }}">
#{% endblock %}
#
#{% block content%}
#<div class="rectangle">
#    <h1>
#        Gestion 15n Quinzaine de la bière Belge
#
#    </h1>
#</div>
#<form method="POST">
#    <div>
#        <label for="SelectQuinzaineId">Choix d'une Quinzaine</label>
#        <select name="SelectQuinzaineId" id="SelectQuinzaineId" size="1">
#            <OPTION selected>Choisissez une Quizaine
#            {% for quinzaine in quinzaines %}
#                <OPTION>{{quinzaine}}
#            {% endfor %}
#        </select>
#    </div>
#</form>

#{% extends "layout.html" %}
#{% block title %}Gestion 15n{% endblock %}
#{% block css %}
#<link rel="stylesheet" href="{{ url_for('static', filename= 'dashbord.css') }}">
#{% endblock %}
#{% block content%}
#<div class="request">
#   <div class="rectangle">
#      <h1>
#          Gestion 15n Quinzaine de la bière Belge
#  
#      </h1>
#  </div>
#  <h1>Selectionner 15n qui existe déja</h1>
#  <p>Pour accéder au graphique concernant le nombres de veaux nés vivants et celui des mort-nés,
#    écrivez ou choisissez le nom de famille d'une vache.
#    Le graphique sera généré en fonction de ce nom.
#  </p>
#
#  <form method="POST">
#    <form id="form">
#
#      <datalist id="15n_data" >
#        <select name="15n_select" >
#            <OPTION selected>Choisissez une Quinzaine
#            {% for quinzaine in quinzaines %}
#                <OPTION>{{quinzaine}}
#            {% endfor %}
#        </select>
#
#      <label for="15n_list">or other:</label>
#      </datalist>
#
#      <input list="15n_data" id="15n_list" name="15n_id" size="50" autocomplete="on" />
#
#      <button type="submit">Envoyer</button>
#      <h1>Créer {{last_15n}} éme 15n</h1>
#      
#      <form action="/data" method = "POST">
#        <p>Chef 15n <input type = "text" name = "chef_15n" /></p>
#        <p>Année <input type = "text" name = "annee" /></p>
#        <p><input type = "submit" value = "Submit" /></p>
#      </form>
#      <p>{{error_message}}</p>
#
#</form>
#  </form>
#
#</div>
#{% endblock %}
