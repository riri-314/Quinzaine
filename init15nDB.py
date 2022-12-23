#This function creat a table for a new 15n and take as imput the number of the 15n
#Lines "stock" and lines "ventes" are created each day (for "ventes") or each time we incert a new stock (for "stock") 
 
# Import required modules
import sqlite3

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
