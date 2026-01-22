# 🩺 Diabetes Risk Prediction System using Machine Learning

This project is an AI-based health screening system that predicts whether a person is diabetic and estimates the future risk level using machine learning models. It also provides a user-friendly web interface built with Streamlit and stores patient records in a database.

---

## 🎯 Project Objectives

- Predict current diabetes status (Diabetic / Non-Diabetic)
- Estimate future diabetes risk probability
- Categorize risk as Low, Moderate, or High
- Provide interactive web-based interface
- Store patient history in database for analysis

---

## 📊 Dataset

- Based on PIMA Indians Diabetes Dataset (extended with lifestyle features)
- Features include:
  - Pregnancies
  - Glucose Level
  - Blood Pressure
  - Skin Thickness
  - Insulin
  - BMI
  - Diabetes Pedigree Function
  - Age
  - Gender
  - Physical Activity
  - Smoking
  - Family History
  - BMI Category (engineered)
  - Age Group (engineered)

---

## ⚙️ Feature Engineering

Additional features were created:

- **BMI Category**
  - Underweight
  - Normal
  - Overweight
  - Obese

- **Age Group**
  - ≤30
  - 31–45
  - 46–60
  - >60

- Lifestyle parameters were encoded numerically:
  - Physical Activity
  - Smoking Status
  - Family History
  - Gender

---

## 🤖 Machine Learning Models Used

- Logistic Regression
- Random Forest Classifier
- XGBoost Classifier

### Evaluation Metrics:
- Accuracy
- ROC-AUC Score

Best performing model was selected and saved using Joblib.

---

## 📈 Risk Classification Logic

Based on predicted probability:

| Probability | Risk Level |
|--------|------------|
| < 30%  | Low Risk |
| 30–60% | Moderate Risk |
| > 60%  | High Risk |

This probability is treated as approximate future diabetes risk.

---

## 🌐 Web Application

Built using **Streamlit** with:

- Interactive form inputs
- Risk gauge display
- Colored risk labels
- Database record storage
- Patient history table view

---

## 🗄️ Database

- SQLite database (`patients.db`)
- Stores:
  - Gender
  - Age
  - BMI
  - Glucose
  - Risk Probability
  - Risk Category

---

## 🚀 Deployment

Deployed on **Streamlit Cloud**

Steps:
1. Project pushed to GitHub
2. requirements.txt added
3. App deployed via Streamlit Cloud

Public app link available after deployment.

---

## 🛠️ Technologies Used

- Python
- Pandas, NumPy
- Scikit-learn
- Joblib
- SQLite
- Streamlit
- Plotly (for visualization)

---

## 📌 How to Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
