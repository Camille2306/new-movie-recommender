from dataclasses import dataclass  #fonction python qui permet de créer des classes de données
from typing import List, Optional
import math


# -----------------------------
# Description d'un film
# -----------------------------

@dataclass
class Film:
    title: str
    runtime: int                    # minutes
    release_year: int
    genres: List[str]
    language: str                   # "fr", "en", ...
    black_and_white: bool
    silent: bool
    sadness: float                  # 0 -> joyeux, 10 -> très triste
    popularity: float               # TMDB popularity
    vote_average: float             # /10
    vote_count: int




# -----------------------------
# Fonctions de scoring
# -----------------------------


def runtime_score(runtime, max_runtime):

if max_runtime is None:
    return 100

if runtime <= max_runtime:
    return 100

return max(0, 100 - (runtime - max_runtime))


def year_score(year, target_year, sigma=12):

    if target_year is None:
        return 100

    d = year - target_year

    return 100 * math.exp(-(d ** 2) / (2 * sigma ** 2))


def genre_score(movie_genres, wanted_genres):

    if not wanted_genres:
        return 100

    intersection = len(set(movie_genres) & set(wanted_genres))

    return 100 * intersection / len(wanted_genres)


def language_score(movie_language, wanted_language):

    if wanted_language is None:
        return 100

    return 100 if movie_language == wanted_language else 0


def black_white_score(movie, forbid):

    if not forbid:
        return 100

    return 0 if movie.black_and_white else 100


def silent_score(movie, forbid):

    if not forbid:
        return 100

    return 0 if movie.silent else 100


def sadness_score(movie_sadness, target):

    if target is None:
        return 100

    d = abs(movie_sadness - target)

    return max(0, 100 - 10 * d)


def popularity_score(movie, mode):

    if mode is None:
        return 100

    # Grand classique
    if mode == "classic":
        return min(100,
                   movie.vote_average * 7 +
                   math.log(movie.vote_count + 1) * 8)

    # Film de niche
    elif mode == "niche":

        score = (10 - movie.popularity / 20) * 10

        return max(0, min(100, score))

    # Film populaire

    elif mode == "popular":

        score = movie.popularity * 2

        return min(100, score)

    return 100
