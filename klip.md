# Yayınlardaki en iyi anları otomatik kesmek: GTAHunter6

[GTAHunter6](GTAHunter6/), bir yayının sohbetini okuyup sohbetin patladığı anları bulan ve o anlardan dikey (9:16) klipler kesen ücretsiz bir araç. Claude Code'a tek mesajla yazdırdım; kodu bu repoda, açık.

Twitch yayın kayıtlarında (VOD) ve YouTube canlı yayın kayıtlarında çalışıyor.

## Fikir

Yayını senin yerine binlerce kişi izliyor: sohbettekiler. Çılgın bir şey olduğu an, birkaç saniye içinde sohbete yüzlerce mesaj düşüyor. O patlama, o anın klip olacağının en net işareti.

Tuzak şu: sohbet hep geç tepki veriyor. Klibi patlama anında kesersen olayın kendisini kaçırırsın. O yüzden araç her klibi patlamadan **25 saniye önce** başlatıyor.

## Ne yapıyor?

1. Yayının bütün sohbetini indiriyor (Twitch'te giriş gerekmiyor; YouTube'da yayının sohbet kaydı açık olmalı).
2. Sohbeti 15 saniyelik dilimlere bölüyor ve her dilimde **kaç farklı kişinin** yazdığını sayıyor. Tek kişinin spam'i patlama sayılmıyor.
3. Her dilimi yayının o bölümündeki normal yoğunlukla kıyaslıyor, en sert 10 sıçramayı seçiyor (aralarında en az 60 saniye).
4. Her patlamanın başladığı saniyeyi bulup klibi 25 saniye önceden başlatıyor, 15 saniye kesiyor.
5. Klibe sohbette en çok tekrarlanan sözün adını koyuyor: "Polis uçtu", "Bu nasıl kaza" gibi.
6. Yayının tamamını değil, sadece o 15 saniyeyi indiriyor. 1080×1920 dikey video yapıyor: yatay görüntünün tamamı ortada, arkası bulanık.

7 saatlik bir Twitch yayınında (65 bin mesaj) 10 klip yaklaşık 11 dakikada çıktı.

## Gerekenler

- Mac ya da Linux, Python 3.10 veya üstü.
- `ffmpeg` ve `yt-dlp` (Mac'te: `brew install ffmpeg yt-dlp`).
- Bitmiş bir yayının linki: `twitch.tv/videos/...` ya da YouTube canlı yayın kaydı. Sadece abonelere açık yayınlar çalışmaz.

## Kurulum ve kullanım

```bash
git clone https://github.com/mert-builds/rehberler.git
cd rehberler/GTAHunter6
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt

# Twitch yayını
.venv/bin/python -m gtahunter6.cli https://www.twitch.tv/videos/YAYIN_ID

# YouTube canlı yayın kaydı
.venv/bin/python -m gtahunter6.cli "https://www.youtube.com/watch?v=VIDEO_ID"

# Önce sadece anları gör, video kesme
.venv/bin/python -m gtahunter6.cli LINK --detect-only
```

Ayarlar:
- `--top 10` kaç klip
- `--lead 25` patlamadan kaç saniye önce başlasın
- `--dur 15` klip kaç saniye
- `--min-gap 60` iki patlama arası en az kaç saniye

Çıktı `out/` klasörüne gidiyor: klipler, `clips.csv` (zamanlar, sohbet sayıları, başlıklar) ve sohbet yoğunluğu grafiği (`chat-density.png`).

İpucu: olay klibin sonunda kesiliyorsa `--lead 20` ya da `--dur 25` dene. Sohbetin gecikmesi yayıncıya göre değişiyor.

## Claude'a yapıştıracağın komut

Repo'yu klonla, `GTAHunter6` klasöründe Claude Code'u aç ve şunu yapıştır:

```text
Bu klasördeki GTAHunter6 aracını benim için kur ve çalıştır.
Önce README.md dosyasını oku.
1. ffmpeg ve yt-dlp kurulu mu kontrol et; yoksa nasıl kuracağımı söyle.
2. .venv oluştur, requirements.txt'yi kur, testleri çalıştır (pytest).
3. Sana vereceğim yayın linkiyle önce --detect-only çalıştır,
   bulduğu anları ve chat-density.png grafiğini bana göster.
4. Ben onaylayınca klipleri kes. Her klibin 1080x1920 ve 15 saniye
   olduğunu ffprobe ile kontrol et, sonucu bana yaz.
```

## Dikkat

- Klipleri yayınlamadan önce yayıncının klip ve yeniden yükleme kurallarına bak. Birçok yayıncı klip kanallarına izin veriyor, bazıları vermiyor.
- Twitch, sohbet çok yoğun olduğunda bir saniyedeki mesajların bir kısmını döndürmeyebiliyor. En güçlü anlar yine de listenin başına çıkıyor.
- YouTube indirme hatası verirse `yt-dlp`'yi güncelle: `brew upgrade yt-dlp`.

Bunun gibi gurme bilgiler için takip et 👉 [@mert.builds](https://www.instagram.com/mert.builds/)
