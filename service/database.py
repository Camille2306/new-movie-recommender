#Ce fichier construit la structure de la base de données SQLite 
#et insère les films récupérés via l'API, en choisissant les données
#récupérées qui sont pertinentes pour le projet. Il est utilisé 
#par le fichier importer.py

import sqlite3



DATABASE_NAME = "data/movies.db"

#fonction qui permet de se connecter à la base de données SQLite
def connect():

    return sqlite3.connect(DATABASE_NAME)

#fonction qui permet de créer les tables dans la base de données SQLite
def create_tables(connection):

    cursor = connection.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS movies(

        id INTEGER PRIMARY KEY,

        title TEXT,

        genres TEXT,

        runtime INTEGER,

        release_date TEXT,

        year INTEGER,

        language TEXT,

        popularity REAL,

        vote_average REAL,

        vote_count INTEGER

    )

    """)

    connection.commit()


#fonction qui permet d'insérer un film dans la base de données SQLite
def insert_movie(connection, movie):

    cursor = connection.cursor()

    release_date = movie.get("release_date", "")

    if release_date:
        year = int(release_date[:4])
    else:
        year = None

    cursor.execute("""

    INSERT OR REPLACE INTO movies

    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

    """, (

        movie["id"],
        movie["title"],
        ", ".join(g["name"] for g in movie["genres"]),
        movie["runtime"],
        movie["release_date"],
        year,
        movie["original_language"],
        movie["popularity"],
        movie["vote_average"],
        movie["vote_count"]

    ))

    connection.commit()