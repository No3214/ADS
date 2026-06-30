import math


def calculate_saturation_point(spend: float, revenue: float) -> dict:
    """Tek-nokta marjinal-getiri SEZGİSELİ (gerçek MMM DEĞİL).

    Dürüstlük notu: Elimizde tek (spend, revenue) noktası var; tek noktayla gerçek
    doygunluk eğrisi (Hill) tanımlanamaz — saturasyon zaman-serisi ister. Bu fonksiyon
    Hill formunu, kıvrım noktası (gamma) MEVCUT HARCAMAYA sabitlenmiş halde kullanır;
    böylece marjinal-ROI ölçekten BAĞIMSIZ (yalnız ROAS'a bağlı: mROI = 0.75 × ROAS).
    Karar (status) tamamen ROAS'a dayanır — mutlak harcama büyüklüğüne değil.
    Gerçek MMM için ≥8-12 haftalık seri toplanıp beta/gamma regresyonla fit edilmeli (yol haritası).

    Returns: {status, suggested_cap, roas_decay_rate, mroi}; status ∈ {underperforming, stable, scalable}
    """
    if spend <= 0:
        return {"status": "scalable", "suggested_cap": 500.0, "roas_decay_rate": 0.0, "mroi": 0.0}

    roas = revenue / spend

    # Gamma (kıvrım) = mevcut harcama → ölçek-değişmezlik. Alpha = 1.5 (reklam için tipik S-eğri).
    alpha = 1.5
    gamma = max(spend, 1.0)
    s_alpha = math.pow(spend, alpha)
    g_alpha = math.pow(gamma, alpha)
    beta = revenue * (g_alpha + s_alpha) / s_alpha if s_alpha > 0 else 0.0
    mroi = (beta * alpha * g_alpha * math.pow(spend, alpha - 1)) / math.pow(g_alpha + s_alpha, 2) if (g_alpha + s_alpha) > 0 else 0.0
    decay_rate = round(max(0.0, 1.0 - mroi), 4)

    # Karar ROAS'a dayanır (ölçek-değişmez). suggested_cap MEVCUT HARCAMAYA göreli + ROAS ile ölçeklenir.
    if roas < 1.5:
        status = "underperforming"
        suggested_cap = max(spend * 0.85, 100.0)
    elif roas >= 3.0:
        status = "scalable"
        mult = 1.3 + min((roas - 3.0) / 20.0, 0.7)  # yüksek ROAS daha cesur; tavan ~spend*2.0
        suggested_cap = spend * mult
    else:  # 1.5 <= roas < 3.0
        status = "stable"
        suggested_cap = spend

    return {
        "status": status,
        "suggested_cap": round(suggested_cap, 1),
        "roas_decay_rate": decay_rate,
        "mroi": round(mroi, 4),
    }
