import pandas as pd
import os

# Verificăm dacă există fișierul alerts.csv
if os.path.exists("alerts.csv"):
    df = pd.read_csv("alerts.csv")

    if df.empty:
        print("Nu există alerte înregistrate.")
    else:
        print("\n🟠 Alerte înregistrate:\n")
        for index, row in df.iterrows():
            print(f"[{row['timestamp']}] Pacient ID {row['patient_id']} → {row['alerts']}")
else:
    print("Fișierul alerts.csv nu a fost creat încă.")
