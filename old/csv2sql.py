# Import required modules
import csv
import sqlite3
 
# Connecting to the geeks database
connection = sqlite3.connect('quizaine.db')
 
# Creating a cursor object to execute
# SQL queries on a database table
cursor = connection.cursor()
 
# Table Definition
create_table = '''CREATE TABLE IF NOT EXISTS bieres(
                id                  INTEGER PRIMARY KEY AUTOINCREMENT,
                name                TEXT        NOT NULL,
                format              INTEGER     NOT NULL,
                nombre_dans_casier  INTEGER     NOT NULL,
                type                TEXT        NOT NULL,
                degre               INTEGER     NOT NULL,
                prix_vente          INTEGER     NOT NULL,
                prix_achat          INTEGER     NOT NULL,
                stock               INTEGER     NOT NULL,
                barecode            TEXT        NOT NULL
                );
                '''
 
# Creating the table into our
# database
cursor.execute(create_table)
 
# Opening the person-records.csv file
file = open('bieres.csv')
 
# Reading the contents of the
# person-records.csv file
contents = csv.reader(file)
 
# SQL query to insert data into the
# person table
insert_records = "INSERT INTO bieres (id, name, format, nombre_dans_casier, type, degre, prix_vente, prix_achat, stock, barecode) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
 
# Importing the contents of the file
# into our person table
cursor.executemany(insert_records, contents)
 
# SQL query to retrieve all data from
# the person table To verify that the
# data of the csv file has been successfully
# inserted into the table
select_all = "SELECT * FROM bieres"
rows = cursor.execute(select_all).fetchall()
 
# Output to the console screen
for r in rows:
    print(r)
 
# Committing the changes
connection.commit()
 
# closing the database connection
connection.close()