import os
import requests
from dotenv import load_dotenv
from service.questionnaire import Questionnaire


load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")

url = "https://api.themoviedb.org/3/movie/popular"

params = {
    "api_key": API_KEY,
    "language": "fr-FR",
    "page": 1
}

response = requests.get(url, params=params)




questionnaire = Questionnaire()

answers = questionnaire.run()

print("\nRéponses de l'utilisateur :")

for key, value in answers.items():
    print(f"{key} : {value}")

