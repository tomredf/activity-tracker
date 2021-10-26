import requests
import os
from datetime import datetime

NUT_APP_ID = os.environ.get("NUT_APP_ID")
NUT_API_KEY = os.environ.get("NUT_API_KEY")
NUT_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"

SHEET_ENDPOINT = os.environ.get("SHEETY_ENDPOINT")
SHEET_TOKEN = os.environ.get("SHEETY_TOKEN")

headers = {
    "x-app-id": NUT_APP_ID,
    "x-app-key": NUT_API_KEY,
    "Content-Type": "application/json"
}


def log_workout(workout_type):

    data = {
        "query": workout_type,
        "gender": "male",
        "weight_kg": 1145,
        "height_cm": 180.34,
        "age": 55
    }

    res = requests.post(url=NUT_ENDPOINT, headers=headers, json=data)
    res.raise_for_status()
    data = res.json()["exercises"][0]

    headers2 = {
        "Content-Type": "application/json",
        "authorization": SHEET_TOKEN
    }

    today = datetime.now()
    day = today.strftime("%d/%m/%Y")
    t = today.strftime("%I:%M:%S %p")

    sheet_inputs = {
        "workout": {
            "date": day,
            "time": t,
            "exercise": data["user_input"],
            "duration": data["duration_min"],
            "calories": data["nf_calories"]
        }
    }

    res2 = requests.post(url=SHEET_ENDPOINT, json=sheet_inputs, headers=headers2)
    res2.raise_for_status()
    print(res2.text)


user_input = input("Please enter your workout: ")

log_workout(user_input)
