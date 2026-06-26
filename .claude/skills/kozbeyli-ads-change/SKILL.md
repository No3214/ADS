---
name: Kozbeyli Ads Change
description: Kozbeyli Konağı reklam değişikliklerinde önce okuma, plan, dry-run, kod seviyesinde guardrail kontrolü, açık onay ve sonradan doğrulama uygular.
argument-hint: "[platform, hesap, işlem, bütçe]"
disable-model-invocation: true
---

# Güvenli değişiklik protokolü (kod seviyesinde zorunlu)

Bu skill otomatik çağrılamaz. Gerçek yazma yalnızca `config/ads-assets.yaml` içinde
`write_guardrails.enabled: true` VE `.env` içinde `ADS_WRITES_ENABLED=true` ise mümkündür.

## Akış (her değişiklik için)

1. **Oku.** İlgili kampanya/varlığın mevcut değerini sorgula (Meta resmi connector veya
   Google okuma MCP). Eski değeri kaydet.
2. **Plan.** Yapılacak değişikliği `change.json` olarak yaz:
   ```json
   {"platform":"google|meta","account_id":"...","action":"create_campaign|update_budget|pause|enable|...",
    "entity":"campaign","status":"PAUSED","daily_budget_try":0,"monthly_budget_try":0,
    "old_value":{...},"new_value":{...}}
   ```
3. **Guardrail kontrolü (ZORUNLU).** Şunu çalıştır:
   ```bash
   python3 scripts/guardrails.py --check change.json
   ```
   - Çıkış 1 (DENY): işlemi YAPMA, nedeni kullanıcıya söyle.
   - Çıkış 2 (NEEDS_APPROVAL): kullanıcıdan açık onay iste (aşağıdaki biçim).
   - Çıkış 0 (ALLOW): yalnızca onay metni de doğrulandıysa devam.
4. **Dry-run.** Mümkünse API'nin `validate_only`/dry-run modunu kullan. Yoksa payload
   önizlemesi üret ve eski→yeni değeri, günlük/aylık harcama etkisini göster.
5. **Açık onay.** Kullanıcıdan tam olarak şu biçimi iste ve guardrail'e `--approval` ile geçir:
   ```
   ONAYLA | platform | hesap_id | işlem | gunluk_butce
   ```
   `ENABLED` işlemleri AYRI ikinci onay ister:
   ```
   ONAYLA-2 | platform | hesap_id | enable | gunluk_butce
   ```
   ```bash
   python3 scripts/guardrails.py --check change.json --approval "ONAYLA | meta | act_123 | create_campaign | 350"
   ```
6. **Uygula.** Yalnızca guardrail ALLOW (0) verdiyse gerçek mutation'ı çağır.
7. **Doğrula.** Tekrar sorgula; önce/sonra farkını göster. Audit log `logs/` altındadır.

## Sabit kurallar (guardrails.py bunları zorlar)

- Yalnızca allowlist hesapları (Meta `act_...`, Google 10 hane).
- Google aylık 15.000 / günlük 493 TL; Meta aylık 15.000 / günlük 500 TL tavanı aşma.
- Yeni kampanyalar yalnızca `PAUSED`.
- Enable için ikinci onay. Delete, billing, kullanıcı yönetimi, müşteri listesi yükleme yasak.
- Token, secret, OAuth içeriğini isteme veya loglama.

## Türkçe yazım
- Cümle başı tire yerine nokta; cümle içi (devam) tire yerine virgül kullan.

Kullanıcı talebi: $ARGUMENTS
