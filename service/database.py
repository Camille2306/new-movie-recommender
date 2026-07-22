#Ce fichier construit la structure de la base de données SQLite 
#et insère les films récupérés via l'API, en choisissant les données
#récupérées qui sont pertinentes pour le projet. Il est utilisé 
#par le fichier importer.py

import sqlite3
import unicodedata


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


def has_latin_title(title):
    """
    Retourne True si le titre contient au moins une lettre latine.

    Exemples acceptés :
        Parasite
        Le Voyage de Chihiro
        Seven Samurai
        Amélie

    Exemples refusés :
        四大名妓之李香君
        愛のぬくもり
        기생충
        Преступление
    """

    for char in title:
        if char.isalpha():
            try:
                if "LATIN" in unicodedata.name(char):
                    return True
            except ValueError:
                pass

    return False







#fonction qui permet d'insérer un film dans la base de données SQLite
def insert_movie(connection, movie):

    # On ignore les films pour adultes
    if movie.get("adult", False):
        return
    # On ignore les films qui n'ont pas de titre en latin
    if not has_latin_title(movie["title"]):
        return

    # On ignore les films sans genre
    if not movie.get("genres"):
        return

    
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



def get_top_movies(connection, limit=10):
    """
    Retourne les films ayant les meilleurs scores.

    Paramètres
    ----------
    connection : sqlite3.Connection
        Connexion à la base de données.
    limit : int
        Nombre de films à retourner (10 par défaut).

    Retour
    ------
    list[tuple]
        Liste des films triés par score décroissant.
        Chaque élément contient :
        (id, title, score)
    """

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            movies.id,
            movies.title,
            scores.score
        FROM movies
        INNER JOIN scores
            ON movies.id = scores.movie_id
        ORDER BY scores.score DESC
        LIMIT ?
    """, (limit,))

    return cursor.fetchall()



#exemple
if __name__ == "__main__":

    connection = connect()

    top_movies = get_top_movies(connection)

    for movie_id, title, score in top_movies:
        print(f"{title} : {score:.3f}")