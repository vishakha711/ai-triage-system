from fastapi import FastAPI
from ml.translator import translate_to_english
from ml.encoder import encode_symptoms
from ml.fusion import fuse_features
from ml.predictor import predict
from ml.queue_model import estimate_wait
from ml.vitals_simulator import simulate_vitals
from ml.emergency import calculate_emergency_score
from api.database import add_patient, get_queue_size, get_all_patients, remove_patient
from fastapi import UploadFile, File
from api.voice import speech_to_text, extract_details

app=FastAPI()

@app.post("/triage")
def triage(patient:dict):

    text_en=translate_to_english(patient["symptom_text"])

    vitals=simulate_vitals()

    score = calculate_emergency_score(
        vitals["heart_rate"],
        vitals["spo2"],
        vitals["temperature"]
    )

    patient_data={
        "age":patient["age"],
        "heart_rate":vitals["heart_rate"],
        "spo2":vitals["spo2"],
        "temperature":vitals["temperature"],
        "waiting_time":8,
        "emergency_score":score
    }

    embedding=encode_symptoms(text_en)
    features=fuse_features(embedding,patient_data)

    priority,confidence=predict(features)
    queue_size = get_queue_size()
    wait_time = estimate_wait(queue_size, 8, priority)

    add_patient(
        patient["name"],
        patient["age"],
        patient["symptom_text"],
        priority,
        confidence,
        wait_time,
        vitals["heart_rate"],
        vitals["spo2"],
        vitals["temperature"]
)

    return{
        "name": patient["name"],
        "priority":priority,
        "confidence":confidence,
        "estimated_wait_time":wait_time,
    }

@app.post("/triage-voice")
async def triage_voice(file: UploadFile = File(...)):

    # Save audio file
    with open("temp.wav", "wb") as f:
        f.write(await file.read())

    # Convert voice → text
    text = speech_to_text("temp.wav")

    # Extract age + symptoms
    name, age, symptoms = extract_details(text)

    text_en = translate_to_english(symptoms)

    vitals = simulate_vitals()

    score = calculate_emergency_score(
        vitals["heart_rate"],
        vitals["spo2"],
        vitals["temperature"]
    )
    
    patient_data = {
        "age": age,
        "heart_rate": vitals["heart_rate"],
        "spo2": vitals["spo2"],
        "temperature": vitals["temperature"],
        "waiting_time": 8,
        "emergency_score": score
    }

    embedding = encode_symptoms(text_en)
    features = fuse_features(embedding, patient_data)

    priority, confidence = predict(features)
    queue_size = get_queue_size()

    wait_time = estimate_wait(queue_size, 8, priority)
    add_patient(
        name,   
        age,
        text,   # recognized voice text
        priority,
        confidence,
        wait_time,
        vitals["heart_rate"],
        vitals["spo2"],
        vitals["temperature"]
)
   
    return {
        "recognized_text": text,
        "name": name,
        "priority": priority,
        "confidence": confidence,
        "estimated_wait_time": wait_time
    }

@app.get("/get-patients")
def get_patients():

    patients = get_all_patients()

    result = []

    for p in patients:
        result.append({
        "id": p[0],
        "name": p[1],
        "age": p[2],
        "symptoms": p[3],
        "priority": p[4],
        "confidence": p[5],
        "wait_time": p[6],
        "heart_rate": p[7],
        "spo2": p[8],
        "temperature": p[9]
    })
    return result

@app.delete("/remove-patient/{patient_id}")
def delete_patient(patient_id: int):
    remove_patient(patient_id)

    return {"message": "Patient removed from queue"}