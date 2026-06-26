# Apache / Nginx güvenlik başlıkları (Next.js dışı host)

## Apache (.htaccess)
```apache
Header always set Strict-Transport-Security "max-age=63072000; includeSubDomains; preload"
Header always set X-Content-Type-Options "nosniff"
Header always set Referrer-Policy "strict-origin-when-cross-origin"
Header always set X-Frame-Options "SAMEORIGIN"
Header always set Permissions-Policy "geolocation=(self), camera=(), microphone=()"
```

## Nginx
```nginx
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
add_header X-Content-Type-Options "nosniff" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header X-Frame-Options "SAMEORIGIN" always;
add_header Permissions-Policy "geolocation=(self), camera=(), microphone=()" always;
```
CSP'yi ayrı ve Report-Only başlayarak ekle; kırılma yoksa enforce'a geç.
