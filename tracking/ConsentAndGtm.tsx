/**
 * Kozbeyli Konağı — Consent Mode v2 + GTM (Next.js 15, App Router)
 * Dosya: app/_analytics/ConsentAndGtm.tsx
 *
 * ÖNEMLİ MİMARİ:
 * - Rezervasyon motoru AYRI alan adındadır: {slug}.hmshotel.net (kozbeylikonagi.com.tr DEĞİL).
 *   Bu yüzden ÇAPRAZ ALAN (cross-domain) ölçümü ZORUNLUDUR ve hmshotel.net'i linker'a eklemeliyiz.
 * - Consent Mode v2 varsayılanı "denied" olmalı (EEA zorunlu, KVKK için en güvenli).
 * - CMP (çerez izni penceresi) GTM'den ÖNCE yüklenmeli ve onay gelince consent 'update' göndermeli.
 *
 * NE YAPMANIZ GEREKİR:
 * 1) NEXT_PUBLIC_GTM_ID env değişkenini canlı GTM container ile doldurun (docs/02 ile seçin).
 * 2) Bu bileşeni app/layout.tsx içinde <body>'nin EN ÜSTÜNE koyun.
 * 3) GA4, Google Ads ve Meta Pixel'i GTM İÇİNDE etiket olarak kurun (kod buraya gömülmez).
 * 4) GA4 Web Stream > Configure tag settings > Configure your domains: hem kozbeylikonagi.com.tr
 *    hem hmshotel.net ekleyin. hmshotel.net'i "unwanted referrals" listesine ekleyin.
 * 5) hmshotel.net booking sayfalarında AYNI GA4 ID + AYNI GTM (veya en az GA4 + linker) bulunmalı.
 *    HMS panelinde GA4/GTM/Pixel ID alanı var mı diye bakın; yoksa HMS desteğine sorun (docs/01).
 */
'use client';

import Script from 'next/script';

const GTM_ID = process.env.NEXT_PUBLIC_GTM_ID; // örn. GTM-XXXXXXX

// Çapraz alan için bağlanacak alan adları. hmshotel.net ZORUNLU.
const LINKER_DOMAINS = ['kozbeylikonagi.com.tr', 'hmshotel.net'];

export default function ConsentAndGtm() {
  if (!GTM_ID) {
    // Konteyner ID yoksa hiçbir şey enjekte etme (yanlış kurulumu önler).
    if (process.env.NODE_ENV !== 'production') {
      // eslint-disable-next-line no-console
      console.warn('[analytics] NEXT_PUBLIC_GTM_ID tanımlı değil; GTM yüklenmedi.');
    }
    return null;
  }

  return (
    <>
      {/* 1) Consent Mode v2 — GTM'DEN ÖNCE. Dört parametre de varsayılan reddedilir. */}
      <Script id="consent-default" strategy="beforeInteractive">
        {`
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('consent', 'default', {
            ad_storage: 'denied',
            ad_user_data: 'denied',
            ad_personalization: 'denied',
            analytics_storage: 'denied',
            functionality_storage: 'granted',
            security_storage: 'granted',
            wait_for_update: 500
          });
          // Çapraz alan linker yapılandırması (GTM/GA4 bunu okur).
          gtag('set', 'linker', { domains: ${JSON.stringify(LINKER_DOMAINS)} });
          // Sayfa görüntüleme öncesi tüketici izni Türkiye/EEA için reddedilmiş başlar.
        `}
      </Script>

      {/* 2) GTM ana snippet'i. CMP onay verince consent 'update' göndermelidir (aşağıdaki helper). */}
      <Script id="gtm-loader" strategy="afterInteractive">
        {`
          (function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
          new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
          j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
          'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
          })(window,document,'script','dataLayer','${GTM_ID}');
        `}
      </Script>

      {/* 3) JS kapalıyken GTM noscript fallback'i. */}
      <noscript>
        <iframe
          src={`https://www.googletagmanager.com/ns.html?id=${GTM_ID}`}
          height="0"
          width="0"
          style={{ display: 'none', visibility: 'hidden' }}
        />
      </noscript>
    </>
  );
}

/**
 * CMP "Kabul Et" / "Reddet" butonlarınız bu fonksiyonları çağırmalı.
 * Onay SAYFA GEÇİŞİNDEN ÖNCE gönderilmeli ki ilk purchase/lead kaybolmasın.
 */
export function grantConsent() {
  // @ts-expect-error gtag global
  window.gtag?.('consent', 'update', {
    ad_storage: 'granted',
    ad_user_data: 'granted',
    ad_personalization: 'granted',
    analytics_storage: 'granted',
  });
}

export function denyConsent() {
  // @ts-expect-error gtag global
  window.gtag?.('consent', 'update', {
    ad_storage: 'denied',
    ad_user_data: 'denied',
    ad_personalization: 'denied',
    analytics_storage: 'denied',
  });
}
