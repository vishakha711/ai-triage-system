def estimate_wait(queue_size, avg_time, priority):
    # Base factors for queue calculation
    factor = {"HIGH": 0.2, "MEDIUM": 0.8, "LOW": 1.5}
    
    # Base calculation
    base_wait = queue_size * avg_time * factor.get(priority, 1.0)

    if priority == "HIGH":
        # Emergency: Max 15-20 mins
        return round(min(base_wait, 15))
    
    elif priority == "MEDIUM":
        # Urgent but stable: Max 45-60 mins
        return round(min(base_wait, 60))
    
    elif priority == "LOW":
        # Non-urgent: Max 120 mins (2 hours)
        return round(min(base_wait, 120))
    
    return round(base_wait)