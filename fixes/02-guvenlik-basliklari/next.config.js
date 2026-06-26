// .com (Next.js) için güvenlik başlıkları. CSP'yi ÖNCE Report-Only ile test et
// (yanlış CSP siteyi bozabilir). HSTS/diğerleri düşük risk.
const securityHeaders = [
  { key: 'Strict-Transport-Security', value: 'max-age=63072000; includeSubDomains; preload' },
  { key: 'X-Content-Type-Options', value: 'nosniff' },
  { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
  { key: 'X-Frame-Options', value: 'SAMEORIGIN' },
  { key: 'Permissions-Policy', value: 'geolocation=(self), camera=(), microphone=()' },
  // CSP: önce Report-Only dene; GTM/GA/Meta/Maps/HMS izinli. Gerçek domainlerine göre genişlet.
  { key: 'Content-Security-Policy-Report-Only', value: [
      "default-src 'self'",
      "script-src 'self' 'unsafe-inline' https://www.googletagmanager.com https://www.google-analytics.com https://connect.facebook.net",
      "img-src 'self' data: https: https://www.google-analytics.com https://www.facebook.com",
      "style-src 'self' 'unsafe-inline'",
      "frame-src https://www.googletagmanager.com https://td.doubleclick.net https://*.hmshotel.net",
      "connect-src 'self' https://www.google-analytics.com https://connect.facebook.net https://*.hmshotel.net"
    ].join('; ') }
];
module.exports = {
  async headers() {
    return [{ source: '/:path*', headers: securityHeaders }];
  }
};
