def calculate_emergency_score(hr, spo2, temp):
    score = 0
    if spo2 < 92: score += 0.4
    if hr > 110: score += 0.3
    if temp > 102: score += 0.3
    return min(score,1.0)