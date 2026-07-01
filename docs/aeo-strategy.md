# Kozbeyli Konağı — AEO / GEO Stratejisi (AI Motoru Görünürlüğü)

> **Amaç:** ChatGPT / Claude / Perplexity / Gemini "Foça butik otel", "İzmir taş otel", "Foça'da köy
> kahvaltısı güzel otel" gibi sorulduğunda **Kozbeyli Konağı önerilsin / kaynak gösterilsin.**
> aymar.tech gibi servisler bunu aylık ~4.490 TL'ye satar; bu paket aynı işi **kendi altyapımızda, ücretsiz** yapar.
> CLI: `kads aeo` · Skill: `skills/aeo-mastery/SKILL.md` · Ölçüm: `aeo/alinti-testi.csv`.
> Araştırma tarihi: Tem 2026 (kaynaklar dosya sonunda).

---

## 0) DÜRÜST GERÇEK — otel AEO'su nasıl çalışır (2026 araştırması)
Bir 16-odalı butik otel için AI görünürlüğünün **kendi sitende bitmediğini** bilmek şart:

- **ChatGPT otel verisinin ~%94'ü Google üzerinden akar** (web sonuçları + Google Places/Maps). Yani Google İşletme Profili (GBP) AI görünürlüğünün de temelidir.
- **Atıfların çoğu ARACI kaynaklara gider:** OTA'lar (Booking, Expedia), TripAdvisor, editoryal gezi rehberleri — otelin kendi sitesine değil. AI, "güvenli öneri" için üçüncü-taraf doğrulama arar.
- **AI otel önerilerinin ~%71'i misafir yorumlarıyla sürüklenir.** Sıralamada **yorum HACMİ + yıldız sınıfı**, tek tek puandan daha etkili; sonra fiyat gelir.
- **RRF fusion:** AI, aynı oteli **birden çok kaynakta** (TripAdvisor + Booking + Google + editoryal liste) görünce ödüllendirir. Tek kaynak yetmez; **çoklu-kaynak tutarlılığı** kazandırır.
- **Wikidata** (Wikipedia'nın makine-okunur kardeşi) Google Knowledge Graph'ı besler → ChatGPT/Perplexity/Bing oradan okur. Küçük işletme için **Wikipedia'dan çok daha ulaşılabilir** ve en yüksek getirili entity kazanımı.
- **Tazelik:** AI atıflarının ~%83'ü son 12 ayda güncellenmiş sayfalardan. Bayat içerik alıntılanmaz.
- **Ton:** AI ansiklopedik/nesnel metni tercih eder. "Bence / en iyi / harika" gibi öznel dil alıntı şansını düşürür; **nesnel, doğrulanabilir cümleler** kazandırır.

**Kozbeyli için sonuç:** En yüksek getirili AEO kaldıraçları sırayla → (1) **yorum hacmi + hıza** (Google/TripAdvisor/Booking), (2) **çoklu-kaynak NAP tutarlılığı**, (3) **Wikidata entity**, (4) site tarafı (llms.txt + şema + FAQ), (5) editoryal/gezi-blogu atıfları. Site zaten güçlü (JSON-LD + FAQPage + llms.txt var) — asıl açık **off-site kanıt + yorum**.

---

## 1) PLATFORM BAZLI STRATEJİ (her biri farklı kaynak kullanır)

### ChatGPT (Search + gezi app'leri)
- **Kaynak:** Google/Places (~%94) + TripAdvisor ortaklığı + Bing. Yapılandırılmış veri + yorum yoğunluğu + editoryal atıf ağırlıklı.
- **Yap:** GBP eksiksiz + kategoriler doğru · TripAdvisor profili güncel + yorum hacmi · llms.txt (var) · FAQPage şeması (var) · Bing Webmaster + IndexNow (AEO ön koşulu — rakiplerin atladığı ucuz avantaj).
- **Test:** "Foça'da tarihi taş konak otel öner", "Kozbeyli Konağı nedir".

### Claude (web arama + eğitim verisi)
- **Kaynak:** Wikipedia/Wikidata ansiklopedik otorite ağırlıklı; nesnel, iyi-kaynaklı içerik. ClaudeBot/Claude-User robots.txt'te açık olmalı (✓ mevcut).
- **Yap:** **Wikidata entity** (en kritik) · llms.txt İngilizce özet (var) · nesnel, doğrulanabilir dil · tutarlı NAP.
- **Test:** "İzmir'de tarihi taş otel öner", "Foça köyünde butik konaklama".

### Perplexity (her zaman atıf gösterir)
- **Kaynak:** Otoriter kaynaklar + **Reddit** (Perplexity sourced içeriğinin ~%46.7'si) + özgün veri + taze sayfalar.
- **Yap:** Reddit gezi topluluklarında (r/turkey, r/travel, r/izmir) organik/dürüst varlık · özgün veri (ör. "600 yıllık köy, 16 oda, bakanlık belge no") · taze içerik · gezi-blogu atıfları.
- **Test:** "best boutique hotel near Foça Turkey", "Foça vs Alaçatı where to stay".

### Gemini / Google AI Overviews (harita + öneri)
- **Kaynak:** Google Knowledge Graph + Places + FAQ/HowTo şeması + Wikidata.
- **Yap:** **GBP optimizasyonu birinci öncelik** · FAQPage + HotelRoom şeması · Wikidata (Knowledge Graph besler) · GSC doğrulama + sitemap.
- **Test:** Google'da "Foça butik otel" AI Overview'da çıkıyor mu · "kozbeyli konağı" knowledge panel.

---

## 2) UYGULAMA PLANI — ne üretilecek, nereye girilecek

### A) Off-site kanıt (en yüksek getirili — burada kazanılır)
1. **Yorum hacmi + hızı** (Google → TripAdvisor → Booking): her misafirden yorum iste; TÜM yorumlara (olumlu+olumsuz) düşünceli yanıt ver. Hedef: ~4.2 → 4.5+ algısı + hacim artışı. (Bkz. `reputation/`, `profiles/`.)
2. **Çoklu-kaynak NAP tutarlılığı:** Google, TripAdvisor, Booking, Yandex, Foursquare, Apple Maps'te **birebir aynı** ad/adres/telefon (`profiles/ESITLEME-KONTROL.md`).
3. **Wikidata item** oluştur: "Kozbeyli Konağı" — instance of: boutique hotel; located in: Kozbeyli, Foça, İzmir; koordinat; resmi site; kuruluş; bakanlık belge no. Notability için kaynak göster (basın/gezi-blogu). → Google Knowledge Graph → Claude/ChatGPT/Perplexity okur.
4. **Editoryal/gezi-blogu atıfları:** "İzmir butik otel", "Foça gezi rehberi", "Ege köy konaklama" listelerine dahil ol (PR/outreach — `outreach/`). RRF fusion için çoklu-kaynak sinyali.

### B) On-site (zaten güçlü — tazele ve genişlet)
5. **llms.txt** (var, güncel) — sürekli tut, İngilizce özet koru.
6. **Şema genişletme:** Hotel + LodgingBusiness + Restaurant + FAQPage + BreadcrumbList (var) → **HotelRoom** (oda tipleri, fiyat, kapasite, manzara) + **Review/AggregateRating** (yorum yıldızı) ekle. `aeo/schema/`.
7. **FAQ/Q&A içerik:** AI'ın verbatim alabileceği net soru-cevap blokları (`aeo/soru-kumeleri.md`). Nesnel dil.
8. **Tazelik:** blog/sayfa güncellemeleri son 12 ayda; lastmod taze.

### C) Ölçüm (haftalık AI görünürlük)
9. `aeo/alinti-testi.csv` — 4 platformda sabit test sorguları, haftalık manuel test → skor.
10. `kads aeo score` — görünürlük skoru + rakip karşılaştırması.

---

## 3) BACKLINK / KAYNAK STRATEJİSİ (AI hangi kaynakları referans alır)
Öncelik sırası (Kozbeyli için ulaşılabilirlik × etki):
1. **Google Business Profile** (ChatGPT %94 buradan) — ücretsiz, birinci öncelik.
2. **TripAdvisor** — otel AEO'sunda ChatGPT ortağı + ağır referans; profil + yorum hacmi.
3. **Booking.com** — OTA atıfı + review sinyali (parite HotelRunner ile korunur).
4. **Wikidata** — Knowledge Graph → tüm AI motorları; ulaşılabilir entity kazanımı.
5. **Reddit** (r/turkey, r/travel, r/izmir) — Perplexity'nin ~%47'si; organik/dürüst, spam DEĞİL.
6. **Gezi blogları / editoryal listeler** — "İzmir butik otel", "Foça nerede kalınır" roundup'ları (outreach).
7. **Yandex/Bing Webmaster + IndexNow** — AEO ön koşulu, rakiplerin atladığı.

> **Etik sınır:** sahte yorum/spam YOK. Yalnızca gerçek misafir yorumu teşviki + dürüst topluluk katılımı + doğru NAP. AI motorları manipülasyonu cezalandırır; tutarlı gerçek sinyal kazandırır.

---

## 4) HAFTALIK AI GÖRÜNÜRLÜK ÖLÇÜMÜ
Her hafta aynı gün, 4 platformda `aeo/alinti-testi.csv`'deki sorguları çalıştır:
- **Skorlama:** her sorgu × platform → 2 (önerildi/kaynak), 1 (bahsedildi ama öne çıkmadı), 0 (yok).
- **Görünürlük skoru** = toplam / (sorgu × platform × 2) × 100.
- **Share of Voice:** Kozbeyli vs rakipler (Bülbül Yuvası, Huri Nuri, Foça Ensar) kaç sorguda çıkıyor.
- Trend: skoru zaman serisinde izle; içerik/yorum/Wikidata sonrası artışı gör.
- `kads aeo score` bu tabloyu okur ve özet + öneri üretir.

---

## 5) 90 GÜNLÜK AEO YOL HARİTASI
| Dönem | İş | Beklenen |
|---|---|---|
| Hafta 1–2 | GBP eksiksiz + kategoriler · Bing/IndexNow · Wikidata item · yorum-isteme rutini başlat | Temel + taban ölçüm |
| Hafta 3–4 | TripAdvisor/Booking profil + yorum hacmi · HotelRoom+Review şema · FAQ genişlet | Çoklu-kaynak sinyali |
| Ay 2 | Editoryal/gezi-blogu outreach (3–5 liste) · Reddit organik varlık · haftalık ölçüm | İlk atıflar (30 günde mümkün) |
| Ay 3 | İçerik tazeleme · yorum hacmi ivme · skor + SoV izleme · zayıf sorgulara içerik | Bileşik görünürlük artışı |

**Formül:** Yorum (hacim+hız) → Çoklu-kaynak NAP → Wikidata entity → Site şema/llms.txt → Editoryal atıf → Haftalık ölçüm.

---

## Kaynaklar (Tem 2026 araştırması)
- Frase — Answer Engine Optimization Complete Guide 2026
- Jasper — GEO vs AEO vs SEO Guide 2026
- Bored Hotelier — Get Your Hotel Recommended by ChatGPT
- HotelRank.ai — Anatomy of ChatGPT Hotel Search 2026 (%94 Google, RRF fusion)
- RevPARGenius — 94% of Hotels Invisible in AI Search 2026
- TrustYou (via Prostay/Mews) — %71 yorum-sürüklü öneri
- SEO Strategy Ltd / Over The Top SEO — Wikidata for SEO & Knowledge Graph
- Authoritas / Profound — AI visibility tracker modeli (sorgu → yanıt+atıf → SoV)
