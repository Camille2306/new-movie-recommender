#ce fichier fait le lien entre le fichier qui récupère les infos API 
# et celui qui construit la base de données.

#le fichier qui permet de récupérer toutes les infos des films via l'API
from api_client import discover_movies
from api_client import get_movie_details

#le fichier qui permet de gérer la base de données SQLite
from database import connect
from database import create_tables
from database import insert_movie



def import_movies():

    connection = connect()

    create_tables(connection)

    NUMBER_OF_PAGES = 100

    for page in range(1, NUMBER_OF_PAGES + 1):

        print(f"Téléchargement page {page}")

        movies = discover_movies(page)

        for movie in movies["results"]:

            details = get_movie_details(movie["id"])

            insert_movie(connection, details)

    connection.close()

    print("Import terminé.")




if __name__ == "__main__":

    import_movies()



