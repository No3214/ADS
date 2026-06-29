import random

def generate_ad_variant(platform: str, campaign_name: str) -> dict:
    """
    Generates a new ad creative variant (Headline + Description) based on the context.
    In a fully integrated environment, this would call an LLM (Claude/Gemini/GPT).
    For now, it uses high-converting template heuristics for Kozbeyli Konağı.
    """
    
    # High-converting semantic elements for Kozbeyli Konağı
    headlines_search = [
        "Tarihi Kozbeyli Konağı'nda Eşsiz Konaklama",
        "Foça'nın Kalbinde Butik Taş Otel",
        "Kozbeyli Konağı: 600 Yıllık Tarih Sizi Bekliyor",
        "Doğayla İç İçe Huzurlu Ege Tatili",
        "Foça Kozbeyli Konağı - Özel Teklifler"
    ]
    
    headlines_meta = [
        "Şehrin Gürültüsünden Uzaklaşın 🌿",
        "600 Yıllık Tarihi Konakta Uyanmak İster Misiniz?",
        "Ege'nin Gizli Cenneti: Kozbeyli Konağı",
        "Foça'da Unutulmaz Bir Hafta Sonu Kaçamağı"
    ]
    
    descriptions = [
        "Doğa manzaralı odalarımız, yöresel Ege kahvaltımız ve tarihi atmosferimizle hizmetinizdeyiz. Hemen rezervasyon yapın.",
        "Geleneksel taş mimari ve modern konfor bir arada. Sınırlı sayıdaki odalarımız için avantajlı fiyatları kaçırmayın.",
        "Şehrin stresini geride bırakın. Foça'nın eşsiz doğasında, 600 yıllık Kozbeyli Konağı'nda huzuru keşfedin.",
        "Özel Ege kahvaltısı, ferah taş odalar ve doğa yürüyüşü rotaları. Ailenizle veya baş başa romantik bir tatil."
    ]

    # Select templates based on platform context
    is_meta = platform.lower() == 'meta'
    hl_pool = headlines_meta if is_meta else headlines_search

    new_headline = random.choice(hl_pool)
    new_desc = random.choice(descriptions)

    return {
        "headline": new_headline,
        "description": new_desc,
        "rationale": f"Generated new variant focusing on 'Tarihi Konak' and 'Ege Kahvaltısı' angles to combat ad fatigue in {platform.capitalize()}."
    }
