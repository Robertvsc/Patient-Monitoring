Sistem de Monitorizare a Datelor Pacientilor in Timp Real

Acest proiect implementeaza un sistem modular de monitorizare a pacientilor care colecteaza, afiseaza si securizeaza date vitale in timp real.

Arhitectura sistemului permite:

-Simularea datelor vitale de la senzori (puls, SpO2, tensiune arteriala)
-Salvarea datelor intr-o baza locala CSV
-Vizualizarea datelor si alertelor printr-un dashboard interactiv Streamlit
-Gestionarea rolurilor de acces Admin, Medic, Asistent
-Inregistrarea alertelor medicale pe Blockchain pentru trasabilitate si securitate

Functionalitati:

-Vizualizarea datelor pacientilor in timp real prin grafice si tabele
-Generarea automata de alerte cand valorile depasesc pragurile normale
-Autentificare pe roluri:
-Admin are acces complet si poate sterge alerte sau gestiona utilizatori
-Medic are acces la datele pacientilor si la rapoarte
-Asistent are acces la datele pacientilor si poate adauga observatii
-Salvarea alertelor in Blockchain pentru securitate si audit
-Export rapoarte in format CSV si PDF

Arhitectura

Senzori (Simulator) → Backend FastAPI → Blockchain Logger → CSV (vitals_data.csv si alerts.csv) → Streamlit UI Dashboard

Tehnologii folosite:

-Python 3.11+
-FastAPI pentru backend API
-Streamlit pentru interfata de vizualizare
-Pandas pentru gestionarea datelor
-FPDF pentru generare rapoarte PDF
-Ganache, Remix si Web3.py pentru integrare Blockchain
-CSV pentru stocare locala a datelor si alertelor

Structura proiectului:

-main.py – backend FastAPI care expune API pentru senzori si UI
-simulator_senzor.py – simulator pentru date vitale pacienti
-afisare_alerte.py – script auxiliar pentru afisarea alertelor
-blockchain_logger.py – logarea alertelor in blockchain
-dashboard.py – UI interactiv in Streamlit
-patients.csv – lista pacientilor
-vitals_data.csv – date vitale salvate
-alerts.csv – alerte generate

Instalare si rulare:

Cloneaza proiectul:
-git clone https://github.com/username/monitorizare_pacienti.git
-cd monitorizare_pacienti

Creeaza un mediu virtual si instaleaza dependintele:
-python -m venv .venv
-source .venv/bin/activate pentru Linux sau Mac
-.venv\Scripts\activate pentru Windows
-pip install -r requirements.txt

Ruleaza backend-ul FastAPI:
-uvicorn main:app --reload
-Acces API la adresa http://127.0.0.1:8000

Ruleaza simulatorul de senzori:
-python simulator_senzor.py

Ruleaza interfata grafica Streamlit:
-streamlit run dashboard.py




