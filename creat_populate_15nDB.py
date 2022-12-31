import sqlite3
import random
import os
from utilities_quinzaine import *


#Init15nDB(numero) creat a new table in quinzaine.db with name "numero"

#you have to delete quinzaine.db before uning this file to get a new and clean db but be CAREFULL you will abviously lose all data in the old database
initDB() #initDB, creat tables: bieres, plateu, quinzaine_list
connection = sqlite3.connect('quinzaine.db', check_same_thread=False)
cursor = connection.cursor()

csv_biere_db("bieres.csv") #add data from bieres.csv to bieres table in db

Init15nDB(87) #add table "87" for the 87 éme 15n
add_to_quinzaine_list(87, "CAP", "2022-2023") #add 87 éme 15n to the list to be tracked, and name+date
id_biere_to_15n_table(87) #add data to table 87, add id biere and make them available
id = get_bieres_id_from_15n(87)

add_column_15n(87, 0) #add stock column
data = generate_random_data(id)
add_stock_or_ventes(87, data, "s") # add stock from data to the last stock column in 87

for x in range(14):
    add_column_15n(87, 1) #add ventes column
    data = generate_random_data(id)
    add_stock_or_ventes(87, data, "v") # add stock from data to the last stock column in 87


nouvelle_15n(88, "CAP", "2022-2023")
add_column_15n(88, 1) #add ventes column
data = generate_random_data(id)
add_stock_or_ventes(88, data, "v") # add stock from data to the last stock column in 87


#add id: 1,2,3 and make them available in 87 88 and add some stock 
#update nouvelle_15n

#id,nom,format,nombre_dans_contenant,type,degre,prix_vente,prix_achat,barecode