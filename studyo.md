# Abonelik ödemeden yapay zeka video stüdyosu: Open Generative AI

[Open Generative AI](https://github.com/anil-matcha/open-generative-ai) (MIT lisanslı, açık kaynak), görsel, video, dudak senkronu ve sinema stüdyosunu tek uygulamada toplayan bir yapay zeka stüdyosu. Aylık abonelik yok: uygulama ücretsiz, modelleri kendi API anahtarınla çağırıyorsun ve sadece ürettiğin kadar ödüyorsun.

## Nedir, ne değildir?

- Uygulamanın kendisi ücretsiz ve açık kaynak (MIT). Mac, Windows ve Linux için masaüstü kurulum dosyası var, istersen kaynaktan da çalıştırabilirsin.
- Bulut modeller (Flux, Kling, Veo, Seedance, Nano Banana gibi) [Muapi](https://muapi.ai) üzerinden çalışıyor. Muapi'den bir erişim anahtarı (API key) alıyorsun, her üretimde kredin düşüyor. Yani abonelik yok ama üretimin bedava da değil.
- README'ye göre masaüstü uygulamada bazı modeller (SD 1.5, SDXL, Z-Image) bilgisayarında yerel de çalışabiliyor. Bu durumda anahtar gerekmiyor, ama bilgisayarın güçlü olmalı (Z-Image için 16 GB RAM öneriliyor).

## İçindeki stüdyolar

Videoda anlattığım dördü:

| Stüdyo | Ne yapar |
|---|---|
| Image Studio | Yazıdan görsel, görselden görsel (referans resimle düzenleme) |
| Video Studio | Yazıdan video, görseli videoya çevirme |
| Lip Sync Studio | Portre fotoğrafı + ses = konuşan video, ya da mevcut videoya dudak senkronu |
| Cinema Studio | Kamera, lens, odak uzaklığı ve diyafram seçerek sinematik çekim |

README'de bunların yanında Audio, AI Clipping, Workflow, Agent, Marketing gibi başka stüdyolar da listeleniyor. Model sayısı README'de farklı yerlerde 200+ ve 600+ olarak geçiyor; ben videoda temkinli olanı (200+) söyledim.

Cinema Studio'da seçenekler: altı kamera tipi (16mm film, 70mm film, dijital sinema kameraları), on bir lens tipi, 8mm'den 85mm'ye focal length ve f/1.4, f/4, f/11 diyafram.

## Kurulum (en kolay yol: masaüstü uygulama)

1. [Releases sayfasından](https://github.com/Anil-matcha/Open-Generative-AI/releases) işletim sistemine uygun dosyayı indir (Mac için Apple Silicon `arm64.dmg` ya da Intel `.dmg`).
2. Mac'te uygulamayı `Applications` klasörüne sürükle. Apple imzası olmadığı için ilk açılışta engeller. Terminal'e şunu yaz:

```bash
xattr -cr "/Applications/Open Generative AI.app"
```

3. Uygulamaya sağ tıkla, Aç de, çıkan pencerede tekrar Aç de. Bunu bir kez yapman yeterli.
4. [muapi.ai/access-keys](https://muapi.ai/access-keys) adresinden anahtar oluştur ve uygulamaya yapıştır. Anahtarın adını değil, değerini yapıştır.

## Kaynaktan kurulum

Node.js 18 ya da üstü gerekli.

```bash
git clone --recurse-submodules https://github.com/Anil-matcha/Open-Generative-AI.git
cd Open-Generative-AI
npm run setup        # sadece npm install yetmez, bu adım şart
npm run electron:dev # masaüstü uygulama
# ya da: npm run dev -> http://localhost:3000
```

## Daha kolayı: Claude Code'a kurdur

Terminalde Claude Code'u aç ve şunu yapıştır:

```
https://github.com/Anil-matcha/Open-Generative-AI reposunu ~/Code klasörüne
--recurse-submodules ile klonla. README'deki Quick Start adımlarını sırayla uygula
(npm run setup, sonra npm run dev). Node.js 18+ yoksa önce bana söyle.
Çalışınca http://localhost:3000 adresini aç.
API anahtarını sana vermeyeceğim: uygulama ilk açılışta istediğinde ben kendim
gireceğim. Anahtarı hiçbir dosyaya yazma ve git'e ekleme.
```

Anahtarı Claude'a yazdırma, uygulamanın kendi ekranına sen gir.

## İpuçları

- **Maliyeti kontrol et:** Her modelin üretim başına kredisi farklı. Önce en ucuz modelle ve kısa sürede dene (5 saniyelik video, düşük çözünürlük), beğenince pahalı modele geç. Muapi panelinden harcamanı takip et.
- **Önce görsel, sonra video:** Video modelleri pahalı. Image Studio'da istediğin kareyi bul, sonra Video Studio'da o kareyi başlangıç görseli yapıp canlandır. Boşa video üretmezsin.
- **Karakter tutarlılığı:** Aynı kişiyi birden çok sahnede istiyorsan referans görsel destekleyen düzenleme modellerini kullan (README'ye göre bazıları 14 referans görsele kadar alıyor).
- **Konuşan karakter:** Lip Sync Studio'da portre + ses dosyası yeterli. Sesi ayrıca üretip yükle.
- **Sinematik hava:** Cinema Studio'da kamera, lens ve diyaframı seç. Portre için 85mm ve f/1.4 (alan derinliği az), manzara için 24mm ve f/11 iyi bir başlangıç.
- **Yerel model denemek istersen:** Ayarlar, Local Models bölümünden SD 1.5 gibi hafif bir modeli indirebilirsin. 8 GB RAM'li Mac'te Z-Image yerine SD 1.5 kullan (README, Z-Image'ın bu makinelerde sistemi kilitleyebildiğini söylüyor).
- **Sorumluluk:** Ürettiğin içerikten sen sorumlusun. Bir kişinin yüzünü ya da sesini izinsiz kullanma, ticari kullanımda her modelin lisansına bak.

## Diğer rehberler

[Tüm rehberler](README.md): [kurgu.md](kurgu.md) (Whisper + Remotion ile kurgu), [editor.md](editor.md) (CapCut'a açık kaynak alternatif), [altyazi.md](altyazi.md) (ücretsiz altyazı), [analiz.md](analiz.md) (reels'leri Claude'a izlet).

---
Bunun gibi gurme bilgiler için takip et 👉 [@mert.builds](https://www.instagram.com/mert.builds/)
