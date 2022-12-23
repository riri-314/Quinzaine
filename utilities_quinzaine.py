#python file with all the function related to operation on tables 15n and 15n_list
import sqlite3

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

#This function creat a table for a new 15n and take as imput the number of the 15n
#Lines "stock" and lines "ventes" are created each day (for "ventes") or each time we incert a new stock (for "stock") 

def Init15nDB(numero):
    connection = sqlite3.connect('quinzaine.db')
    cursor = connection.cursor()
    numerobis = str(numero)
    table1 = 'CREATE TABLE IF NOT EXISTS "'
    table2 = '" (id_quinzaine INTEGER PRIMARY KEY NOT NULL, stock INTEGER)'
    table_15n = table1 + numerobis + table2
    
    cursor.execute(table_15n)

    connection.commit()
    connection.close()
    return 1

 #creat new table with numero as name and add it into 15n list and put it as active 
 #input:
 #numero = numero of the new 15n ex:88
 #Chef_15n = chef 15n of the new 15n ex:cap48
 #annee = year of the new 15n ex:2022-2023
def nouvelle_15n(numero, Chef_15n, annee):
    Init15nDB(numero)
    add_to_quinzaine_list(numero, Chef_15n, annee)
    switch_15n(numero)
    return 1

def switch_15n(numero):
    #switch currect 15n to "numero" 15n
    num = []
    num.append(numero)
    set_inactif = "UPDATE quinzaine_list SET actif = 0"
    cursor.execute(set_inactif)
    set_actif = "UPDATE quinzaine_list SET actif = 1 WHERE id_quinzaine = ? "
    cursor.execute(set_actif, num[:])
    connection.commit()
    return 1

def add_to_quinzaine_list(numero, chef_15n, annee):
    #add a line in quinzaine_list db
    data = []
    data.append(numero)
    data.append(chef_15n)
    data.append(0)
    data.append(annee)
    #print(data)
    add_line = ("INSERT INTO quinzaine_list (id_quinzaine, auteur, actif, annee) VALUES(?, ?, ?, ?)")
    cursor.execute(add_line, data[:])
    connection.commit()
    return 1

def initDB():
    connection = sqlite3.connect('quinzaine.db')

    # Connecting to the geeks database
    cursor = connection.cursor()

    # Creating a cursor object to execute
    # SQL queries on a database table
    cursor.execute('''CREATE TABLE IF NOT EXISTS bieres(
                    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom                     TEXT        NOT NULL,
                    format                  INTEGER     NOT NULL,
                    nombre_dans_contenant   INTEGER     NOT NULL,
                    type                    TEXT        NOT NULL,
                    degre                   INTEGER     NOT NULL,
                    prix_vente              INTEGER     NOT NULL,
                    prix_achat              INTEGER     NOT NULL,
                    a_un_barecode           INTEGER     NOT NULL,
                    barecode                TEXT        NOT NULL,
                    disponible_sur_carte    INTEGER     NOT NULL
                    );
                    ''')

    #15n table will be init in a other python file

    cursor.execute("""CREATE TABLE IF NOT EXISTS quinzaine_list(
                    id_quinzaine            INTEGER PRIMARY KEY NOT NULL,
                    auteur                  TEXT        NOT NULL,
                    actif                   INTEGER     NOT NULL,
                    annee                   TEXT        NOT NULL
                    );
                    """)



    cursor.execute('''CREATE TABLE IF NOT EXISTS plateau(
                    id_plateau              INTEGER PRIMARY KEY NOT NULL,
                    id_biere1               INTEGER     NOT NULL,
                    id_biere2               INTEGER     NOT NULL,
                    id_biere3               INTEGER     NOT NULL,
                    id_biere4               INTEGER     NOT NULL,
                    id_biere5               INTEGER     NOT NULL,
                    id_biere6               INTEGER     NOT NULL,
                    prix                    INTEGER     NOT NULL,
                    FOREIGN KEY (id_biere1) REFERENCES bieres(id),
                    FOREIGN KEY (id_biere2) REFERENCES bieres(id),
                    FOREIGN KEY (id_biere3) REFERENCES bieres(id),
                    FOREIGN KEY (id_biere4) REFERENCES bieres(id),
                    FOREIGN KEY (id_biere5) REFERENCES bieres(id),
                    FOREIGN KEY (id_biere6) REFERENCES bieres(id)
                    );
                    ''')

    connection.commit()
    connection.close()

    return 1