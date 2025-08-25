from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import pandas as pd
import os
from blockchain_logger import log_alert_in_blockchain


app = FastAPI()

# Definim structura datelor așteptate de la senzor
class Vitals(BaseModel):
    patient_id: int
    heart_rate: int
    bp_sys: int
    bp_dia: int
    spo2: int

# Nume fișier CSV în care vom salva datele
DATA_FILE = "vitals_data.csv"

# Inițializăm fișierul dacă nu există
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["timestamp", "patient_id", "heart_rate", "bp_sys", "bp_dia", "spo2"])
    df.to_csv(DATA_FILE, index=False)

@app.post("/api/v1/vitals")
def receive_vitals(vitals: Vitals):
    # Salvăm în vitals_data.csv
    df = pd.read_csv(DATA_FILE)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_entry = {
        "timestamp": timestamp,
        "patient_id": vitals.patient_id,
        "heart_rate": vitals.heart_rate,
        "bp_sys": vitals.bp_sys,
        "bp_dia": vitals.bp_dia,
        "spo2": vitals.spo2
    }
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

    # Verificăm praguri și salvăm alertele în alerts.csv
    alerts = []
    if vitals.heart_rate > 120 or vitals.heart_rate < 50:
        alerts.append(f"Puls anormal: {vitals.heart_rate}")
    if vitals.spo2 < 90:
        alerts.append(f"SpO2 scăzut: {vitals.spo2}")
    if vitals.bp_sys > 160 or vitals.bp_sys < 90:
        alerts.append(f"Tensiune sistolică anormală: {vitals.bp_sys}")

    if alerts:
        alert_df = pd.DataFrame([{
            "timestamp": timestamp,
            "patient_id": vitals.patient_id,
            "alerts": " | ".join(alerts)
        }])
        # Verificăm dacă există fișierul alerts.csv
        if os.path.exists("alerts.csv"):
            old_alerts = pd.read_csv("alerts.csv")
            alert_df = pd.concat([old_alerts, alert_df], ignore_index=True)
        alert_df.to_csv("alerts.csv", index=False)
        
        try:
            from blockchain_logger import log_alert_in_blockchain
            log_alert_in_blockchain(" | ".join(alerts))
        except Exception as e:
            print(f"⚠️ Eroare la logarea în blockchain: {e}")
        
        
    return {"message": "Datele au fost primite și verificate!"}
    # logare automată în blockchain
        
    try:
        blockchain_message = f"Alerte pacient {vitals.patient_id}: {' | '.join(alerts)}"
        log_alert_in_blockchain(blockchain_message)
    except Exception as e:
        print("❌ Nu s-a putut loga alerta în blockchain:", e)

