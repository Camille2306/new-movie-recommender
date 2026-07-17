#définition du questionnaire sous forme de classe, utile pour quand on fera plusieurs questionnaires en même temps
from dataclasses import dataclass  #fonction python qui permet de créer des classes de données
from typing import List, Optional
import math


class Questionnaire:

    def __init__(self):
        self.answers = {}

    #fonction permettant de poser une question à choix unique à l'utilisateur
    def ask_single_choice(self, question, choices):
        print(f"\n{question}")

        for i, choice in enumerate(choices, start=1):
            print(f"{i}. {choice}")

        while True:
            try:
                answer = int(input("\nVotre choix : "))

                if 1 <= answer <= len(choices):
                    return choices[answer - 1]

                print("Choisissez un numéro valide.")

            except ValueError:
                print("Veuillez entrer un nombre.")

    #fonction permettant de poser une question à choix multiple à l'utilisateur
    def ask_multiple_choice(self, question, choices):
        print(f"\n{question}")

        for i, choice in enumerate(choices, start=1):
            print(f"{i}. {choice}")

        print("\nEntrez plusieurs numéros séparés par une virgule.")
        print("Exemple : 1,4,7")

        while True:
            try:
                answers = input("Vos choix : ")

                indexes = [int(x.strip()) for x in answers.split(",")]

                if all(1 <= i <= len(choices) for i in indexes):
                    return [choices[i-1] for i in indexes]

                print("Un des numéros est invalide.")

            except ValueError:
                print("Format invalide.")

    #fonction permettant de poser toutes les questions du questionnaire à l'utilisateur
    def run(self):

        self.answers["runtime"] = self.ask_single_choice(
            "Combien de temps avez-vous devant vous ?",
            [
                "Film très court (1h15 max)",
                "Un peu de temps mais pas plus que ça (1h30 max)",
                "Pas spécialement limitée par le temps (2h15 max)",
                "Prêt.e pour un marathon (plus de 2h)",
                "Je ne sais pas"
            ]
        )

        self.answers["genres"] = self.ask_multiple_choice(
            "Quels genres aimez-vous ?",
            [
                "Romantique",
                "Horreur",
                "Comédie musicale",
                "Science-fiction",
                "Action",
                "Réflexion",
                "Historique",
                "Comédie",
                "Documentaire",
                "Animation",
                "Peu importe"
            ]
        )

        self.answers["dealbreakers"] = self.ask_multiple_choice(
            "C'est rédhibitoire pour vous :",
            [
                "Film en noir et blanc",
                "Film muet",
                "Aucune de ces options"
            ]
        )

        self.answers["sadness"] = self.ask_single_choice(
            "Quel niveau de tristesse êtes-vous prêt(e) à accepter ?",
            [
                "Je veux quelque chose de léger",
                "Je peux passer des rires aux larmes",
                "J'ai les nerfs accrochés"
            ]
        )

        self.answers["period"] = self.ask_single_choice(
            "Quelle période préférez-vous ?",
            [
                "Très récent (2016 à aujourd'hui)",
                "Récent (2005-2016)",
                "Moyen (1990-2005)",
                "Vieux (1970-1990)",
                "Très vieux (avant 1970)",
                "Je ne sais pas"
            ]
        )

        self.answers["popularity"] = self.ask_single_choice(
            "Quel type de film recherchez-vous ?",
            [
                "Un grand classique du cinéma",
                "Un film peu connu",
                "Un coup de cœur du public"
            ]
        )

        self.answers["language"] = self.ask_single_choice(
            "Quelle langue ?",
            [
                "Français",
                "Anglais",
                "Espagnol",
                "Allemand",
                "Italien",
                "Sans préférence"
            ]
        )

        return self.answers

    
    def build_profile(self):

        runtime_map = {
            "Film très court (1h15 max)": 75,
            "Un peu de temps mais pas plus que ça (1h30 max)": 90,
            "Pas spécialement limitée par le temps (2h15 max)": 135,
            "Prêt.e pour un marathon (plus de 2h)": 999,
            "Je ne sais pas": None
        }

        period_map = {
            "Très récent (2016 à aujourd'hui)": 2020,
            "Récent (2005-2016)": 2010,
            "Moyen (1990-2005)": 1998,
            "Vieux (1970-1990)": 1980,
            "Très vieux (avant 1970)": 1955,
            "Je ne sais pas": None
        }

        language_map = {
            "Français": "fr",
            "Anglais": "en",
            "Espagnol": "es",
            "Allemand": "de",
            "Italien": "it",
            "Sans préférence": None
        }

        sadness_map = {
            "Je veux quelque chose de léger": 2,
            "Je peux passer des rires aux larmes": 5,
            "J'ai les nerfs accrochés": 9
        }

        popularity_map = {
            "Un grand classique du cinéma": "classic",
            "Un film peu connu": "niche",
            "Un coup de cœur du public": "popular"
        }

        genres = self.answers["genres"]

        if "Peu importe" in genres:
            genres = None

        dealbreakers = self.answers["dealbreakers"]

        return UserProfile(

            max_runtime=runtime_map[self.answers["runtime"]],

            target_year=period_map[self.answers["period"]],

            genres=genres,

            language=language_map[self.answers["language"]],

            forbid_black_white="Film en noir et blanc" in dealbreakers,

            forbid_silent="Film muet" in dealbreakers,

            target_sadness=sadness_map[self.answers["sadness"]],

            popularity_mode=popularity_map[self.answers["popularity"]]

        )

        
      
@dataclass
class UserProfile:
    max_runtime: Optional[int]

    target_year: Optional[int]
    sigma_year: float = 12

    genres: Optional[List[str]] = None

    language: Optional[str] = None

    forbid_black_white: bool = False
    forbid_silent: bool = False

    target_sadness: Optional[float] = None

    popularity_mode: Optional[str] = None
    # "classic"
    # "niche"
    # "popular"




