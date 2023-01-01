from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from utilities_quinzaine import *
app = Flask(__name__)

@app.route('/', methods=["POST", "GET"])
def dashbord():
    active_15n = get_active_15n()
    return render_template("dashbord.html", active_15n=active_15n)

@app.route("/scanner")
def scanner():
    active_15n = get_active_15n()

    return render_template("scanner.html", active_15n=active_15n)

@app.route("/gestion_stock")
def gestion_stock():
    active_15n = get_active_15n()
    data = get_stocks_ventes_from_15n(active_15n)
    colums_name = get_colums_names_from_15n(active_15n)
    error_message = "Test error message"
    return render_template("gestion_stock.html", active_15n=active_15n, data = data, error_message = error_message, colums_name = colums_name)

@app.route("/gestion_carte",  methods=["POST", "GET"])
def gestion_carte():
    active_15n = get_active_15n()
    data = get_carte(active_15n)
    error_message = "Test error message"
    return render_template("gestion_carte.html", active_15n=active_15n, error_message=error_message, data=data)

@app.route("/gestion_15n", methods=["POST", "GET"])
def gestion_15n():
    
    error_message = ""
    data = get_15n_chef_annee()
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
            active_15n = get_active_15n()
            return render_template("gestion_15n.html", quinzaines = quinzaines, error_message = "Erreur veuillez selectionner une 15n ou en créer une", last_15n = last_15n, data = data, active_15n=active_15n)
        try:
            int(SelectedQuinzaineId)
        except:
            #creat new 15n

            return redirect(url_for('add_15n', To_add=last_15n))
            #return render_template("add_15n.html")
        try:
            switch_15n(SelectedQuinzaineId)
            print("selected switch 15n")
        except:
            error_message = "error switching 15n"
            active_15n = get_active_15n()
            return render_template("gestion_15n.html", quinzaines = quinzaines, error_message = switched, last_15n = last_15n, data = data, active_15n=active_15n)

        switched = "Switched to "+str(SelectedQuinzaineId)+" éme 15n"
        active_15n = get_active_15n()
        return render_template("gestion_15n.html", quinzaines = quinzaines, error_message = switched, last_15n = last_15n, data = data, active_15n=active_15n)
    else:
        #print("other")
        active_15n = get_active_15n()
        return render_template("gestion_15n.html", quinzaines = quinzaines, error_message = error_message, last_15n = last_15n, data = data, active_15n=active_15n)

@app.route("/add_15n/<To_add>", methods=["POST", "GET"])
def add_15n(To_add):
    error_message = "Test it"
    #print(To_add)
    if request.method == 'POST':
        annee = request.form["annee"]
        chef_15n = request.form["chef_15n"]
        if (0>=len(annee) or len(annee)>10):
            error_message = "Entrez une année valide, pas vide et pas plus de 10 carractères"
            active_15n = get_active_15n()
            return render_template("add_15n.html", To_add = To_add, error_message=error_message, active_15n=active_15n)
        if (0>=len(chef_15n) or len(chef_15n)>15):
            error_message = "Entrez un chef valide, pas vide et pas plus de 15 carractères"
            active_15n = get_active_15n()
            
            return render_template("add_15n.html", To_add = To_add, error_message=error_message, active_15n=active_15n)
        #print(len(annee))
        #print(chef_15n)
        try:
            if nouvelle_15n(To_add, chef_15n, annee):
                error_message = "Quinzaine "+str(To_add)+" ajouté à la base de donnée"
                #print(type(To_add))
                To_add = int(To_add) + 1
        except:
            error_message = "error in creating new 15n"
            active_15n = get_active_15n()
            
            return render_template("add_15n.html", To_add = To_add, error_message=error_message, active_15n=active_15n)

        return redirect(url_for('gestion_15n'))
        #return render_template("add_15n.html", To_add = To_add, error_message=error_message, active_15n=active_15n)
    else:
        active_15n = get_active_15n()

        return render_template("add_15n.html", To_add = To_add, error_message= error_message, active_15n=active_15n)


#@app.route("/gestion_15n/add_15n", methods=["POST", "GET"])
#def add_15n():
#    return render_template("add_15n.html")



if __name__ == '__main__':
#    app.run(host="0.0.0.0")
    app.run()

