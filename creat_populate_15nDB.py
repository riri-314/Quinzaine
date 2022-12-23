import sqlite3
from utilities_quinzaine import *
#Init15nDB(numero) creat a new table in quinzaine.db with name "numero"

#you have to delete quinzaine.db before uning this file to get a new and clean db but be CAREFULL you will abviously lose all data in the old database
initDB() #initDB, creat tables: bieres, plateu, quinzaine_list


connection = sqlite3.connect('quinzaine.db', check_same_thread=False)
cursor = connection.cursor()


Init15nDB(87) #add table "87" for the 87 éme 15n
add_to_quinzaine_list(87, "CAP", "2022-2023") #add 87 éme 15n to the list to be tracked, and name+date
Init15nDB(88)
add_to_quinzaine_list(88, "CAP", "2022-2023")
switch_15n(87) #sitch acitve 15n to 87éme

#add bieres from csv