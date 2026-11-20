# ManyChat'in açık kaynak alternatifi: OpenReply

[OpenReply](https://github.com/diwenne/openreply), yorum yazana otomatik DM gönderen, ManyChat benzeri açık kaynak bir araç. MIT lisanslı, TypeScript ile yazılmış (Next.js). Yazılım ücretsiz, kendi sunucunda çalıştırıyorsun: barındırma masrafı ayrı.

## Ne yapıyor?

- Gönderine anahtar kelime koyuyorsun. O kelimeyi yorum olarak yazan herkese Meta'nın resmi Instagram API'siyle özel DM gidiyor. Şifre istemiyor, tarayıcı otomasyonu yok.
- İstersen yorumun altına herkese açık bir cevap da yazıyor (birkaç cevap arasından rastgele).
- Linkler kendi kısa linkine (`/r/...`) çevriliyor, tıklama sayılarını panelde görüyorsun.
- Takip şartı: linki göndermeden önce takip edip etmediğine bakıyor. Takip etmeyene butonla tekrar soruyor.
- Aynı kelime DM'de yazılınca da çalışıyor. Birden fazla hesap ve ekip rolleri var.

## Gerekenler

- Instagram Business ya da Creator hesabı.
- Meta geliştirici hesabı ve bir Meta uygulaması (Instagram Login, webhook). Kendi hesabını uygulamada **Instagram tester** olarak ekleyip daveti Instagram'dan kabul etmen gerekiyor. Ya da ücretli Zernio bağlantısı (Meta uygulaması kurmadan).
- PostgreSQL, Redis ve sürekli açık duran bir worker (DM'leri o gönderiyor).
- Herkese açık bir HTTPS adresi (Vercel'in ücretsiz `*.vercel.app` adresi yetiyor).
- Giriş e-postaları için Resend hesabı ya da kendi SMTP sunucun (giriş sadece e-posta linkiyle).

## Kurulum yolu

Repo'nun önerdiği düzen: web uygulaması Vercel'de; worker, Postgres ve Redis Railway'de. Adım adım anlatım repo'da: [docs/setup.md](https://github.com/diwenne/openreply/blob/main/docs/setup.md).

Kendi bilgisayarında denemek için:

```bash
git clone https://github.com/diwenne/openreply.git
cd openreply
npm install
cp .env.example .env      # değerleri doldur
docker-compose up -d      # Postgres ve Redis
npm run db:generate
npm run db:migrate
npm run dev               # web uygulaması
npm run worker            # ikinci terminalde: DM'leri bu gönderiyor
```

Dikkat:
- Meta uygulaması Development modundayken gerçek yorum webhook'ları gelmiyor; uygulamayı yayınlaman (Publish) gerekiyor.
- Daha önce ManyChat bağladıysan, Meta Business Suite'te Ayarlar → Entegrasyonlar → Konuşma yönlendirme kısmından OpenReply'a konuşma kontrolünü ver. Yoksa butona basınca DM gitmiyor.
- `.env.example` içindeki `ENCRYPTION_KEY` örnek bir değer: mutlaka kendi rastgele anahtarını üret. `ALLOWED_EMAILS` ile girişi kendi e-postana kısıtla.

## Claude'a yapıştıracağın komut

Repo'yu klonla, klasörde Claude Code'u aç ve şunu yapıştır. Repo'nun kendi hazır komutu da var: [docs/setup.md → Set it up with an AI assistant](https://github.com/diwenne/openreply/blob/main/docs/setup.md#set-it-up-with-an-ai-assistant).

```text
Bu klasördeki OpenReply'ı kendi Instagram hesabım için kurmama yardım et.
Önce README.md ve docs/setup.md dosyalarını oku, sonra adım adım ilerle.
1. Bağlantı yolu olarak kendi Meta uygulamamı kullanacağım (Zernio değil).
2. Önce yerelde çalıştır: docker-compose ile Postgres ve Redis, .env dosyası,
   Prisma generate ve migrate, sonra web uygulaması ve worker.
3. Güçlü rastgele NEXTAUTH_SECRET, CRON_SECRET ve ENCRYPTION_KEY üret.
   ALLOWED_EMAILS'e sadece benim e-postamı yaz. Hiçbir sırrı ekrana yazdırma, commit'leme.
4. Yayına alma için Vercel (web) ve Railway (worker, Postgres, Redis) adımlarını
   sırayla anlat; hesap açma, ödeme ve Meta panelindeki tıklamaları bana bırak,
   bana sadece ne yapacağımı söyle.
5. Meta uygulaması için: OAuth redirect, webhook, Instagram tester daveti ve Publish
   adımlarını tek tek anlat ve her adımdan sonra benden onay iste.
6. Sonunda /api/health'in "ok" döndüğünü kontrol et ve TEST kelimesiyle
   başka bir hesaptan yorum atarak deneme planı ver.
```

Bu komutu biz uçtan uca denemedik. Meta panelindeki adımları (uygulama oluşturma, tester daveti, yayınlama) Claude senin yerine yapamaz, sen yapıyorsun.

## Bilmen gerekenler

- Takip şartı, takip etmeyen birine linki hiç göndermiyor; butona her basışta tekrar soruyor. (ManyChat akışımızda 2 kez sorduktan sonra link yine de gidiyor.)
- Repo'da Instagram girişiyle ilgili açık sorunlar var: [#64](https://github.com/diwenne/openreply/issues/64), [#103](https://github.com/diwenne/openreply/issues/103), [#104](https://github.com/diwenne/openreply/issues/104). Kurmadan önce bir göz at.
- Yorum yapan kişilerin bilgileri ve yorumları veritabanında saklanıyor; kendi sunucunda olduğu için sorumluluk sende.

## Emek kimin?

OpenReply'ı [Diwen Huang](https://github.com/diwenne) yazıyor ve yönetiyor (MIT). İlk hali [Anish Raj](https://github.com/im-anishraj)'ın instagram-comment-to-dm projesinden çatallanmış. Beğendiysen repo'ya bir yıldız bırak.

Bunun gibi gurme bilgiler için takip et 👉 [@mert.builds](https://www.instagram.com/mert.builds/)
