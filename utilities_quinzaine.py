#python file with all the function related to operation on tables 15n and 15n_list
import sqlite3
import csv
import random

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

# return numero of the active 15n
def get_active_15n():
    out = []
    action1 = "SELECT id_quinzaine FROM quinzaine_list WHERE actif = 1"
    data = cursor.execute(action1)
    connection.commit()
    
    for x in data:
        out.append(x)
    return out[0][0]

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
    # test if 15n numero exist, if exist return 0
    if (get15n_id().count(int(numero)) != 0):
        print("refused to creat 15n because already exist")
        return 0
    Init15nDB(numero)
    add_to_quinzaine_list(numero, Chef_15n, annee)
    #copy list of avalable bieres from older (numero-1) 15n
    availability_id_15n_db(int(numero))
    # creat new stock column
    add_column_15n(numero,0) 
    # add stock from old 15n
     
    add_old_stock(numero) 
        
    # make 15n numero active
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
            #print(x[1:])
        i += 1

    insert_records = "INSERT INTO bieres (nom, format, nombre_dans_contenant, type, degre, prix_vente, prix_achat, barecode) VALUES(?, ?, ?, ?, ?, ?, ?, ?)"
    
    cursor.executemany(insert_records, contents)
    connection.commit()
    return 1

# used to init db and add bieres id and availability in "table" 15n
# return number of biere id 
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


# return list of id from 15n table
def get_bieres_id_from_15n(table):
    numerobis = str(table)
    id = [] #list of id
    action4 = 'SELECT id FROM "'
    action2 = '"'
    action5 = action4 + numerobis + action2
    #get list of id in 15n table
    for i in cursor.execute(action5):
        tmp = []
        for j in i:
            if type(j) == int:
                tmp.append(j)
        id.append(tmp)
    return id

# return 2D list of nom, format, stocks, ventes, ventes,... from table 15n
def get_stocks_ventes_from_15n(table):
    out = []
    numerobis = str(table)
    action1 = 'SELECT * FROM "'
    action2 = '" WHERE disponible_sur_carte = 1'
    action3 = action1 + numerobis + action2
    data = cursor.execute(action3)
    connection.commit()

    action4 = 'SELECT nom,format FROM bieres WHERE id = '
    action5 = ''
    
    id = [] #store the biere id
    out = [] #store the biere data: id, available, stock, ventes, ...
    for x in data:
        #print(x)
        id.append(x[0])
        tmp1 = []
        for y in x:
            tmp1.append(y)
        out.append(tmp1) 
    
    #print(out)
    
    for i in range(len(out)):
        action6 = action4 + str(id[i]) + action5
        #print(action6)
        name_format = cursor.execute(action6)
        connection.commit()
        for z in name_format:
            #print(z)
            out[i][0] = z[0]
            out[i][1] = z[1]
    #print(out)   
    return out

def get_colums_names_from_15n(table):
    numerobis = str(table)
    action1 = 'SELECT * FROM "'
    action2 = '"'
    action3 = action1 + numerobis + action2
    cursor.execute(action3)
    
    out = []
    for x in cursor.description:
        #print((x[0]))
        out.append(x[0]) 
    connection.commit()
    out[0] = "Nom"
    out[1] = "Format"
    return out

#add random stock in the last stock column
# usefull for tests, gestion stock and gestion 15n
# input: data((id0,stock_value0),(id1, stock_value1),..)
# input: sv: "s" for stock and "v" for ventes
def add_stock_or_ventes(table, data, sv):
    d = 0
    stock = 0
    numerobis = str(table)
    action1 = 'SELECT * FROM "'
    action2 = '"'
    action3 = action1 + numerobis + action2
    cursor.execute(action3)
    
    #get last stock column to add stock
    for x in cursor.description:
        if x[0][0] == sv:
            stock = d
        d += 1

    stock_name = cursor.description[stock][0]

    action6 = 'UPDATE "' 
    action7 = '" SET "' 
    action9 = '" = ? WHERE id = ?'
    action8 = action6 + numerobis + action7 + stock_name + action9
    cursor.executemany(action8, data)
    connection.commit()
    return 1

# add last stock from last 15n into new 15n
# input: table = (int) 87, new table
# usefull when creating a new 15n table
def add_old_stock(table):
    numerominus = str(int(table)-1)
    d = 0
    data = []

    action1 = 'SELECT * FROM "'
    action2 = '"'
    action3 = action1 + numerominus + action2
    test = cursor.execute(action3)

    #get last stock column to add stock
    for x in cursor.description:
        if x[0][0] == "s":
            stock = d
        d += 1

    stock_name = cursor.description[stock][0]

    action4 = 'SELECT "' 
    action5 = '", id FROM "'
    action6 = '"'
    action7 = action4 + stock_name + action5 + numerominus + action6


    for i in cursor.execute(action7):
   
        data.append(i)
    add_stock_or_ventes(table, data, "s")

    return 1





