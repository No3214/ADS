# WCAG 2.1 AA Kontrol Listesi (otel sitesi)

## Algılanabilir
- [ ] Tüm görsellerde anlamlı `alt` (dekoratif ise `alt=""`). next/image alt zorunlu.
- [ ] Metin/arka plan kontrastı ≥ **4.5:1** (büyük metin ≥ 3:1). Marka paleti: `renk-kontrast.md`.
- [ ] Bilgi yalnız renkle verilmesin (ikon/etiket ekle).
- [ ] Video/animasyon: otomatik oynatma sessiz + durdurulabilir; altyazı (kreatif videolar).

## Çalıştırılabilir
- [ ] Tam **klavye** erişimi (Tab sırası mantıklı; tuzak yok). Görünür `:focus-visible` halkası.
- [ ] "İçeriğe atla" (skip link) ilk odaklanabilir öğe.
- [ ] Dokunma hedefleri ≥ **44×44px**; yakın hedefler arası boşluk.
- [ ] `prefers-reduced-motion` saygısı (animasyonları kıs).

## Anlaşılabilir
- [ ] `<html lang="tr">` (EN sayfada `lang="en"`). Form `label`'ları bağlı (`htmlFor`).
- [ ] Hata mesajları net + `aria-describedby`; rezervasyon/iletişim formu erişilebilir.
- [ ] Tutarlı navigasyon + başlık hiyerarşisi (tek H1, sıralı H2/H3).

## Sağlam
- [ ] Geçerli, anlamsal HTML (`<nav> <main> <header> <footer> <button> <a>`).
- [ ] ARIA yalnız gerektiğinde (önce native öğe). Landmark roller.
- [ ] Dinamik içerik için `aria-live` (form gönderim durumu).

## Doğrulama
axe DevTools / Lighthouse Accessibility (≥ 95) / WAVE / klavye-only tur / ekran okuyucu (NVDA/VoiceOver) ile test.
