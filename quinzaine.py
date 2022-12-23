#python file with all the function related to operation on tables 15n and 15n_list
import sqlite3
from init15nDB import *

connection = sqlite3.connect('quinzaine.db', check_same_thread=False)
cursor = connection.cursor()

def get15n_id():
    quinzaineId = []
    for i in cursor.execute("SELECT id_quinzaine FROM quinzaine_list"):
        tmp = []
        for j in i:
            if type(j) == int:
                tmp.append(j)
        quinzaineId.append(tmp[0])
    return quinzaineId
 #input:
 #numero = numero of the new 15n ex:88
 #Chef_15n = chef 15n of the new 15n ex:cap48
 #annee = year of the new 15n ex:2022-2023
def nouvelle_15n(numero, Chef_15n, annee):
    Init15nDB(numero)
    add_to_quinzaine_list(numero, Chef_15n, annee)
    switch_15n(numero)
    return

def switch_15n(numero):
    #switch currect 15n to "numero" 15n
    num = []
    num.append(numero)
    set_inactif = "UPDATE quinzaine_list SET actif = 0"
    cursor.execute(set_inactif)
    set_actif = "UPDATE quinzaine_list SET actif = 1 WHERE id_quinzaine = ? "
    cursor.execute(set_actif, num[:])
    connection.commit()
    return

def add_to_quinzaine_list(numero, chef_15n, annee):
    #add a line in quinzaine_list db
    data = []
    data.append(numero)
    data.append(chef_15n)
    data.append(0)
    data.append(annee)
    print(data)
    add_line = ("INSERT INTO quinzaine_list (id_quinzaine, auteur, actif, annee) VALUES(?, ?, ?, ?)")
    cursor.execute(add_line, data[:])
    connection.commit()
    return
    