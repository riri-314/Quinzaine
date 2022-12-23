# Import required modules
import sqlite3
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

