# Claude Code'a DaVinci Resolve kullandırmak

[DaVinci Resolve MCP](https://github.com/samuelgursky/davinci-resolve-mcp) (MIT) Claude Code'u DaVinci Resolve'a bağlar. Böylece kurguyu ve renk ayarını konuşarak yaptırırsın.

## Kurulum

1. DaVinci Resolve'u aç: **Preferences → General → External scripting using → Local**.
2. Terminale yaz:
   ```bash
   npx davinci-resolve-mcp setup
   ```
   Kurulum Resolve'un yolunu bulur ve Claude Code'a bağlantıyı ekler.
3. Claude Code'u yeniden başlat.

**Not:** Resolve **Studio** sürümü tam destekleniyor. Ücretsiz sürümde uygulama içi köprü (Workspace → Scripts) gerekiyor. Projenin README'sine göre 21.1 ve sonrası ücretsiz sürümde çalışmayabilir.

## Örnek komutlar

```
Medya havuzundaki klipleri sırayla timeline'a diz.
```
```
Tüm kliplere sıcak bir renk ver, kontrastı biraz artır.
```
```
Timeline'ı 1080x1920 dikey olarak render al.
```

---
Bunun gibi gurme bilgiler için takip et 👉 [@mert.builds](https://www.instagram.com/mert.builds/)
