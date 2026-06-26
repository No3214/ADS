/**
 * Kozbeyli Konağı — Olay yardımcıları (GA4 + Meta, tek kaynak)
 * Dosya: app/_analytics/events.ts
 *
 * Bu helper'lar dataLayer'a STANDART olaylar gönderir. GTM içinde:
 *  - GA4 etiketleri bu event adlarını dinler (purchase, begin_checkout, generate_lead...)
 *  - Google Ads "Satın alma" dönüşümü purchase + transaction_id ile beslenir (tekilleştirme).
 *  - Meta Pixel etiketi Purchase/InitiateCheckout/Lead'i AYNI event_id ile gönderir (CAPI dedup).
 *
 * KRİTİK: purchase olayı HMS onay (teşekkür) sayfasında tetiklenmeli. O sayfa AYRI alandadır
 * ({slug}.hmshotel.net). Onay sayfasının gerçek transaction_id/value/currency sağlayıp
 * sağlamadığı TEST REZERVASYONU ile doğrulanmalı (docs/01). Sağlamıyorsa offline import.
 */

type Currency = 'TRY';

export interface PurchaseInput {
  transactionId: string;   // HMS rezervasyon no (benzersiz). ZORUNLU — tekilleştirme anahtarı.
  value: number;           // Toplam rezervasyon tutarı.
  currency?: Currency;     // Varsayılan TRY.
  roomId?: string;
  roomName?: string;
  nights?: number;
}

export interface LeadInput {
  method: 'phone' | 'whatsapp' | 'form';
}

declare global {
  interface Window {
    dataLayer?: Record<string, unknown>[];
  }
}

function push(obj: Record<string, unknown>) {
  if (typeof window === 'undefined') return;
  window.dataLayer = window.dataLayer || [];
  window.dataLayer.push(obj);
}

/** Aynı event_id'yi GA4 purchase ile Meta Purchase arasında paylaşmak için. */
function newEventId(prefix: string): string {
  const rnd = Math.random().toString(36).slice(2, 10);
  return `${prefix}_${Date.now()}_${rnd}`;
}

/** Oda detay görüntüleme. */
export function viewItem(roomId: string, roomName: string, price?: number) {
  push({ ecommerce: null });
  push({
    event: 'view_item',
    ecommerce: {
      currency: 'TRY',
      items: [{ item_id: roomId, item_name: roomName, price }],
    },
  });
}

/** Müsaitlik / tarih araması. */
export function search(query: string, checkin?: string, checkout?: string) {
  push({ event: 'search', search_term: query, checkin, checkout });
}

/** Rezervasyon akışına giriş (HMS'e yönlenmeden hemen önce tetikleyin). */
export function beginCheckout(value?: number, roomId?: string, roomName?: string) {
  const eventId = newEventId('ic');
  push({ ecommerce: null });
  push({
    event: 'begin_checkout',
    event_id: eventId, // Meta InitiateCheckout ile paylaşılır.
    ecommerce: {
      currency: 'TRY',
      value,
      items: roomId ? [{ item_id: roomId, item_name: roomName, price: value }] : [],
    },
  });
  return eventId;
}

/**
 * Rezervasyon tamamlandı (HMS onay sayfası). Google Ads "Satın alma" + GA4 purchase.
 * value/currency/transaction_id HMS'ten DİNAMİK gelmeli; sabit değer girmeyin.
 */
export function purchase(input: PurchaseInput) {
  const { transactionId, value, currency = 'TRY', roomId, roomName, nights } = input;
  const eventId = newEventId('pur');
  push({ ecommerce: null });
  push({
    event: 'purchase',
    event_id: eventId, // Meta Purchase ile AYNI id (CAPI tekilleştirme).
    ecommerce: {
      transaction_id: transactionId,
      value,
      currency,
      items: [
        {
          item_id: roomId ?? 'ODA',
          item_name: roomName ?? 'Oda',
          price: value,
          quantity: nights ?? 1,
        },
      ],
    },
  });
  return eventId;
}

/** Telefon / WhatsApp / form tıklaması (butik otelde kapanış kanalı). */
export function generateLead(input: LeadInput) {
  const eventId = newEventId('lead');
  push({
    event: 'generate_lead',
    event_id: eventId, // Meta Lead/Contact ile paylaşılır.
    method: input.method,
  });
  return eventId;
}
