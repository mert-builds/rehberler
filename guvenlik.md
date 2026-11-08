# Uygulamanı yayından önce yapay zekaya test ettir: Shannon

Vibe coding ile hızlı uygulama çıkarmak kolay, ama "çalışıyor" demek "güvenli" demek değil. [Shannon](https://github.com/KeygraphHQ/shannon) (AGPL-3.0, ~51 bin yıldız) web uygulamalarını ve API'leri bir saldırgan gibi test eden açık kaynak bir yapay zeka pentester'ı. Kaynak kodunu analiz ediyor, açıkları buluyor ve gerçekten istismar edip kanıtını gösteriyor.

> ⚠️ **Sadece kendi uygulamanda ya da yazılı izin aldığın sistemlerde kullan.** Başkasının sistemine izinsiz test yapmak suçtur.

## Gereksinimler

- Docker
- Node.js 22+
- Bir yapay zeka sağlayıcısı anahtarı (Anthropic, OpenAI vb.)
- Anthropic ve OpenAI siber güvenlik işlerinde ek doğrulama istiyor. İlk taramadan önce Shannon dokümanlarındaki adımları tamamla.

## Çalıştırma

```bash
npx @keygraph/shannon@latest setup
npx @keygraph/shannon@latest
```

Etkileşimli ekran kurulumda ve ilk taramada yol gösterir.

## Önerim

- Canlı sistem yerine **staging** kopyasını tara.
- Çıkan her açığı Claude Code'a ver: "Bu açığı düzelt ve neden olduğunu açıkla."
- Düzelttikten sonra tekrar tara.

---
Bunun gibi gurme bilgiler için takip et 👉 [@mert.builds](https://www.instagram.com/mert.builds/)
