// Ağır/etkileşimli bileşenleri ertele (bundle küçült, ilk yükü hızlandır).
import dynamic from "next/dynamic";

// Harita / galeri lightbox / takvim gibi ağır client bileşenleri:
const Map = dynamic(() => import("@/components/Map"), {
  ssr: false, loading: () => <div aria-hidden className="h-80 bg-stone-100 animate-pulse" />,
});
const Gallery = dynamic(() => import("@/components/Gallery"), { loading: () => <p>Yükleniyor…</p> });

export function ContactSection() {
  return <section><Map /><Gallery /></section>;
}
// Kural: above-the-fold içeriği SSR/SSG ile statik; ağır etkileşim aşağıda dynamic.
