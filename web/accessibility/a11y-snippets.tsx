// Erişilebilirlik drop-in'leri.

// 1) İçeriğe atla (layout'ta ilk öğe)
export function SkipLink() {
  return (
    <a href="#main" className="sr-only focus:not-sr-only focus:fixed focus:top-2 focus:left-2
      focus:z-50 focus:bg-white focus:px-4 focus:py-2 focus:rounded">İçeriğe atla</a>
  );
}

// 2) Erişilebilir form alanı (label bağlı + hata aria)
export function Field({ id, label, error }: { id: string; label: string; error?: string }) {
  return (
    <div>
      <label htmlFor={id} className="block font-medium">{label}</label>
      <input id={id} aria-invalid={!!error} aria-describedby={error ? `${id}-err` : undefined}
        className="min-h-[44px] w-full border rounded px-3" />
      {error && <p id={`${id}-err`} role="alert" className="text-red-700 text-sm">{error}</p>}
    </div>
  );
}

// 3) İkon buton (erişilebilir ad)
export function IconButton({ label, onClick, children }: any) {
  return <button type="button" aria-label={label} onClick={onClick}
    className="min-h-[44px] min-w-[44px] grid place-items-center">{children}</button>;
}
