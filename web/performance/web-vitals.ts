// Core Web Vitals'ı GA4'e gönder (LCP/CLS/INP/FCP/TTFB). app/layout'ta <WebVitals/> ekle.
"use client";
import { useReportWebVitals } from "next/web-vitals";
export function WebVitals() {
  useReportWebVitals((m) => {
    // GA4 event (gtag yüklüyse)
    (window as any).gtag?.("event", m.name, {
      value: Math.round(m.name === "CLS" ? m.value * 1000 : m.value),
      metric_id: m.id, metric_rating: m.rating, non_interaction: true,
    });
  });
  return null;
}
// Hedefler: LCP < 2.5s · INP < 200ms · CLS < 0.1 (mobil saha verisi). Lighthouse + CrUX ile izle.
