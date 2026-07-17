from dotenv import load_dotenv
from service.questionnaire import Questionnaire



questionnaire = Questionnaire()

answers = questionnaire.run()
user = questionnaire.build_profile()

print("\nRéponses de l'utilisateur :")

for key, value in answers.items():
    print(f"{key} : {value}")

print("\nProfil de l'utilisateur :")

for key, value in user.__dict__.items():
    print(f"{key} : {value}")



