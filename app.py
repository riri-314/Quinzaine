from flask import Flask, render_template, request
import sqlite3
from quinzaine import *
app = Flask(__name__)

@app.route('/')
def dashbord():
    return render_template("dashbord.html")

@app.route("/scanner")
def scanner():
    return render_template("scanner.html")

@app.route("/gestion_stock")
def gestion_stock():
    return render_template("gestion_stock.html")

@app.route("/gestion_carte")
def gestion_carte():
    return render_template("gestion_carte.html")

@app.route("/gestion_15n", methods=('GET','POST'))
def gestion_15n():
    quinzaines = get15n_id()
    
    if request.method == 'POST':
        SelectedQuinzaineId = request.form["SelectQuinzaineId"]
    #get_15n_list_data()
    #render a table with the data
    #scroling menu with 15n numbers and catch user selection
    return render_template("gestion_15n.html", quinzaines = quinzaines)



if __name__ == '__main__':
    app.run(host="0.0.0.0")
