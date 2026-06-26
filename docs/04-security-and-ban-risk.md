# 04 — Güvenlik ve Ban Riski (Kesin Kurallar)

Tam otonom çalışmak, "kontrolsüz" çalışmak değildir. Aşağıdakiler para harcayan bir
production hesabında hesabın askıya alınmasını ve kontrolsüz harcamayı önler.

## Kimlik bilgisi (credential) hijyeni
- Access token, refresh token, App Secret, client secret veya OAuth dosya içeriğini
  **sohbete, GitHub'a veya URL'ye** ASLA yazmayın.
- Token'ı URL query parametresine koymayın (`?token=...`). Geçmiş, proxy ve log'larda
  sızar. (Bazı üçüncü taraf MCP README'leri bunu önerir; yapmayın.)
- Secret'lar yalnızca `.env` (git-ignored) ve OAuth/ADC dosyalarında durur.
- Gerçek dünya uyarısı: incelenen bazı topluluk Google MCP repolarından biri, README'sinde
  gerçek `client_secret` ve `refresh_token` sızdırmıştı. Bu, "secret'ı koda koyma"
  kuralının neden mutlak olduğunun canlı örneğidir.

## Neden prompt seviyesinde onay YETERSİZ
- "Önce onay al" yalnızca prompt'ta yazıyorsa, bir talimat enjeksiyonu (reklam metni,
  açılış sayfası, yorum vb. içine gömülü) bunu atlayabilir.
- Bu yüzden onay **kod seviyesinde** (`scripts/guardrails.py`) ve **connector izinleri**
  seviyesinde (Needs approval / Blocked) zorunlu kılınır. Üç katman: prompt + kod + izin.

## guardrails.py'nin garanti ettiği
- Yalnızca **allowlist**'teki hesap kimlikleri (Meta `act_...`, Google 10 hane).
- Tüm yeni kampanyalar **PAUSED**.
- Sabit **günlük + aylık bütçe tavanı** (Google 493/15.000, Meta 500/15.000 TL).
- Önce **validate_only / dry-run**; yoksa payload önizlemesi.
- Eski → yeni değer gösterimi.
- Mevcut oturumda **açık onay**; `ENABLED` için **ikinci ayrı onay**.
- **Delete, ödeme, kullanıcı yönetimi, müşteri listesi yükleme YOK.**
- Her işlem için **audit log** (tarih, hesap, eski/yeni değer, karar) → `logs/`.

## Google ban/askıya alma
- Google, yetkisiz hesap erişimi tespit ettiğinde hesabı geçici askıya alabilir; politika,
  ödeme veya ciddi ihlallerde daha ağır askıya alma uygulanabilir.
- API yanlış kullanımı, kontrolsüz otomatik bütçe değişiklikleri ve reklam politikası
  ihlalleri risk üretir. İlk bağlantıda yalnızca okuma kullanın; yazmayı kademeli açın.
- Developer token üretim sorgusu için en az **Explorer** erişimi ister; yeni token'lar çoğu
  zaman otomatik Explorer'a yükseltilir. "Yalnızca test hesaplarıyla onaylı" hatası
  görürseniz token henüz üretim hesabına erişemiyordur.

## Meta ban/askıya alma
- Aşırı otomatik düzenleme (ör. saatte onlarca optimizasyon) işaretlenme riski taşır.
  Pause-by-default ve düzenli, ölçülü değişiklik tercih edin.
- Resmî connector token süresi sınırlıdır (~60 gün). Süre dolunca işlemler sessizce
  başarısız olabilir; takvim hatırlatması kurun.
- "Onayladım" der ama Ads Manager'da değişiklik görünmez" bilinen bir beta sorunudur;
  her mutasyondan sonra **tekrar sorgulayıp** önce/sonra farkını doğrulayın.

## Üçüncü taraf remote MCP kullanırsanız
- Reklam verisi o sağlayıcının altyapısından işlenir; bunu kabul etmiş olursunuz.
- Anthropic, custom connector'ların doğrulanmamış olabileceğini ve yalnızca güvenilen
  sunuculara bağlanılmasını belirtir. Mümkünse resmî connector'ları tercih edin.

## CVE notu (dürüstlük)
- Eski belgenin "pipeboard CVE-2026-48039 / CVSS 9.1" iddiası bağımsız doğrulanamadı; kesin
  gerçek olarak sunulmuyor. Genel MCP STDIO RCE açıkları ailesi (2025–2026) ise belgelidir.
  Sonuç: üçüncü taraf MCP'lerde sürüm sabitleme, kendi sunucunuzda barındırma, dar yetki ve
  yazma onayı şarttır.

## Ek: Meta connector caveat'ları (docs/10 referans kütüphanesi)
- **`@meta/ads-cli` nesneleri VARSAYILAN ACTIVE oluşturur** — `--status PAUSED` vermezsen reklam
  canlı başlar. Bu, paketin "PAUSED-by-default" varsayımını bozar; CLI yolunu kullanıyorsan
  guardrail'e EK olarak status'u sen zorlamalısın. (MCP/connector yolunda yeni nesneler PAUSED.)
- Meta MCP **Claude Code OAuth bug'ı** → güvenilir yol **Claude.ai web connector**. ~200 çağrı/saat;
  açık beta sessiz hatalar; her mutasyondan sonra tekrar sorgulayıp doğrula.
- Bilinen: Lead Ads TOS hatası (Error 100 / 1815089).
- MCP STDIO RCE ailesi (OX Security, Nis 2026): MCP config'i güvenilmez kabul et; token env var'da.
