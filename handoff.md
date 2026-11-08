# Claude Code'da token bitmesin: Caveman + handoff.md + /clear

**Sorun:** Claude Code'da uzun çalıştıkça context doluyor, tokenların çabuk bitiyor. `/compact` her şeyi tek bir özete sıkıştırıyor ama gereksiz bilgiler de o özetin içinde kalıyor, yani gerçek bir temizlik olmuyor.

**Çözüm iki parça:**
1. **Caveman:** Claude'un cevaplarını kısaltıp tokenları azaltan açık kaynak araç.
2. **handoff.md + /clear:** Kaldığın yeri bir dosyaya yazdırıp context'i tamamen sıfırlamak.

## 1. Caveman'i kur

GitHub: https://github.com/JuliusBrussee/caveman (Apache-2.0)

Node.js 22.13 veya üstü gerekiyor. Terminale yaz:

```bash
npx @caveman-ai/cli@latest
```

Kurulum ekranı bilgisayarındaki ajanları (Claude Code dahil) bulur, ne değiştireceğini gösterir; Enter'a basman yeterli. Sonra `claude` her zamanki gibi açılır, sadece daha az token harcar.

## 2. Kaldığın yeri handoff.md'ye yazdır

Çalıştığın projenin içinde Claude Code'a şunu de:

```
Bana projemle alakalı bir handoff.md dosyası oluştur. İçinde şunlar olsun:
projenin amacı, şu ana kadar yaptıklarımız, aldığımız kararlar ve nedenleri,
yarım kalan işler, sıradaki adımlar ve dikkat edilmesi gereken tuzaklar.
```

## 3. Context'i sıfırla

```
/clear
```

Geçmiş konuşmanın tamamı gider, ama `handoff.md` dosyan projede durur.

## 4. Kaldığın yerden devam et

```
handoff.md dosyasını oku ve kaldığımız yerden devam et.
```

Claude temiz bir context ile, sadece gerçekten gerekli bilgiyle başlar.

## İpucu

Büyük bir iş bitince ya da context %70'i geçince bu döngüyü tekrarla. Her seferinde `handoff.md`'yi güncellet.

---
Bunun gibi gurme bilgiler için takip et 👉 [@mert.builds](https://www.instagram.com/mert.builds/)
