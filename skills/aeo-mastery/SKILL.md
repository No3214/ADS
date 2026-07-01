---
name: aeo-mastery
description: >-
  Kozbeyli Konağı'nı AI motorlarında (ChatGPT, Claude, Perplexity, Gemini) önerilen/kaynak
  gösterilen hâle getirir — AEO/GEO görünürlük artırma. Kullan: "AI görünürlük", "ChatGPT'de
  çıkalım", "Perplexity kaynak", "Gemini öneri", "AEO", "GEO", "answer engine optimization",
  "AI'da önerilen ol", "Wikidata", "llms.txt", "citation", "AI visibility skor", "rakip AI
  karşılaştırma" veya AI arama görünürlüğü işleri geçtiğinde. Kaynak: docs/aeo-strategy.md ·
  CLI: kads aeo (queries/score/schema) · Ölçüm: aeo/alinti-testi.csv.
---

# Kozbeyli Konağı — AEO/GEO Ustalığı (AI Motoru Görünürlüğü)

aymar.tech gibi servislerin ~4.490 TL/ay'a sattığı işi **kendi altyapımızda** yapar.
Tam strateji: `docs/aeo-strategy.md`. Durum/ölçüm: `kads aeo score`.

## 0) DÜRÜST GERÇEK — bu bir OLASILIK oyunu, garanti yok
Bir 16-odalı butik otel için AI görünürlüğü **kendi sitende bitmez**:
- ChatGPT otel verisinin **~%94'ü Google/Places** üzerinden akar → **GBP birinci öncelik.**
- Atıfların çoğu **aracı kaynaklara** gider (TripAdvisor, Booking, editoryal) — kendi siteye değil.
- AI otel önerilerinin **~%71'i misafir yorumlarıyla** sürüklenir; **yorum HACMİ + yıldız > tek puan.**
- **RRF fusion:** aynı otel birden çok kaynakta görününce ödüllenir → **çoklu-kaynak tutarlılığı.**
- **Wikidata** Knowledge Graph'ı besler → tüm AI motorları okur; küçük işletme için **ulaşılabilir #1 entity kazanımı.**
- Tazelik: atıfların ~%83'ü son 12 ayda güncel sayfalardan. Nesnel/ansiklopedik ton kazandırır.

En yüksek getirili sıra: **yorum (hacim+hız) → çoklu-kaynak NAP → Wikidata → site şema/llms.txt → editoryal atıf → haftalık ölçüm.**

## 1) PLATFORM BAZLI STRATEJİ (her biri farklı kaynak)
- **ChatGPT** → Google/Places + TripAdvisor + Bing. Yap: GBP eksiksiz, TripAdvisor yorum hacmi, llms.txt, FAQPage şema, Bing/IndexNow.
- **Claude** → Wikipedia/**Wikidata** + nesnel içerik. Yap: **Wikidata entity** (kritik), llms.txt EN özet, doğrulanabilir dil, tutarlı NAP. (ClaudeBot robots'ta açık ✓)
- **Perplexity** → otoriter kaynak + **Reddit (~%47)** + özgün veri + taze. Yap: r/turkey·r/travel·r/izmir'de dürüst varlık, özgün veri, gezi-blogu atıf.
- **Gemini / AI Overviews** → Knowledge Graph + Places + FAQ/HowTo şema. Yap: **GBP** + FAQPage + HotelRoom şema + Wikidata + GSC.

## 2) UYGULAMA (ne üret, nereye gir)
Off-site (burada kazanılır): yorum hacmi+hızı (Google→TripAdvisor→Booking) · çoklu-kaynak NAP tutarlılığı (`profiles/`) · **Wikidata item** (ad, tür, konum, koordinat, resmî site, belge no + kaynak) · editoryal/gezi-blogu atıf (`outreach/`).
On-site (zaten güçlü, tazele): llms.txt (var) · şema genişlet → **HotelRoom + Review/AggregateRating** (`aeo/schema/`) · FAQ/Q&A nesnel bloklar (`aeo/soru-kumeleri.md`).

## 3) BACKLINK / KAYNAK ÖNCELİĞİ (AI neyi referans alır)
GBP → TripAdvisor → Booking → **Wikidata** → Reddit (organik) → gezi-blogu/editoryal → Yandex/Bing+IndexNow.
**Etik sınır:** sahte yorum/spam YOK; sadece gerçek misafir yorumu teşviki + dürüst topluluk katılımı + doğru NAP.

## 4) ÖLÇÜM VE İZLEME (haftalık)
1. `kads aeo queries` → 20 test sorgusunu gör (TR + EN, 6 kategori).
2. Haftada 1 aynı gün, `aeo/alinti-testi.csv`'yi 4 platformda test et: **2**=önerildi/kaynak · **1**=bahsedildi · **0**=yok.
3. `kads aeo score` → genel görünürlük % + platform bazlı + ölçülen hücre. Boş hücre paydaya girmez (dürüst kısmi skor).
4. **Rakip Share-of-Voice:** aynı sorguları Bülbül Yuvası / Huri Nuri / Foça Ensar için de test et → kim daha çok çıkıyor karşılaştır.
5. Skoru zaman serisinde izle; Wikidata/yorum/içerik sonrası artışı gör.

## 5) AYLIK OPTİMİZASYON RUTİNİ
- **Hafta 1:** GBP + Bing/IndexNow + Wikidata item + yorum-isteme rutini. Taban skoru al (`kads aeo score`).
- **Hafta 2:** TripAdvisor/Booking yorum hacmi + HotelRoom/Review şema + FAQ genişlet.
- **Hafta 3:** editoryal/gezi-blogu outreach (3–5 liste) + Reddit organik varlık.
- **Hafta 4:** içerik tazele + skor + SoV karşılaştır → en zayıf sorgulara içerik üret. Tekrarla.

## Güvenlik (repo kuralları)
- Sahte yorum/spam/manipülasyon YOK (AI cezalandırır, gerçek sinyal kazandırır).
- Doğrulanmamış iddia ("13 km", ödül, "en iyi") kullanma → **"Yeni Foça'ya yakın"**, nesnel dil.
- `.com.tr` gündem yapma; tek odak `www.kozbeylikonagi.com`. Token/secret sohbete/GitHub'a yazma.

## Hızlı komutlar
`kads aeo` (soru kümeleri) · `kads aeo queries` (test sorguları) · `kads aeo score` (görünürlük skoru) · `kads aeo schema` (JSON-LD listesi).
Referanslar: `docs/aeo-strategy.md` · `aeo/` (llms.txt, robots.txt, schema/, soru-kumeleri.md, olcum.md) · `kads tracking` (ölçüm ön koşulu).
