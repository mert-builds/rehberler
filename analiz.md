# Kaydettiğin reels'leri Claude'a izletip veritabanı yapmak

Instagram'da kaydettiğin yüzlerce reel genelde bir daha açılmıyor. Ben 219 reel'imi Claude Code'a izlettim ve içlerinden çıkan her aracı, repoyu ve linki aranabilir bir veritabanına koydurdum. Her sabah yeni kaydettiklerimi de kendisi ekliyor.

## Kullandığım parçalar

| Parça | Ne işe yarıyor |
|---|---|
| [Claude in Chrome](https://claude.ai/chrome) | Claude, açık Chrome'unda "Kaydedilenler" sayfanı okuyor (sadece okuma) |
| [whisper.cpp](https://github.com/ggml-org/whisper.cpp) | Her videonun sesini bilgisayarında yazıya döküyor |
| SQLite | Araçlar, linkler, açıklamalar aranabilir bir veritabanında |
| macOS launchd | Her sabah otomatik çalışma |

## Claude Code'a vereceğin görev

```
Chrome'da instagram.com/<kullanıcı-adım>/saved sayfamı aç. Kaydettiğim reels'lerin
listesini çıkar. Her birinin açıklamasını ve sesini (whisper ile yazıya dökerek)
incele. İçinde geçen araçları, GitHub repolarını ve siteleri bul. Her birini
ne işe yaradığıyla birlikte bir SQLite veritabanına ve okunabilir bir HTML
kataloğa yaz. Hiçbir şeyi beğenme, yorum yapma, takip etme: sadece oku.
```

Sonra şöyle sorabilirsin:

```
Video kurgusu için ne kaydetmiştim? En işe yarayan 3 tanesini söyle.
```

## Dikkat

- Instagram hesabında hiçbir işlem yaptırma, sadece okuma.
- İstekleri yavaş tut (saniyede ~1). Çok hızlı giderse Instagram geçici olarak engelleyebilir.

---
Bunun gibi gurme bilgiler için takip et 👉 [@mert.builds](https://www.instagram.com/mert.builds/)
