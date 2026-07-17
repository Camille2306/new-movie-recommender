from dotenv import load_dotenv
from service.questionnaire import Questionnaire



testquestionnaire = Questionnaire()

answers = testquestionnaire.run()
user = testquestionnaire.build_profile()

print("\nRéponses de l'utilisateur :")

for key, value in answers.items():
    print(f"{key} : {value}")

print("\nProfil de l'utilisateur :")

for key, value in user.__dict__.items():
    print(f"{key} : {value}")



