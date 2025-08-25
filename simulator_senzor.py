import requests
import random
import time

url = "http://127.0.0.1:8000/api/v1/vitals"

while True:
    data = {
        "patient_id": random.randint(1, 5),
        "heart_rate": random.randint(60, 120),
        "bp_sys": random.randint(100, 140),
        "bp_dia": random.randint(60, 90),
        "spo2": random.randint(85, 100)
    }

    try:
        response = requests.post(url, json=data)
        print(f"Trimis: {data} | Status: {response.status_code}")
    except Exception as e:
        print("Eroare la trimitere:", e)

    time.sleep(5)
