# Kaydettiğin reels'leri aranabilir bir kütüphaneye çevir

"Bir gün işime yarar" diye kaydettiğin videolar lazım olduğunda bulunmuyor, çünkü kaydedilenler bir kütüphane değil, bir çekmece. Ben kaydettiğim 241 reel'i Claude Code ile aranabilir bir kütüphaneye çevirdim: şu an 228 kaynak, 13 kategori. "Kurgu için ne kaydetmiştim" diyorum, saniyesinde buluyor. Yeni kaydettiklerimi de kendisi ekliyor.

Bu rehberde Claude'a yapıştıracağın komut ve tüm kurulum var.

## Kullandığım parçalar

| Parça | Ne işe yarıyor |
|---|---|
| [Claude Code](https://claude.com/claude-code) | Bütün işi yapan ajan |
| [Claude in Chrome](https://claude.ai/chrome) | Claude, açık Chrome'unda "Kaydedilenler" sayfanı okuyor (sadece okuma) |
| [whisper.cpp](https://github.com/ggml-org/whisper.cpp) | Her videonun sesini kendi bilgisayarında, ücretsiz yazıya döküyor |
| SQLite | Araçlar, repolar, linkler aranabilir bir veritabanında |
| Basit bir HTML sayfa | Kütüphaneyi kategorilere ayrılmış şekilde gezmek için |

## 1. Hazırlık (bir kere)

Mac'te terminale yaz:

```bash
brew install whisper-cpp ffmpeg
```

Chrome'a Claude in Chrome eklentisini kur ve Instagram'a kendi hesabınla giriş yapmış ol.

## 2. Claude Code'a yapıştıracağın komut

Boş bir klasörde `claude` yaz ve şunu yapıştır:

```
Instagram'da kaydettiğim reels'lerden aranabilir bir kütüphane kur.

1. Chrome'da instagram.com/<kullanıcı-adım>/saved/ sayfamı aç. Bütün
   klasörleri ve içlerindeki reels'leri listele (kod, klasör, link).
2. Her reel için: açıklamayı, ilk yorumları ve sabitlenmiş yorumu oku
   (linklerin çoğu oradadır). Videoyu indir ve whisper.cpp ile sesini
   kendi bilgisayarımda yazıya dök (Türkçe olanı Türkçe, İngilizce olanı
   İngilizce).
3. Metinlerde geçen her aracı, GitHub reposunu, siteyi ve yöntemi çıkar.
   Her biri için: ad, link, ne işe yaradığı, fiyat, hangi reel'den geldiği.
4. Hepsini kategorilere ayır (ör. video kurgu, yapay zeka görsel, Claude
   skill'leri, GitHub, reklam) ve bir SQLite veritabanına yaz. Tam metin
   araması olsun.
5. Gezmek için tek sayfalık bir HTML katalog yap (kategori filtresi + arama).
6. Bir senkron komutu yaz: yeni kaydettiğim reels'leri bulup aynı adımlardan
   geçirsin. Bunu her gün otomatik çalıştır (macOS launchd).

Kurallar: Instagram'da hiçbir şeyi beğenme, yorum yapma, takip etme,
kaydı kaldırma; sadece oku. İstekleri yavaş tut (saniyede ~1).
Bir şeyi bulamazsan uydurma, "bulunamadı" yaz.
```

## 3. Kullanım

Kütüphane kurulduktan sonra Claude Code'a şöyle sor:

```
Video kurgusu için ne kaydetmiştim? En işe yarayan 3 tanesini söyle.
```

```
Kaydettiklerimde ücretsiz altyazı aracı var mı?
```

## İpuçları

- **Açıklamaları ve yorumları da okut.** Linklerin yarısı videoda değil, açıklamada ve yorumlarda.
- **Ses dökümü kendi bilgisayarında kalsın.** whisper.cpp internete bir şey yüklemiyor ve ücretsiz.
- **Kategorileri sen belirle.** Kendi işine göre 10-15 kategori, aramayı çok hızlandırıyor.
- **Instagram hesabında hiçbir işlem yaptırma**, sadece okuma. Çok hızlı giderse Instagram geçici olarak engelleyebilir.

---
Bunun gibi gurme bilgiler için takip et 👉 [@mert.builds](https://www.instagram.com/mert.builds/)
