// next/image — lazy default, hero için priority, blur placeholder, doğru sizes.
import Image from "next/image";

export function Hero() {
  return (
    <Image
      src="/images/hero.jpg" alt="Kozbeyli Konağı taş konak cephesi, Foça"
      width={1920} height={1080} priority         // LCP görseli: priority + preload
      sizes="100vw" placeholder="blur" blurDataURL="data:image/jpeg;base64,/9j/..." />
  );
}
export function RoomCard({ src, name }: { src: string; name: string }) {
  return (
    <Image
      src={src} alt={`${name} — Kozbeyli Konağı`}
      width={800} height={600} loading="lazy"     // viewport dışı: lazy (varsayılan)
      sizes="(max-width: 768px) 100vw, 33vw" />    // responsive: küçük ekranda tam genişlik
  );
}
// Kurallar: her <img> yerine next/image; alt ZORUNLU; LCP'ye priority; gerisi lazy.
// CMS (Payload) görselleri için loader/remotePatterns yapılandır.
