import sqlite3

from service.film import MovieProfile
from scoring import movie_score



def build_movie_profile(row):

    return MovieProfile(
        title=row["title"],
        runtime=row["runtime"],
        release_year=row["year"],
        genres=row["genres"],
        language=row["language"],
    )



def score_database(db_path, user_profile):

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM movies")

    movies = cursor.fetchall()

    results = []

    for row in movies:

        movie = build_movie_profile(row)

        final_score, details = movie_score(user_profile, movie)

        results.append((row["id"], final_score))

    conn.close()

    return results



def save_scores(db_path, results):

    conn = sqlite3.connect(db_path)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scores(
            movie_id INTEGER PRIMARY KEY,
            score REAL
        )
    """)

    cursor.execute("DELETE FROM scores")

    cursor.executemany(
        "INSERT INTO scores(movie_id, score) VALUES (?, ?)",
        results
    )

    conn.commit()

    conn.close()



if __name__ == "__main__":

    from service.questionnaire import UserProfile

    DATABASE = "data/movies.db"

    print("=== Questionnaire ===")

    user_profile = UserProfile(
        max_runtime=135,
        target_year=2000,
        sigma_year=12,
        genres=["Réflexion"],
        language="fr",
    )
    
    print("\nProfil utilisateur créé avec succès.")

    print("\nCalcul des scores...")

    results = score_database(DATABASE, user_profile)

    print(f"{len(results)} films évalués.")

    save_scores(DATABASE, results)

    print("Scores enregistrés dans la table 'scores'.")