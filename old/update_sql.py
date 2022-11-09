import csv
import sqlite3
 
# Connecting to the geeks database
connection = sqlite3.connect('quizaine.db')
 
# Creating a cursor object to execute
# SQL queries on a database table
cursor = connection.cursor()

#open csv file
file = open('bieres.csv')
contents = csv.reader(file)

#get beer is from sql db
id_db = []
for i in cursor.execute("SELECT id from bieres"):
    id_db.append(i[0])

def listOfTuplesTOListOfFloatSmart(list, index = 0):
    try:
        float(list[index])
    except:
        if index < len(list):
            listOfTuplesTOListOfFloatSmart(list, index+1)
        else:
            return
    else:
        list[index] = float(list[index])
        if index < len(list):
            listOfTuplesTOListOfFloatSmart(list, index+1)
        else:
            return

#get beer id from csv
id_csv = []
csv_rows_list = []
for csv_row in contents:
    listOfTuplesTOListOfFloatSmart(csv_row)
    #print(csv_row)
    csv_rows_list.append(csv_row)
    id_csv.append(int(csv_row[:][0]))  
print(csv_rows_list)

# Python code to get difference of two lists
def Diff(li1, li2):
    li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
    return li_dif 
diff_id = Diff(id_csv, id_db)

if (len(diff_id) != 0):
    #add diff_id into sql db
    0

#else compare row by row for diff
#parse db_rows to cast to list of str and float
select_all = "SELECT * FROM bieres"
db_rows_tuple = cursor.execute(select_all).fetchall()
db_rows_list = []
for db_row in db_rows_tuple:
    #if (Diff(r, ))
    db_row = list(db_row)
    listOfTuplesTOListOfFloatSmart(db_row)
    db_rows_list.append(db_row)
print(db_rows_list)

#compare csv_rows_list and db_rows_list
for j in range(len(db_rows_list)):
    diff_row = Diff(csv_rows_list[j], db_rows_list[j])
    print(csv_rows_list[j])
    print(diff_row)
    if (len(diff_row) != 0):
        update_biere = "UPDATE bieres SET name = ?, format = ?, nombre_dans_casier = ?, type = ?, degre = ?, prix_vente = ?, prix_achat = ?, stock = ?, barecode = ? WHERE id = ?"
        cursor.execute(update_biere, csv_rows_list[j][1:])

connection.commit()
connection.close()