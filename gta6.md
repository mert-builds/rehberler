# GTA 6 yayınlarından otomatik klip: GTAHunter6 kurulum rehberi

Bu rehber, uzun bir yayının (Twitch ya da YouTube canlı yayın kaydı) en heyecanlı anlarını bulup dikey (9:16) klip olarak kesen **GTAHunter6** aracını kurmak için. Aracın kodu bu repoda, açık: [GTAHunter6/](GTAHunter6/).

Kod bilmene gerek yok. Rehberi Claude Code'a okutuyorsun, kurulumu o yapıyor.

> Kazanç garanti değil. Bu bir araç; klibin izlenip izlenmeyeceği yayıncıya, içeriğe ve sana bağlı.

---

## En kolay yol: rehberi Claude'a okut

1. Bilgisayarında boş bir klasör aç (örnek: `klipler`).
2. O klasörde terminali aç ve `claude` yazıp Claude Code'u başlat.
3. Aşağıdaki mesajı olduğu gibi yapıştır, Enter'a bas:

```text
Şu rehberi oku ve içindeki "Claude için kurulum talimatı" bölümünü
adım adım benim bilgisayarımda uygula:
https://raw.githubusercontent.com/mert-builds/rehberler/main/gta6.md

Her adımdan sonra ne yaptığını kısaca söyle. Bir şey kurman
gerekirse önce bana sor. Sonunda bana bir yayın linki sor.
```

4. Claude bir şey kurmak için izin isterse "evet" de.
5. Sonunda senden bir yayın linki isteyecek. Bitmiş bir Twitch yayınının (`twitch.tv/videos/...`) ya da YouTube canlı yayın kaydının linkini ver.
6. Önce anları ve sohbet grafiğini gösterir; sen onaylayınca klipleri keser.

Bu kadar. Aşağısı, aracın nasıl çalıştığı ve Claude'un uygulayacağı adımlar.

---

## Mantık: sohbet bir alarm gibi çalar

Yayını senin yerine binlerce kişi izliyor: sohbettekiler. Önemli bir an yaşandığında birkaç saniye içinde sohbete yüzlerce mesaj düşüyor. İşte burası videonun pik noktası.

Araç yayını izlemiyor, sohbeti okuyor:

1. **İndiriyor.** Yayının bütün sohbetini indiriyor. Twitch'te giriş gerekmiyor; YouTube'da yayının sohbet kaydı açık olmalı.
2. **Dilimliyor.** Sohbeti 15 saniyelik küçük dilimlere bölüyor ve her dilimde **kaç farklı kişinin** yazdığını sayıyor. Tek kişinin spam'i patlama sayılmıyor.
3. **Pikleri seçiyor.** Her dilimi yayının o bölümündeki normal yoğunlukla kıyaslıyor ve en sert 10 sıçramayı tek tek seçiyor (aralarında en az 60 saniye).
4. **Önceden kesiyor.** Sohbet hep geç tepki verir. Klibi patlama anında kesersen olayın kendisini kaçırırsın. O yüzden klip, mesajların yoğunlaştığı andan **25 saniye önce** başlıyor ve 15 saniye sürüyor.
5. **Adlandırıyor.** Klibe sohbette en çok tekrarlanan sözü ad olarak koyuyor, mesela `01-polis-uctu.mp4`.
6. **Dikey yapıyor.** Yayının tamamını değil, sadece o 15 saniyeyi indiriyor ve 1080x1920 dikey video yapıyor: yatay görüntünün tamamı ortada, arkası bulanık.

Kendi denememde 7 saatlik bir Twitch yayınında (65 bin mesaj) 10 klip yaklaşık 11 dakikada çıktı.

---

## Gerekenler

