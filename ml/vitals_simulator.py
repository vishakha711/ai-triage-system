import random

def simulate_vitals():

    return {
        "heart_rate":random.randint(90,130),
        "spo2":random.randint(85,98),
        "temperature":round(random.uniform(98,103),1)
    }