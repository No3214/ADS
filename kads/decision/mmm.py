import math

def calculate_saturation_point(spend: float, revenue: float) -> dict:
    """
    McKinsey/God Tier: Calculates the diminishing returns (saturation point).
    Uses a simplified logarithmic curve fitting to determine if scaling 
    budget will yield linear or diminishing returns.
    
    Returns a dict with 'status' (saturated or scalable) and 'suggested_cap'
    """
    if spend <= 0:
        return {"status": "scalable", "suggested_cap": 500.0, "roas_decay_rate": 0.0}
        
    roas = revenue / spend
    
    # Logarithmic saturation formula: R = a * ln(S + 1)
    # If a campaign is highly saturated, scaling it by 20% won't yield 20% more revenue.
    # We use ROAS as a proxy for 'a' factor.
    
    # Thresholds for Kozbeyli Konağı
    # Base daily spend expected around 200-500 TL.
    
    decay_rate = math.log1p(spend) / (spend ** 0.5) if spend > 0 else 0
    
    if roas < 1.5:
        status = "underperforming"
        suggested_cap = max(spend * 0.9, 100.0) # Reduce
    elif roas >= 3.0 and spend > 1500:
        # If it's already spending a lot, check saturation
        if decay_rate < 0.1: # Highly saturated
            status = "saturated"
            suggested_cap = spend
        else:
            status = "scalable"
            suggested_cap = spend * 1.2
    elif roas >= 3.0:
        status = "scalable"
        suggested_cap = spend * 1.5
    else:
        status = "stable"
        suggested_cap = spend
        
    return {
        "status": status,
        "suggested_cap": round(suggested_cap, 1),
        "roas_decay_rate": round(decay_rate, 4)
    }
