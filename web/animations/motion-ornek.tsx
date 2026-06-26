// Framer Motion + reduced-motion saygısı. Zarif fade-up reveal.
"use client";
import { motion, useReducedMotion } from "framer-motion";
export function Reveal({ children }: { children: React.ReactNode }) {
  const reduce = useReducedMotion();
  return (
    <motion.div
      initial={reduce ? false : { opacity: 0, y: 12 }}
      whileInView={reduce ? {} : { opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-10%" }}
      transition={{ duration: 0.4, ease: "easeOut" }}>
      {children}
    </motion.div>
  );
}
// Kural: reduce ise animasyon yok. Sadece transform/opacity. Hero LCP'sini geciktirme.
