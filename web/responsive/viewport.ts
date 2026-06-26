// app/layout viewport (Next.js 15) — themeColor + güvenli alan.
import type { Viewport } from "next";
export const viewport: Viewport = {
  width: "device-width", initialScale: 1, themeColor: "#3f6b4f", colorScheme: "light",
  // maximumScale KOYMA (erişilebilirlik: kullanıcı zoom'u engellenmemeli).
};
