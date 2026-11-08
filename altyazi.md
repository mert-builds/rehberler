# Bilgisayarında ücretsiz altyazı: whisper.cpp

[whisper.cpp](https://github.com/ggml-org/whisper.cpp) (MIT, ~55 bin yıldız), OpenAI Whisper modelinin bilgisayarında çalışan hali. Videonu hiçbir siteye yüklemiyorsun, para da ödemiyorsun. Türkçe dahil onlarca dili anlıyor.

## Kurulum (Mac)

```bash
brew install whisper-cpp ffmpeg
mkdir -p ~/.cache/whisper
curl -L -o ~/.cache/whisper/ggml-large-v3-turbo-q5_0.bin \
  https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo-q5_0.bin
```

## Altyazı çıkar

```bash
ffmpeg -i video.mp4 -ar 16000 -ac 1 -c:a pcm_s16le ses.wav
whisper-cli -m ~/.cache/whisper/ggml-large-v3-turbo-q5_0.bin -f ses.wav -l tr -osrt -of altyazi
```

`altyazi.srt` dosyası oluşur. Bunu CapCut, OpenCut, DaVinci ya da Instagram'a yükleyebilirsin.

## Daha kolayı

Claude Code'a şunu de:

```
Bu videonun Türkçe altyazısını whisper.cpp ile çıkar, srt olarak kaydet.
Yanlış duyulan teknik kelimeleri (Claude, GitHub gibi) düzelt.
```

İpucu: Whisper "Claude" kelimesini sık sık "Cloud" diye duyar. Claude'a düzelttir.

---
Bunun gibi gurme bilgiler için takip et 👉 [@mert.builds](https://www.instagram.com/mert.builds/)
