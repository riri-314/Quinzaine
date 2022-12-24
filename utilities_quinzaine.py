#python file with all the function related to operation on tables 15n and 15n_list
import sqlite3
import csv

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
    numerobis = str(numero)
    table1 = 'CREATE TABLE IF NOT EXISTS "'
    table2 = '" (id INTEGER PRIMARY KEY NOT NULL, disponible_sur_carte INTEGER NOT NULL, FOREIGN KEY (id) REFERENCES bieres(id))'
    table_15n = table1 + numerobis + table2
    
    cursor.execute(table_15n)

    connection.commit()
    return 1

 #creat new table with numero as name and add it into 15n list and put it as active 
 #input:
 #numero = numero of the new 15n ex:88
 #Chef_15n = chef 15n of the new 15n ex:cap48
 #annee = year of the new 15n ex:2022-2023
def nouvelle_15n(numero, Chef_15n, annee):
    Init15nDB(numero)
    add_to_quinzaine_list(numero, Chef_15n, annee)
    #copy list of avalable bieres from older (numero-1) 15n
    availability_id_15n_db(int(numero)) 
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
                    barecode                TEXT
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
                    id_plateau              INTEGER PRIMARY KEY AUTOINCREMENT,
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
    #connection.close()

    return 1

#add data from csv_file to yable bieres in db
def csv_biere_db(csv_file):
    file = open(csv_file)
    raw = csv.reader(file)
    contents = []
    
    i = 0
    for x in raw:
        if (i != 0):
            contents.append(x[1:])
            print(x[1:])
        i += 1

    insert_records = "INSERT INTO bieres (nom, format, nombre_dans_contenant, type, degre, prix_vente, prix_achat, barecode) VALUES(?, ?, ?, ?, ?, ?, ?, ?)"
    
    cursor.executemany(insert_records, contents)
    connection.commit()
    return 1

# used to init db and add bieres id and availability in "table" 15n
# usefull for tests
def id_biere_to_15n_table(table):
    data = []
    num = str(table)
    #data.append(('1', '1'))
    #data.append(('2', '1'))
    #data.append(('3', '1'))

    for i in cursor.execute("SELECT id FROM bieres"):
        tmp = []
        for j in i:
            if type(j) == int:
                tmp.append(j)
                tmp.append(1)
        data.append(tmp)
    #print(data)

    action1 = 'INSERT INTO "'
    action2 = '" (id, disponible_sur_carte) VALUES(?, ?)'
    action3 = action1 + num + action2
    cursor.executemany(action3, data)
    connection.commit()
    return 1


#copy id and dispo_sur_carte from old (numero-1) 15n table to new 15n table
# input: table = (int) 87, will add bieres id and availability into table "87" from table "86"
# usefull when creating a new 15n table
def availability_id_15n_db(table):
    numerobis = str(table-1)
    numero = str(table)
    action1 = 'INSERT INTO "'
    action2 = '" (id, disponible_sur_carte) SELECT id, disponible_sur_carte FROM "'
    action5 = '"'
    action3 = action1 + numero + action2 + numerobis + action5
    #print(action3)

    cursor.execute(action3)
    connection.commit()

    return 1

# change availability of a biere in table 15n
# value: (int) 0=not available, 1=available
# table: (int) 87
# id: biere (int) id 
# usefull in gestion carte
def make_disponible_sur_carte(table, id, value):
    return 1


# add new biere into table biere and into active 15n table and making it available in carte
# biere_data: array
# active 15n: (int) 87
# usefull in gestion carte
def new_biere(biere_data,active_15n):
    #add biere to biere table
    #copy id and add it into active 15n table
    #make new biere available to carte (into active table 15n)
    return 1

#nouvelle_15n(89, "kiki", "oui")
#availability_id_15n_db(88)