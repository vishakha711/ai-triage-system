import random
import pandas as pd

critical_symptoms = [
    "severe chest pain with sweating",
    "unconscious after collapse",
    "severe breathing difficulty",
    "major trauma from accident",
    "seizure activity ongoing"
]

urgent_symptoms = [
    "moderate chest pain",
    "high fever with weakness",
    "shortness of breath",
    "persistent vomiting"
]

moderate_symptoms = [
    "fever and cough",
    "headache with nausea",
    "minor fracture pain"
]

mild_symptoms = [
    "mild fever",
    "sore throat",
    "body ache"
]

very_mild_symptoms = [
    "routine checkup request",
    "prescription refill",
    "mild allergy rash"
]

def emergency_score(hr, spo2, temp):
    score = 0
    if spo2 < 92: score += 0.4
    if hr > 110: score += 0.3
    if temp > 102: score += 0.3
    return min(score,1.0)

def generate_patient(pid):

    esi = random.randint(1,5)

    if esi == 1:
        symptom=random.choice(critical_symptoms)
        hr=random.randint(120,150)
        spo2=random.randint(80,90)
        temp=round(random.uniform(101,105),1)

    elif esi == 2:
        symptom=random.choice(urgent_symptoms)
        hr=random.randint(105,130)
        spo2=random.randint(88,95)
        temp=round(random.uniform(100,103),1)

    elif esi == 3:
        symptom=random.choice(moderate_symptoms)
        hr=random.randint(85,110)
        spo2=random.randint(92,98)
        temp=round(random.uniform(99,102),1)

    elif esi == 4:
        symptom=random.choice(mild_symptoms)
        hr=random.randint(70,95)
        spo2=random.randint(95,100)
        temp=round(random.uniform(98,100),1)

    else:
        symptom=random.choice(very_mild_symptoms)
        hr=random.randint(60,85)
        spo2=random.randint(97,100)
        temp=round(random.uniform(98,99.5),1)

    age=random.randint(1,90)
    waiting_time=random.randint(1,40)

    if esi<=2:
        priority="HIGH"
    elif esi==3:
        priority="MEDIUM"
    else:
        priority="LOW"

    return [
        symptom,age,hr,spo2,temp,waiting_time,
        emergency_score(hr,spo2,temp),
        priority
    ]

data=[generate_patient(i) for i in range(1500)]

df=pd.DataFrame(data,columns=[
"symptom_text","age","heart_rate","spo2",
"temperature","waiting_time",
"emergency_score","priority_label"
])

df.to_csv("er_patient_dataset.csv",index=False)
print("Dataset created!")