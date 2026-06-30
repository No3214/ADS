import math

def calculate_saturation_point(spend: float, revenue: float) -> dict:
    """
    McKinsey/God Tier: Calculates the diminishing returns (saturation point).
    Uses the industry-standard Hill Function (Response = Beta * S^Alpha / (Gamma^Alpha + S^Alpha))
    to calculate marginal ROI (mROI) and determine scalability.
    
    Returns a dict with 'status' (saturated or scalable) and 'suggested_cap'
    """
    if spend <= 0:
        return {"status": "scalable", "suggested_cap": 500.0, "roas_decay_rate": 0.0}
        
    roas = revenue / spend
    
    # --- HILL FUNCTION ASSUMPTIONS ---
    # Alpha (Shape parameter): 1.5 (S-shaped curve typical for ad spend)
    # Gamma (Inflection point): 300 TL (Assuming standard daily saturation starts scaling down here)
    alpha = 1.5
    gamma = 300.0
    
    # Since we only have one data point (spend, revenue), we solve for Beta (Scale parameter):
    # Beta = Revenue * (Gamma^Alpha + Spend^Alpha) / Spend^Alpha
    s_alpha = math.pow(spend, alpha)
    g_alpha = math.pow(gamma, alpha)
    
    if s_alpha > 0:
        beta = revenue * (g_alpha + s_alpha) / s_alpha
    else:
        beta = 0.0

    # Calculate Marginal ROI (Derivative of Hill Function with respect to Spend)
    # mROI = (Beta * Alpha * Gamma^Alpha * Spend^(Alpha - 1)) / (Gamma^Alpha + Spend^Alpha)^2
    if s_alpha > 0 and (g_alpha + s_alpha) > 0:
        mroi = (beta * alpha * g_alpha * math.pow(spend, alpha - 1)) / math.pow(g_alpha + s_alpha, 2)
    else:
        mroi = 0.0
        
    # Decay rate (inverse of mROI capability)
    decay_rate = 1.0 - mroi if mroi < 1.0 else 0.0
    
    if roas < 1.5:
        status = "underperforming"
        suggested_cap = max(spend * 0.9, 100.0) # Reduce
    elif mroi < 0.5:
        # If every extra 1 TL brings less than 0.5 TL, we are highly saturated
        status = "saturated"
        suggested_cap = spend
    elif roas >= 3.0 and mroi >= 1.2:
        # High ROAS and high marginal potential
        status = "scalable"
        suggested_cap = spend * 1.5
    elif roas >= 2.0 and mroi >= 0.8:
        # Moderate scaling
        status = "scalable"
        suggested_cap = spend * 1.2
    else:
        status = "stable"
        suggested_cap = spend
        
    return {
        "status": status,
        "suggested_cap": round(suggested_cap, 1),
        "roas_decay_rate": round(decay_rate, 4),
        "mroi": round(mroi, 4)
    }

