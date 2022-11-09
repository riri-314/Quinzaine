#python file with all the function related to operation on tables 15n and 15n_list
import sqlite3
connection = sqlite3.connect('quinzaine.db', check_same_thread=False)
cursor = connection.cursor()

def get15n_id():
    quinzaineId = []
    for i in cursor.execute("SELECT id_quinzaine FROM quinzaine_list"):
        quinzaineId.append(i)
    return quinzaineId
    
