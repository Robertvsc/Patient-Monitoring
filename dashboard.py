import streamlit as st
import pandas as pd
import os
from fpdf import FPDF

st.set_page_config(page_title="Monitorizare Pacienți", layout="wide")
st.title("🩺 Dashboard Monitorizare Date Pacienți")

# === Utilizatori ===
users = {
    "admin": {"password": "admin123", "role": "admin"},
    "medic1": {"password": "medic123", "role": "medic"},
    "asistent1": {"password": "asistent123", "role": "asistent"},
}

# === LOGIN ===
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "role" not in st.session_state:
    st.session_state.role = ""

if not st.session_state.authenticated:
    st.title("🔐 Autentificare")
    username = st.text_input("Utilizator")
    password = st.text_input("Parolă", type="password")
    if st.button("Login"):
        if username in users and users[username]["password"] == password:
            st.session_state.authenticated = True
            st.session_state.role = users[username]["role"]
            st.success(f"Autentificat ca {username} ({st.session_state.role})")
            st.rerun()
        else:
            st.error("Utilizator sau parolă greșită")
    st.stop()

# === Mesaj roluri ===
if st.session_state.role == "admin":
    st.warning("🛠️ Ai acces complet la sistem.")
elif st.session_state.role == "medic":
    st.info("👨‍⚕️ Acces medic – date pacienți și alerte.")

# === Sidebar ===
st.sidebar.markdown(f"👤 Utilizator: **{st.session_state.role}**")
if st.sidebar.button("🚪 Delogare"):
    st.session_state.authenticated = False
    st.session_state.role = ""
    st.rerun()

if st.button("🔄 Refresh date"):
    st.rerun()

# === Resetare alerte ===
if st.sidebar.button("🧹 Șterge toate alertele"):
    if st.session_state.role != "admin":
        st.error("❌ Doar administratorul poate șterge alertele.")
    else:
        if os.path.exists("alerts.csv"):
            os.remove("alerts.csv")
            st.success("Alertele au fost șterse.")
            st.rerun()

# === Încărcare date ===
if os.path.exists("vitals_data.csv") and os.path.exists("patients.csv"):
    df = pd.read_csv("vitals_data.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    patients_info = pd.read_csv("patients.csv")

    # Combinație id + nume
    patient_options = [
        f"{row['id']} - {row['name']}"
        for _, row in patients_info.iterrows()
    ]
    selected_patient = st.selectbox("Selectează pacient:", patient_options)
    pacient_id = int(selected_patient.split(" - ")[0])
    pacient_nume = selected_patient.split(" - ")[1]

    pacient_df = df[df["patient_id"] == pacient_id]

    st.subheader(f"📊 Date vitale pentru {pacient_nume} (ID {pacient_id})")
    st.dataframe(pacient_df.tail(10), use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.line_chart(pacient_df.set_index("timestamp")[["heart_rate"]])
        st.caption("Puls")
        st.line_chart(pacient_df.set_index("timestamp")[["spo2"]])
        st.caption("SpO2")
    with col2:
        st.line_chart(pacient_df.set_index("timestamp")[["bp_sys"]])
        st.caption("Tensiune sistolică")
        st.line_chart(pacient_df.set_index("timestamp")[["bp_dia"]])
        st.caption("Tensiune diastolică")

    # Export CSV
    st.download_button(
        label="⬇️ Exportă datele pacientului (CSV)",
        data=pacient_df.to_csv(index=False).encode("utf-8"),
        file_name=f"{pacient_nume}_vitals.csv",
        mime="text/csv"
    )

    # === Export PDF ===
    def generate_pdf(df, patient_id, patient_name):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Raport pacient {patient_name} (ID {patient_id})", ln=True, align="C")
        pdf.ln(10)
        pdf.set_font("Arial", "B", size=10)
        headers = ["timestamp", "heart_rate", "spo2", "bp_sys", "bp_dia"]
        for col in headers:
            pdf.cell(38, 8, col, border=1)
        pdf.ln()
        pdf.set_font("Arial", size=10)
        for _, row in df.iterrows():
            for col in headers:
                pdf.cell(38, 8, str(row[col]), border=1)
            pdf.ln()
        return pdf.output(dest="S").encode("latin1")

    pdf_data = generate_pdf(pacient_df.tail(20), pacient_id, pacient_nume)
    st.download_button(
        label="⬇️ Exportă PDF cu datele pacientului",
        data=pdf_data,
        file_name=f"{pacient_nume}_raport.pdf",
        mime="application/pdf"
    )

    st.markdown("---")
    st.subheader("📋 Date recente pentru toți pacienții")
    st.dataframe(df.tail(10), use_container_width=True)

# === Alerte ===
if os.path.exists("alerts.csv"):
    alerts_df = pd.read_csv("alerts.csv")
    if "patient_id" in alerts_df.columns:
        pacient_alerts = alerts_df[alerts_df["patient_id"] == pacient_id]
        st.subheader(f"🚨 Alerte pentru {pacient_nume}")
        st.dataframe(pacient_alerts.tail(10), use_container_width=True)
    else:
        st.warning("alerts.csv nu are coloana 'patient_id'")
else:
    st.info("Nu există alerte salvate.")
