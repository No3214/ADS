// app/opengraph-image.tsx — dinamik 1200x630 OG görseli (next/og).
import { ImageResponse } from "next/og";
export const runtime = "edge";
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";
export default function OG() {
  return new ImageResponse(
    (<div style={{ width: "100%", height: "100%", display: "flex", flexDirection: "column",
      justifyContent: "center", alignItems: "center", background: "#3f3a30", color: "#fff",
      fontSize: 64, fontWeight: 700 }}>
      Kozbeyli Konağı
      <div style={{ fontSize: 30, marginTop: 12, opacity: .9 }}>Foça · 600 yıllık taş konak otel</div>
    </div>), { ...size }
  );
}
// Gerçek foto OG istersen statik /public/og.jpg (1200x630) kullan + metadata images.
