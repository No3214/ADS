# dataLayer Olay Şeması (geliştirici uygular)

GTM tetikleyicileri bu olaylara bağlanır. `.com` sitesinde + (mümkünse) HMS onay sayfasında push et.

## Ürün/oda görüntüleme (.com /odalar)
```js
dataLayer.push({ event: 'view_item', items:[{ item_name:'Superior Oda', price: 2000 }] });
```

## Rezervasyon başlatma (HMS'e geçişten önce)
```js
dataLayer.push({ event: 'begin_checkout', value: 6000, currency: 'TRY' });
```

## Satın alma (HMS onay/teşekkür sayfası — KRİTİK)
```js
dataLayer.push({
  event: 'purchase',
  transaction_id: 'HMS-REZ-12345',   // benzersiz rezervasyon no
  value: 6000,                       // toplam, sayı
  currency: 'TRY',
  items: [{ item_name:'Superior Oda', price:2000, quantity:3 }]
});
```
- `transaction_id` hem GA4 hem Google Ads hem Meta `eventID` için kullanılır (dedup).
- HMS onay sayfasına dokunamıyorsan: fixes/05 ile HMS desteğinden bunu iste; olmazsa yedek (03).
