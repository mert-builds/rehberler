# Tek saniye kurgu yapmadan reels: Claude Code ile video kurgusu

Benim reels'lerimin hepsi bu sistemle çıkıyor. Ben sadece konuşuyorum; boşlukları kesmek, altyazı, arka plan ve başlık animasyonları Claude Code'un işi.

## Kullandığım araçlar (hepsi ücretsiz)

| İş | Araç |
|---|---|
| Sesi kelime kelime yazıya dökmek | [whisper.cpp](https://github.com/ggml-org/whisper.cpp) (bilgisayarında çalışır) |
| Boşlukları ve duraksamaları kesmek | `ffmpeg` (sessizlik tespiti) + whisper zamanlamaları |
| Seni arka plandan kesmek | Apple Vision (macOS'ta yerleşik kişi ve nesne ayırma) |
| Başlıklar, kartlar, animasyonlar | [Remotion](https://www.remotion.dev) (React ile video) |

## Akış

1. Telefonla dikey (9:16) çek. Yüzün kadrajın üst yarısında olsun.
2. Claude Code'a şunu de:
   ```
   Bu videodaki 0.2 saniyeden uzun duraksamaları kes. Sesi whisper ile yazıya dök
   ve her kelimenin zamanını çıkar.
   ```
3. Arka planı değiştirmek için:
   ```
   Apple Vision ile beni videodan kes, şeffaf arka planlı bir webm yap
   ve arkama bu ofis fotoğrafını koy.
   ```
4. Animasyonlar için Remotion projesi kur ve başlıkları kelimelere bağla:
   ```
   Remotion ile 1080x1920 bir video yap. "token" dediğim anda başımın arkasında
   büyük bir başlık çıksın, araç isimleri cam kartlarda gelsin, altyazılar
   beyaz ve siyah çerçeveli olsun.
   ```
5. Render al: `npx remotion render`.

## İpuçları

- Efektleri isimleriyle iste: "orbit ring", "head stack", "comment drop", "dolly zoom".
- Her efekti söylediğin kelimeye bağla. Video böylece "konuşulanı gösteren" bir hale gelir.
- Konuştuğun konuyla ilgili görseller ekranda en az 2 saniye kalsın, izleyici okuyabilsin.

---
Bunun gibi gurme bilgiler için takip et 👉 [@mert.builds](https://www.instagram.com/mert.builds/)
