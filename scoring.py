from dataclasses import dataclass
import numpy as np
from service.film import MovieProfile
from service.questionnaire import UserProfile




# ======================================================================
# Liste officielle des genres TMDB
# ======================================================================

ALL_GENRES = [
    "Action",
    "Aventure",
    "Animation",
    "Comédie",
    "Crime",
    "Documentaire",
    "Drame",
    "Familial",
    "Fantastique",
    "Histoire",
    "Horreur",
    "Musique",
    "Mystère",
    "Romantique",
    "Science-Fiction",
    "Téléfilm",
    "Thriller",
    "Guerre",
    "Western",
]



# ======================================================================
# Similarité cosinus
# ======================================================================

def genre_vector(genres: list[str]) -> np.ndarray:
    """
    Convertit une liste de genres en vecteur binaire.
    """

    return np.array(
        [1 if genre in genres else 0 for genre in ALL_GENRES],
        dtype=float,
    )


def cosine_similarity(v1: np.ndarray, v2: np.ndarray) -> float:
    """
    Similarité cosinus entre deux vecteurs.
    """

    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return float(np.dot(v1, v2) / (norm1 * norm2))


def genre_score(user: UserProfile, movie: MovieProfile) -> float:
    """
    Score de similarité des genres.
    """

    u = genre_vector(user.genres)
    m = genre_vector(movie.genres)

    return cosine_similarity(u, m)


# ======================================================================
# Durée
# ======================================================================

def runtime_score(user: UserProfile, movie: MovieProfile) -> float:
    """
    1 si le film est plus court que la durée maximale souhaitée.

    Puis décroissance exponentielle.
    """

    if movie.runtime <= user.max_runtime:
        return 1.0

    delta = movie.runtime - user.max_runtime

    return float(np.exp(-delta / 20))


# ======================================================================
# Année
# ======================================================================

def year_score(user: UserProfile, movie: MovieProfile) -> float:
    """
    Score gaussien autour de l'année souhaitée.
    """

    if movie.release_year is None:
        return 0

    delta = movie.release_year - user.target_year

    return float(
        np.exp(
            -(delta ** 2) /
            (2 * user.sigma_year ** 2)
        )
    )


# ======================================================================
# Langue
# ======================================================================

def language_score(user: UserProfile, movie: MovieProfile) -> float:
    """
    1 si la langue correspond.
    """

    return float(
        user.language.lower() == movie.language.lower()
    )


# ======================================================================
# Pondération
# ======================================================================

WEIGHTS = {

    "runtime": 0.20,

    "year": 0.25,

    "language": 0.10,

}


# ======================================================================
# Score global
# ======================================================================

def movie_score(user: UserProfile, movie: MovieProfile):
    """
    Calcule le score global d'un film.

    Retourne :

        score_final,
        détail_des_scores
    """

    scores = {

        "genre": genre_score(user, movie),

        "runtime": runtime_score(user, movie),

        "year": year_score(user, movie),

        "language": language_score(user, movie),

    }

    final_score = sum(
        scores[key] * WEIGHTS[key]
        for key in WEIGHTS
    )

    return final_score, scores





# Exemple

if __name__ == "__main__":

    user = UserProfile(
        max_runtime=135,
        target_year=2000,
        sigma_year=12,
        genres=["Réflexion"],
        language="fr",
    )

    movie = MovieProfile(
        title="Le Monde de Nemo",
        genres=["Animation", "Familial", "Aventure"],
        runtime=101,
        release_year=2003,
        language="en",
    )

    score, details = movie_score(user, movie)

    print("Film :", movie.title)
    print()

    print("Score final :", round(score, 3))
    print()

    print("Détail :")

    for key, value in details.items():
        print(f"{key:10s}: {value:.3f}")