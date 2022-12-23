import sqlite3
from init15nDB import *
from quinzaine import *
#initDB.py init quinzaine.db and tables bieres, plateau, quinzaine_list
#Init15nDB(numero) creat a new table in quinzaine.db with name "numero"

connection = sqlite3.connect('quinzaine.db', check_same_thread=False)
cursor = connection.cursor()


Init15nDB(87)
add_to_quinzaine_list(87, "CAP", "2022-2023")
Init15nDB(88)
add_to_quinzaine_list(88, "CAP", "2022-2023")
switch_15n(87)