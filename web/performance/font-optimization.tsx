// next/font — self-host, display:swap, sadece kullanılan subset. CLS'i önler, hızlı.
import { Inter } from "next/font/google";
const inter = Inter({ subsets: ["latin", "latin-ext"], display: "swap", variable: "--font-inter" });

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return <html lang="tr" className={inter.variable}><body>{children}</body></html>;
}
// Yerel font için next/font/local kullan. Marka serif başlık fontunu da subset + swap ile yükle.