| Ne | Neden | Not |
|---|---|---|
| Mac ya da Linux | Araç bu sistemlerde denendi | Windows'ta WSL (Ubuntu) ile çalışması gerekir, ama denemedim |
| Python 3.9 veya üstü | Aracın dili | Mac'te hazır gelen Python 3.9 ile denendi, çalışıyor |
| `ffmpeg` | Videoyu kesip dikey yapmak | Mac: `brew install ffmpeg` |
| `yt-dlp` | Yayından sadece gereken 15 saniyeyi indirmek | Mac: `brew install yt-dlp` |
| `git` | Repoyu indirmek | Mac'te `xcode-select --install` ile gelir |
| Claude Code | Kurulumu senin yerine yapmak | [claude.com/claude-code](https://claude.com/claude-code) |
| Bitmiş bir yayın linki | Klip kaynağı | Sadece abonelere açık yayınlar çalışmaz |

---

## Claude için kurulum talimatı

> Claude: bu bölümü sırayla uygula. Her adımın sonundaki kontrolü çalıştır; kontrol geçmezse bir sonraki adıma geçme, kullanıcıya sorunu ve çözümünü söyle. Kullanıcının bilgisayarına bir şey kurmadan önce izin iste. Komutları kullanıcının bulunduğu klasörde çalıştır.

### Adım 1. İşletim sistemini öğren

```bash
uname -s
```

- `Darwin` = Mac. Devam et.
- `Linux` = Linux. Paket kurulumlarında `brew` yerine `apt` kullan (`sudo apt install ffmpeg git python3-venv` ve `pipx install yt-dlp` ya da `python3 -m pip install --user yt-dlp`).
- Windows ise: kullanıcıya WSL (Ubuntu) kurmasını öner, sonra Linux yolunu izle. Windows'ta denenmediğini söyle.

### Adım 2. Gerekli programları kontrol et

```bash
python3 --version
git --version
ffmpeg -version | head -1
yt-dlp --version
```

Kontrol: Python 3.9 veya üstü, dördü de bir sürüm yazmalı.

Eksik olan varsa (Mac):

```bash
# Homebrew yoksa önce bunu kur (kullanıcıya sor):
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

brew install ffmpeg yt-dlp git python
```

Sonra 4 kontrol komutunu tekrar çalıştır.

### Adım 3. Aracı indir

```bash
git clone https://github.com/mert-builds/rehberler.git
cd rehberler/GTAHunter6
```

Kontrol: `ls` çıktısında `gtahunter6`, `requirements.txt`, `README.md` ve `tests` görünmeli.

### Adım 4. Python ortamını kur

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Kontrol: komut hatasız bitmeli (pip'in "yeni sürüm var" uyarısı sorun değil).

### Adım 5. Testleri çalıştır

```bash
.venv/bin/python -m pytest -q tests
```

Kontrol: son satır `5 passed` gibi olmalı, `failed` olmamalı.

### Adım 6. Yayın linkini iste ve önce sadece anları bul

Kullanıcıdan bitmiş bir yayının linkini iste: `https://www.twitch.tv/videos/...` ya da YouTube canlı yayın kaydı `https://www.youtube.com/watch?v=...`.

```bash
.venv/bin/python -m gtahunter6.cli "YAYIN_LINKI" --detect-only
```

Bu adım video kesmez, sadece sohbeti indirip anları bulur. Uzun yayınlarda sohbet indirmesi birkaç dakika sürebilir; kullanıcıya beklediğini söyle.

Kontrol: `out/` altında yayının klasörü oluşmalı; içinde `clips.csv` ve `chat-density.png` olmalı.

Kullanıcıya göster:
- `clips.csv` içindeki anları tablo olarak (sıra, başlık, başlangıç saati, kaç kişi yazdı),
- `chat-density.png` grafiğini (kırmızı işaretler seçilen anlar).

Sonra sor: "Bu anlardan klip keseyim mi?"

### Adım 7. Onay gelince klipleri kes

```bash
.venv/bin/python -m gtahunter6.cli "YAYIN_LINKI"
```

Kontrol: `out/<platform>-<id>/clips/` içindeki her klibi şununla doğrula:

```bash
for f in out/*/clips/*.mp4; do
  ffprobe -v error -select_streams v:0 -show_entries stream=width,height -show_entries format=duration -of csv=p=0 "$f" | tr '\n' ' '; echo " $f"
done
```

Her satır `1080,1920` ve yaklaşık `15` saniye olmalı. Sonucu kullanıcıya tablo olarak yaz ve `clips` klasörünü açmayı öner (Mac: `open out/*/clips`).

### Adım 8. Kullanıcıya ayarları anlat

Klipler kullanıcının hoşuna gitmezse şu ayarlarla tekrar çalıştır:

| Ayar | Varsayılan | Ne zaman değiştirilir |
|---|---|---|
| `--top 10` | 10 klip | Daha çok ya da az klip için |
| `--lead 25` | Patlamadan 25 sn önce başlar | Olay klibin başında kalıyorsa `--lead 20`, olay kaçıyorsa `--lead 30` |
| `--dur 15` | 15 sn | Olay klibin sonunda kesiliyorsa `--dur 25` |
| `--min-gap 60` | İki an arası en az 60 sn | Birbirine yakın anları da istiyorsa düşür |
| `--window 15` | 15 sn'lik dilimler | Genelde dokunma |

Sohbetin gecikmesi yayıncıya göre değişir; ilk denemeden sonra `--lead` ile oynamak normal.

---

## Video ve sohbeti kendin indirdiysen (TwitchDownloader)

Videoda bahsettiğim ücretsiz [TwitchDownloader](https://github.com/lay295/TwitchDownloader) ile yayını ve sohbetini kendin indirdiysen, araç bunları da kabul ediyor. Link vermek yerine:

```bash
.venv/bin/python -m gtahunter6.cli --video yayin.mp4 --chat chat.json
```

`chat.json` TwitchDownloader'ın sohbet dosyası ya da `yt-dlp`'nin `live_chat.json` dosyası olabilir. Link ile çalışmak daha kolay: araç sohbeti kendisi indirir, videodan da sadece gereken 15 saniyeleri alır.

---

## Çıktılar

```
out/<platform>-<id>/
  clips/01-polis-uctu.mp4 ...   dikey klipler, en güçlü an en başta
  clips.csv                     sıra, başlık, zamanlar, kaç kişi yazdı
  manifest.json                 aynı bilgi, makine için
  chat-density.png              sohbet yoğunluğu grafiği, seçilen anlar kırmızı
  chat.json / *.live_chat.json  indirilen sohbet (tekrar çalıştırınca yeniden indirilmez)
```

---

## Sorun çıkarsa

| Sorun | Çözüm |
|---|---|
| `command not found: ffmpeg` ya da `yt-dlp` | Adım 2'deki `brew install` satırını çalıştır |
| YouTube indirmesi hata veriyor | `brew upgrade yt-dlp` (YouTube sık değişiyor, yt-dlp'nin güncel olması gerekiyor) |
| YouTube'da sohbet bulunamadı | Yayının "sohbet tekrarı" kapalı olabilir; o yayında araç çalışmaz |
| Twitch yayını açılmıyor | Yayın silinmiş ya da sadece abonelere açık olabilir |
| Çok yoğun anlarda sayılar düşük görünüyor | Twitch çok yoğun saniyelerde mesajların bir kısmını döndürmeyebiliyor; en güçlü anlar yine de listenin başına çıkıyor |

---

## Dikkat

- Klipleri yayınlamadan önce yayıncının klip ve yeniden yükleme kurallarına bak. Birçok yayıncı klip kanallarına izin veriyor, bazıları vermiyor.
- Klipleri YouTube Shorts ya da Instagram'a otomatik yükleme özelliği henüz yok; klipleri sen yüklüyorsun.

Videoyu, işine yarayacağını düşündüğün bir arkadaşına gönder.

Bunun gibi gurme bilgiler için takip et 👉 [@mert.builds](https://www.instagram.com/mert.builds/)
