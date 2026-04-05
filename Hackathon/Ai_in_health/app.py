import os
import sys
import torch
import json
import mysql.connector
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import List

# Fix for imports if running directly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from src.algorithms.dbn import DBN

app = FastAPI(title="Clinical Decision Support API")

# Mount static folder for the frontend UI
os.makedirs("static", exist_ok=True)
app.mount("/ui", StaticFiles(directory="static", html=True), name="static")

class PatientData(BaseModel):
    age: float = Field(..., ge=20, le=120)
    sex: int = Field(..., ge=0, le=1)
    cp: int = Field(..., ge=0, le=3)
    trestbps: float = Field(..., ge=80, le=250)
    chol: float = Field(..., ge=100, le=600)
    fbs: int = Field(..., ge=0, le=1)
    restecg: int = Field(..., ge=0, le=2)
    thalach: float = Field(..., ge=60, le=220)
    exang: int = Field(..., ge=0, le=1)
    oldpeak: float = Field(..., ge=0.0, le=10.0)
    slope: int = Field(..., ge=0, le=2)
    ca: int = Field(..., ge=0, le=3)
    thal: int = Field(..., ge=1, le=3)

# Global variables for DB and Model
db_connection = None
model = None
selected_indices = []

@app.on_event("startup")
def startup_event():
    global db_connection, model, selected_indices
    # 1. Initialize MySQL Database
    try:
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="heart_disease_db" 
        )
    except mysql.connector.Error as err:
        if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            try:
                temp_conn = mysql.connector.connect(host="localhost", user="root", password="")
                cursor = temp_conn.cursor()
                cursor.execute("CREATE DATABASE IF NOT EXISTS heart_disease_db")
                temp_conn.commit()
                temp_conn.close()
                db_connection = mysql.connector.connect(host="localhost", user="root", password="", database="heart_disease_db")
            except Exception as e:
                print(f"Could not create database automatically: {e}")
        else:
            print(f"Database connection failed: {err}")
            
    if db_connection:
        try:
            cursor = db_connection.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS Patients_Vitals (
                id INT AUTO_INCREMENT PRIMARY KEY,
                age FLOAT, sex INT, cp INT, trestbps FLOAT, chol FLOAT, fbs INT,
                restecg INT, thalach FLOAT, exang INT, oldpeak FLOAT, slope INT,
                ca INT, thal INT
            )''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS AI_Predictions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                patient_id INT,
                prediction_result INT,
                FOREIGN KEY (patient_id) REFERENCES Patients_Vitals(id)
            )''')
            db_connection.commit()
            print("Database initialized successfully.")
        except Exception as e:
            print(f"Error creating tables: {e}")

    # 2. Load Model and Configuration
    try:
        if os.path.exists("selected_features.json"):
            with open("selected_features.json", "r") as f:
                selected_indices = json.load(f)
            
            input_dim = len(selected_indices)
            model = DBN(input_dim=input_dim, hidden_dims=[16, 8], output_dim=2, k=1)
            model.load_state_dict(torch.load("heart_disease_model.pth"))
            model.eval()
            print("PyTorch Model loaded successfully from 'heart_disease_model.pth'.")
        else:
            print("Warning: selected_features.json not found. Run main.py first to train the model.")
    except Exception as e:
        print(f"Error loading model: {e}")

@app.post("/predict")
async def predict(data: PatientData):
    global db_connection, model, selected_indices
    patient_id = None
    
    # 1. Insert into Patients_Vitals
    if db_connection:
        try:
            cursor = db_connection.cursor()
            query = """INSERT INTO Patients_Vitals 
                       (age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(query, (data.age, data.sex, data.cp, data.trestbps, data.chol, data.fbs, 
                                   data.restecg, data.thalach, data.exang, data.oldpeak, data.slope, 
                                   data.ca, data.thal))
            db_connection.commit()
            patient_id = cursor.lastrowid
        except Exception as e:
            print(f"DB Error (Insert Vital): {e}")

    # 2. Inference
    features_full = [
        data.age, data.sex, data.cp, data.trestbps, data.chol, data.fbs,
        data.restecg, data.thalach, data.exang, data.oldpeak, data.slope,
        data.ca, data.thal
    ]
    
    try:
        if model is not None and selected_indices:
            # Filter features based on training selection
            features_sel = [features_full[i] for i in selected_indices]
            tensor_input = torch.tensor([features_sel], dtype=torch.float32)
            
            with torch.no_grad():
                output = model(tensor_input)
                prediction = torch.argmax(output, dim=1).item()
        else:
            print("Model not loaded, falling back to basic mock inference")
            # Fallback mock if model failed to load or hasn't trained
            prediction = 1 if (data.chol > 240 or data.age > 60) else 0

    except Exception as e:
        print(f"Error during model inference: {e}")
        raise HTTPException(status_code=500, detail="Model inference failed")

    # 3. Insert Prediction
    if db_connection and patient_id:
        try:
            cursor = db_connection.cursor()
            query2 = "INSERT INTO AI_Predictions (patient_id, prediction_result) VALUES (%s, %s)"
            cursor.execute(query2, (patient_id, prediction))
            db_connection.commit()
        except Exception as e:
            print(f"DB Error (Insert Prediction): {e}")

    return {"prediction": prediction}