#copy id and dispo_sur_carte from old (numero-1) 15n table to new 15n table
# input: table = (int) 87, will add bieres id and availability into table "87" from table "86"
# usefull when creating a new 15n table
def availability_id_15n_db(table):
    numerobis = str(int(table)-1)
    numero = str(table)
    action1 = 'INSERT INTO "'
    action2 = '" (id, disponible_sur_carte) SELECT id, disponible_sur_carte FROM "'
    action5 = '"'
    action3 = action1 + numero + action2 + numerobis + action5
    #print(action3)

    cursor.execute(action3)
    connection.commit()

    return 1

# add new column in table 15n
# type: (int) 0 = stock, 1 = vente
# usefull in gestion stock and scanner
def add_column_15n(table, type):
    ventes = 0
    stock = 0
    numerobis = str(table)
    action1 = 'SELECT * FROM "'
    action2 = '"'
    action3 = action1 + numerobis + action2
    cursor.execute(action3)
    for x in cursor.description:
        if x[0][0] == "v": 
            ventes += 1
        elif x[0][0] == "s":
            stock += 1
        #print((x[0]))
    connection.commit()
    if type == 0:
        action1 = 'ALTER TABLE "' 
        action2 = '" ADD "'
        action3 = '" INTEGER'
        name0 = str(stock+1)
        name1 = "stock" + name0
        action4 = action1 + numerobis + action2 + name1 + action3
        #print(action4)
        cursor.execute(action4)
        connection.commit()
        return 1
    
    elif type == 1:
        action1 = 'ALTER TABLE "' 
        action2 = '" ADD "'
        action3 = '" INTEGER'
        name0 = str(ventes+1)
        name1 = "ventes" + name0
        action4 = action1 + numerobis + action2 + name1 + action3
        #print(action4)
        cursor.execute(action4)
        connection.commit()
        return 1
    else:
        
        return 0
        



# change availability of a biere in table 15n
# value: (int) 0=not available, 1=available
# table: (int) 87
# id: biere (int) id 
# usefull in gestion carte
def make_disponible_sur_carte(table, id, value):
    numerobis = str(table)
    data = []
    data.append(value)
    data.append(id)

    action1 = 'UPDATE "'
    action2 = '" SET disponible_sur_carte = ? WHERE id = ?'
    action3 = action1 + numerobis + action2
    cursor.execute(action3, data)
    connection.commit()

    return 1


# output: a array of array with 15n_id chef and année
# usefull to see data in gestion 15n
def get_15n_chef_annee():
#    id = get15n_id()
    out = []
    action1 = 'SELECT id_quinzaine, auteur, annee FROM quinzaine_list'
    tmp = cursor.execute(action1)
    for x in tmp:
        out.append(x)
    #print(out[1][1]) 
    connection.commit()
    return out

# input: list of bieres id from get_bieres_id_from_15n(87)
# usefull for debug
def generate_random_data(id):
    data = []
    for i in range(len(id)):
        tmp = []
        tmp.append(random.randint(5,48))
        tmp.append(id[i][0])
        data.append(tmp)
    return data

def get_carte(table):
    action1 = 'SELECT * FROM bieres WHERE id = '
    action2 = ''
    id = get_bieres_id_from_15n(table)
    data = []
    for i in range(len(id)):
        id_tmp = str(id[i][0])
        action3 = action1 + id_tmp + action2
        data_raw = cursor.execute(action3)
        connection.commit()
        out = []
        for x in data_raw:
            tmp = []
            for y in x:
                tmp.append(y)
            
        data.append(tmp)
    #print(data)
    return data

# make a csv with the latest stock, bire id, biere name, biere format from 15n table
def make_csv_from_15n_table(table):
    # select id and stock from 15n table where available = 1
    # select biere name, biere format from biere table where id = id
    # creat empty "new stock" column in csv
    # output in a csv 
    return 1

def verifie_stock_csv(csv):
    # verifie that id, name verifie what on the biere table
    # verifie data are all int and not négatif
    return 1

def add_stock_from_csv(table,csv):
    #verifie_stock_csv(csv)
    #add_stock(table,csv)
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

get_carte(87)