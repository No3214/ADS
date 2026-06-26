// Meta Conversions API (sunucu tarafı) — Next.js App Router route handler.
// app/api/meta-capi/route.ts. Pixel ile AYNI event_id (transaction_id) → dedup (48s pencere).
// Secret'lar .env'de: META_PIXEL_ID, META_CAPI_TOKEN. Token'ı koda/URL'ye yazma.
import crypto from "crypto";

const PIXEL_ID = process.env.META_PIXEL_ID!;            // 1781546559309505
const CAPI_TOKEN = process.env.META_CAPI_TOKEN!;        // Events Manager > System User token
const sha256 = (s: string) =>
  crypto.createHash("sha256").update(s.trim().toLowerCase()).digest("hex");

export async function POST(req: Request) {
  const b = await req.json();   // { transaction_id, value, currency, email?, phone?, fbp?, fbc? }
  const payload = {
    data: [{
      event_name: "Purchase",
      event_time: Math.floor(Date.now() / 1000),
      event_id: String(b.transaction_id),               // Pixel eventID ile AYNI
      action_source: "website",
      event_source_url: "https://www.kozbeylikonagi.com/",
      user_data: {
        ...(b.email ? { em: [sha256(b.email)] } : {}),
        ...(b.phone ? { ph: [sha256(b.phone)] } : {}),
        ...(b.fbp ? { fbp: b.fbp } : {}),
        ...(b.fbc ? { fbc: b.fbc } : {}),
      },
      custom_data: { value: Number(b.value), currency: b.currency || "TRY" },
    }],
  };
  const r = await fetch(
    `https://graph.facebook.com/v21.0/${PIXEL_ID}/events?access_token=${CAPI_TOKEN}`,
    { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) }
  );
  return new Response(await r.text(), { status: r.status });
}
// Pixel tarafı (GTM tag 7): fbq('track','Purchase',{value,currency},{eventID: transaction_id})
// → CAPI event_id == Pixel eventID olduğu için Meta tek olay sayar (dedup).
