import streamlit as st
import numpy as np
import joblib
import sqlite3
import pandas as pd

# ================= DATABASE =================
conn = sqlite3.connect(
    "C:\\Users\\hp\\Desktop\\Diabetes_ML_Project\\app\\patients.db",
    check_same_thread=False
)
c = conn.cursor()

# NEW TABLE WITH GENDER
c.execute("""
CREATE TABLE IF NOT EXISTS records(
    gender TEXT,
    age INT,
    bmi REAL,
    glucose INT,
    risk REAL,
    category TEXT
)
""")
conn.commit()

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Diabetes Risk Predictor", page_icon="🩺", layout="wide")

# ================= BACKGROUND IMAGE + OVERLAY =================
st.markdown("""
<style>
.stApp {
    background-image: 
        linear-gradient(rgba(0, 60, 120, 0.65), rgba(0, 60, 120, 0.65)),
        url("https://images.unsplash.com/photo-1588776814546-1ffcf47267a5?auto=format&fit=crop&w=1600&q=80");
    background-size: cover;
    background-attachment: fixed;
}

.card {
    background: rgba(255,255,255,0.25);
    backdrop-filter: blur(12px);
    border-radius: 15px;
    padding: 25px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}

.title {
    text-align:center;
    color:white;
    font-size:42px;
    font-weight:800;
}

.subtitle {
    text-align:center;
    color:#f1f1f1;
}

.badge-low {color:#2ecc71; font-weight:bold;}
.badge-mid {color:#f1c40f; font-weight:bold;}
.badge-high {color:#e74c3c; font-weight:bold;}
</style>
""", unsafe_allow_html=True)

# ================= LOAD MODEL =================
model = joblib.load("C:\\Users\\hp\\Desktop\\Diabetes_ML_Project\\models\\diabetes_model.pkl")
scaler = joblib.load("C:\\Users\\hp\\Desktop\\Diabetes_ML_Project\\models\\scaler.pkl")

# ================= HEADER =================
st.markdown("<div class='title'>🩺 Diabetes Risk Prediction Dashboard</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>AI-powered early health screening system</div>", unsafe_allow_html=True)
st.markdown("---")

left, right = st.columns(2)

# ================= INPUT PANEL =================
with left:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📋 Patient Inputs")

    gender = st.selectbox("Gender", ["Male","Female"])
    activity = st.selectbox("Physical Activity", ["Low","Moderate","High"])
    smoking = st.selectbox("Smoking", ["No","Yes"])
    family = st.selectbox("Family History", ["No","Yes"])

    age = st.number_input("Age", 1, 120, 30)
    preg = st.number_input("Pregnancies", 0, 20, 0)

    glucose = st.number_input("Glucose Level", 0, 300, 100)
    bp = st.number_input("Blood Pressure", 0, 200, 70)
    skin = st.number_input("Skin Thickness", 0, 100, 20)
    insulin = st.number_input("Insulin Level", 0, 900, 80)
    bmi = st.number_input("BMI", 0.0, 60.0, 25.0)

    dpf = st.number_input("Diabetes Pedigree Function", 0.0, 3.0, 0.5)

    predict_btn = st.button("🔍 Predict Diabetes Risk")

    st.markdown("</div>", unsafe_allow_html=True)

# ================= RESULT PANEL =================
with right:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📊 Prediction Output")

    if predict_btn:

        # -------- Feature Engineering --------
        age_group = 0 if age<=30 else 1 if age<=45 else 2 if age<=60 else 3
        bmi_cat = 0 if bmi<18.5 else 1 if bmi<25 else 2 if bmi<30 else 3

        activity_map = {"Low":0,"Moderate":1,"High":2}
        smoking_map = {"No":0,"Yes":1}
        family_map = {"No":0,"Yes":1}
        gender_map = {"Male":0,"Female":1}

        data = np.array([[preg, glucose, bp, skin, insulin, bmi, dpf, age,
                          gender_map[gender],
                          activity_map[activity],
                          smoking_map[smoking],
                          family_map[family],
                          bmi_cat,
                          age_group]])

        data_scaled = scaler.transform(data)

        pred = model.predict(data_scaled)[0]
        prob = model.predict_proba(data_scaled)[0][1]

        if prob < 0.3:
            risk = "Low Risk"
            badge = "badge-low"
        elif prob < 0.6:
            risk = "Moderate Risk"
            badge = "badge-mid"
        else:
            risk = "High Risk"
            badge = "badge-high"

        # SAVE TO DATABASE (6 COLUMNS → 6 VALUES)
        c.execute("INSERT INTO records VALUES (?,?,?,?,?,?)",
                  (gender, age, bmi, glucose, prob, risk))
        conn.commit()

        st.metric("Diabetes Status", "Diabetic" if pred==1 else "Non-Diabetic")
        st.metric("Risk Probability", f"{prob*100:.2f}%")
        st.markdown(f"### Risk Level: <span class='{badge}'>{risk}</span>", unsafe_allow_html=True)
        st.success("✔ Record saved successfully")

    else:
        st.info("Enter details and click Predict")

    st.markdown("</div>", unsafe_allow_html=True)

# ================= DATABASE TABLE =================
st.markdown("---")
if st.checkbox("📂 View Saved Patient Records"):
    rows = c.execute("SELECT * FROM records").fetchall()
    df = pd.DataFrame(rows, columns=["Gender","Age","BMI","Glucose","Risk","Category"])
    st.dataframe(df, use_container_width=True)

# ================= FOOTER =================
st.markdown("---")
st.markdown("<center style='color:white;'>Developed by GOUTHAMI</center>", unsafe_allow_html=True)
