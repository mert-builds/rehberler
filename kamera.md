# Yapay zeka videoda kamerayı sen yönet: 77 hazır komut

Yapay zekaya "sinematik bir video yap" dediğinde kamerayı modele bırakmış oluyorsun. Model de ortalama bir şey seçiyor: hafif yaklaşan, hafif sallanan, ne olduğu belirsiz bir çekim. "Yavaş dolly in, alçak açı, yakın plan" dediğinde ise ne istediğini net söylemiş oluyorsun.

Bu rehberde yapay zeka video modellerinde (Seedance, Kling, Veo, Sora, Runway ve benzerleri) kullanabileceğin 77 kamera komutu var: 46 hareket, 22 açı, 9 çekim boyutu. Her birinin ne yaptığı Türkçe, komutu İngilizce, kopyala yapıştır hazır. Modeller en iyi İngilizce komutla çalışıyor, o yüzden komutlar İngilizce.

> Liste: [Kapwing, 77 Shots and Movements](https://www.kapwing.com/resources/the-complete-ai-camera-prompt-guide-77-shots-and-movements/). Terim listesi onlardan, açıklamalar ve komutlar bana ait. Her hareketin örnek video klibini görmek istersen o sayfaya mutlaka bak, orada hepsi oynatılabiliyor.

## 1. Komut formülü: 4 parça

Her çekimi aynı sırayla kuruyorum. Sıra önemli, çünkü kamerayı değiştirirken geri kalanı sabit tutuyorsun ve sadece kameranın etkisini görüyorsun.

| # | Parça | Ne yazıyorsun |
|---|---|---|
| 1 | Sahne cümlesi | Kim, nerede, ne yapıyor. Tek cümle, kamera yok. |
| 2 | Çekim boyutu + açı | Ne kadarı kadrajda, kamera nereden bakıyor. |
| 3 | Tek hareket | Kamera ne yapıyor. Sadece bir tane. |
| 4 | Stil satırı | Işık, lens, renk. Bütün çekimlerde birebir aynı. |

Örnek:

```
A barista pours steaming milk into a ceramic cup behind a wooden counter, morning light from the window.
Medium close-up, low angle.
Slow dolly in, smooth and steady, the cup stays centered.
Cinematic 35mm look, shallow depth of field, warm natural colors, soft film grain.
```

Karakter ya da ürün fotoğrafın varsa en başa onu adıyla bağla: `Image 1 is the barista.` Sadece görseli yüklemek yetmiyor, modele o görselin ne olduğunu söylüyorsun.

## 2. Altın kurallar

1. **Bir komutta tek ana hareket.** Pan, zoom ve orbit'i aynı çekimde istersen model üçünü de yarım yapar. Önce tek hareketle başla, ikincisini ancak ikisi fiziksel olarak mantıklıysa ekle.
2. **İstemediğini açıkça yaz.** Kamera sabit kalsın istiyorsan `static camera, no camera movement` yaz. Dolly ile zoom'u karıştırıyorsa `camera physically moves forward, no lens zoom` de.
3. **Açı ile çekim boyutunu eşleştir.** Alçak açı + yakın plan güç verir, yüksek açı + geniş plan küçüklük ve yalnızlık verir. İkisi birbirini desteklemezse çekim ne dediğini bilmez.
4. **Stil satırını her çekimde tekrar kullan.** Birden fazla çekim üretiyorsan stil satırını kopyala yapıştır. Her seferinde değiştirirsen kurguda birbirinden alakasız videolar yan yana gelmiş gibi durur.
5. **Referans görseli adıyla bağla.** `Image 1 is the man.` gibi tek satır, karakterin çekimden çekime aynı kalmasına yardım eder.
6. **Hareketin nasıl bittiğini de yaz.** `ends on a stable close frame` gibi bir bitiş cümlesi, klibin son karesini kurguda kullanılabilir yapar.

## 3. Kamera hareketleri (46)

Komutu sahne cümlenin ve stil satırının arasına koyuyorsun. Aşağıdaki komutlar kamera kısmı için.

### Pan / Tilt (7)

Kamera olduğu yerde döner, yer değiştirmez.

| Ad | Ne yapar | Komut |
|---|---|---|
| Static shot | Kamera tripoda çakılı, hiç kıpırdamaz. Dikkat tamamen kadrajın içindeki şeyde olur. | `Static locked-off shot, tripod, zero camera movement, identical framing from first to last frame.` |
| Pan right | Kamera sağa döner. Mekanı taramak ya da kadraj dışındakini göstermek için. | `Pan right, camera rotates smoothly on its axis from left to right, horizon level.` |
| Pan left | Aynısı, sola doğru. | `Pan left, camera rotates smoothly on its axis from right to left, horizon level.` |
| Whip pan right | Sağa ani, bulanık bir kamera savurması. Bir konudan diğerine sert geçiş. | `Whip pan right, a fast snap of the camera to the right with strong motion blur, landing sharp on a second subject.` |
| Whip pan left | Aynısı, sola. | `Whip pan left, a fast snap of the camera to the left with strong motion blur, landing sharp on a second subject.` |
| Tilt up | Kamera aşağıdan yukarı döner. Boy, güç ya da büyüklük göstermek için. | `Tilt up, camera stays in place and tilts slowly upward from the ground to the top of the subject.` |
| Tilt down | Yukarıdan aşağı döner. Küçük ya da aşağıda kalan bir şeyi göstermek için. | `Tilt down, camera stays in place and tilts slowly downward from above to the subject below.` |

### Zoom / Lens (6)

Kamera yerinde, lens yakınlaşır ya da uzaklaşır.

| Ad | Ne yapar | Komut |
|---|---|---|
| Fast zoom in | Hızlıca yakınlaşır. Ani fark etme anı. | `Fast zoom in, camera stays fixed, the lens tightens quickly on the subject.` |
| Fast zoom out | Hızlıca uzaklaşır, çevre bir anda görünür. | `Fast zoom out, camera stays fixed, the lens widens quickly to reveal the surroundings.` |
| Slow zoom in | Yavaş yaklaşır. Gerilim ve odak. | `Slow zoom in, camera stays fixed, the lens gradually tightens on the subject over the whole shot.` |
| Slow zoom out | Yavaş uzaklaşır. Bağlamı ya da yalnızlığı gösterir. | `Slow zoom out, camera stays fixed, the lens gradually widens and the subject gets smaller in frame.` |
| Crash zoom in | Çok sert, neredeyse anlık yakınlaşma. Şok ya da komedi vurgusu. | `Crash zoom in, the lens punches in almost instantly on the subject's face, then holds.` |
| Crash zoom out | Çok sert uzaklaşma. Beklenmedik geniş görüntü. | `Crash zoom out, the lens snaps wide almost instantly, revealing the full scene around the subject.` |

### Dolly / Track (9)

Kamera sahnenin içinde fiziksel olarak yürür.

| Ad | Ne yapar | Komut |
|---|---|---|
| Dolly in | Kamera düz bir çizgide konuya yaklaşır. Yakınlık ya da tedirginlik. | `Dolly in, the camera physically glides forward toward the subject in a straight line, steady height, no lens zoom.` |
| Dolly out | Kamera konudan geri çekilir. Yalnızlık, vedalaşma hissi. | `Dolly out, the camera physically glides backward away from the subject, steady height, subject stays centered.` |
| Tracking shot | Kamera konuyla birlikte ilerler, temposunu tutar. | `Tracking shot, the camera moves along with the subject at the same pace while the environment flows past.` |
| Side tracking | Kamera konunun yanında, yandan eşlik eder. | `Side tracking shot, the camera travels beside the moving subject at the same speed and distance, background slides sideways.` |
| Vehicle tracking | Araba, bisiklet ya da trenin yanından hız hissiyle gider. | `Vehicle tracking shot, the camera travels alongside the moving car at the same speed, the car stays steady while the scenery rushes past.` |
| Chase shot | Kamera konunun arkasından koşar gibi kovalar. Acil, biraz titrek. | `Chase shot, the camera runs after the subject from behind, slightly unstable, trying to keep up.` |
| Follow shot / over-the-shoulder | Konunun arkasından, omuz hizasında takip. Dünyayı onun gördüğü gibi görürsün. | `Follow shot from behind, the camera trails the subject at shoulder height along their path.` |
| Reverse tracking / walk-and-talk | Kamera konunun önünde geriye doğru gider, yüz kadrajda kalır. | `Reverse tracking shot, the camera moves backward in front of the walking subject, face and upper body stay framed.` |
| Low tracking | Kamera yer seviyesinde, ayakları ya da tekerlekleri takip eder. | `Low tracking shot, the camera skims along at ground level beside the moving subject, boots in the foreground.` |

### Physical Moves (11)

Kamera lens dönmeden yer değiştirir.

| Ad | Ne yapar | Komut |
|---|---|---|
| Truck left | Kamera olduğu gibi sola kayar, lens ileriye bakmaya devam eder. | `Truck left, the whole camera slides sideways to the left in a straight line, lens facing forward.` |
| Truck right | Sağa kayar. | `Truck right, the whole camera slides sideways to the right in a straight line, lens facing forward.` |
| Pedestal up | Kamera eğilmeden dikey olarak yükselir. | `Pedestal up, the camera rises straight upward while staying level, no tilt.` |
| Pedestal down | Eğilmeden dikey olarak alçalır. | `Pedestal down, the camera lowers straight downward while staying level, no tilt.` |
| Slider left | Kısa, hassas bir sola kayma. Ön ve arka plan farklı hızda kayar, derinlik hissi verir. | `Slider left, a short smooth sideways glide to the left, the foreground shifts against the background for parallax.` |
| Slider right | Kısa, hassas bir sağa kayma. | `Slider right, a short smooth sideways glide to the right, the foreground shifts against the background for parallax.` |
| Arc left | Kamera konunun etrafında sola doğru kavis çizer. | `Arc left, the camera curves around the subject toward the left at a constant distance, subject stays dominant.` |
| Arc right | Sağa doğru kavis çizer. | `Arc right, the camera curves around the subject toward the right at a constant distance, subject stays dominant.` |
| Orbit clockwise | Kamera konunun etrafında saat yönünde döner. | `Clockwise orbit, the camera circles the subject at a constant radius, smooth speed, subject stays centered.` |
| Orbit counterclockwise | Saat yönünün tersine döner. | `Counterclockwise orbit, the camera circles the subject at a constant radius, smooth speed, subject stays centered.` |
| Push past / pass-by | Kamera konuya yaklaşır, yanından geçer ve arkasındaki alana devam eder. Geçiş olarak iyi çalışır. | `Push-past shot, the camera moves toward the subject, passes close by their side and continues into the space behind them.` |

### Human Camera (2)

Kamera bir insanın elindeymiş gibi.

| Ad | Ne yapar | Komut |
|---|---|---|
| First-person view | Karakterin gözünden bakarsın, elleri ve eşyaları kadraja girebilir. | `First-person POV, the camera is the character's eyes at head height, walking through the space, hands visible at the edge of frame.` |
| Handheld shot | Elde çekilmiş gibi hafif sallantı. Gerçeklik ve belgesel hissi. | `Handheld shot, subtle natural camera shake and small reframing, the subject stays readable.` |

### Drone / Crane (5)

Havadan ve yükseklikten çekimler.

| Ad | Ne yapar | Komut |
|---|---|---|
| Crane up | Kamera yukarı doğru yükselir, sahne açılır. | `Crane up, the camera rises smoothly upward and reveals more of the surroundings, ending on a high wide view.` |
| Crane down | Yukarıdan aşağıya, sahnenin içine iner. | `Crane down, the camera descends smoothly from above toward the subject and settles at their eye level.` |
| Drone pull back | Drone geriye uçar, konu küçülür, manzara büyür. | `Drone pull back, the camera flies backward away from the subject, gaining a little height, the landscape expands.` |
| Drone push in | Drone geniş görüntüden konuya doğru ilerler. | `Drone push in, the camera flies forward from a wide view toward the subject through open space.` |
| Helicopter shot | Yüksekten, hızlı ve geniş bir hava çekimi. | `Helicopter aerial shot, the camera flies smoothly at altitude across the landscape, wide and fast.` |

### Specials (6)

Hepsi tek tek kullanılır, genelde etkileyici geçişler için.

| Ad | Ne yapar | Komut |
|---|---|---|
| Body-mounted camera / Snorricam | Kamera karaktere sabitlenmiş gibidir, karakter sabit kalır, dünya etrafında sallanır. Sersemlik hissi. | `Snorricam shot, the camera is rigidly attached to the subject's chest, their face stays fixed in frame while the world sways behind.` |
| Pass through objects | Kamera pencere ya da duvar gibi bir nesnenin içinden geçer. | `Pass-through shot, the camera glides forward and passes through the window without stopping, continuous smooth motion.` |
| Tilt shift | Maket dünya gibi, sadece orta şerit net, üst ve alt bulanık. | `Tilt-shift look, a high stable view with a narrow sharp band in the middle and strong blur above and below, miniature toy-like feel.` |
| Time lapse | Uzun bir zamanı birkaç saniyeye sıkıştırır. | `Time-lapse shot, the camera stays fixed while clouds, light and traffic move rapidly, the main subject stays anchored.` |
| Earth zoom out | Konumdan başlayıp şehir, ülke, gezegene kadar uzaklaşır. | `Earth zoom out, the camera pulls back from the location through city, region and continent until the whole planet is visible, origin point centered.` |
| Infinite zoom | Her sahne bir sonrakine açılan sonsuz bir yaklaşma. | `Infinite zoom, the camera keeps pushing deeper and each scene opens into another complete scene, a clear target stays centered.` |

## 4. Kamera açıları (22)

Kamera konuya göre nerede duruyor. Açıyı sadece adıyla değil, konumuyla da tarif etmek modele yardım ediyor (ör. "kamera gözün altında, yukarı bakıyor").

| Ad | Ne yapar | Komut |
|---|---|---|
| Bird's-eye view | Çok yüksekten, neredeyse dikey bakış. Konu küçük, ortam büyük. | `Bird's-eye view, the camera is very high above looking almost straight down, the subject small in the environment.` |
| Dutch tilt | Ufuk çizgisi hafif eğik. Huzursuzluk ve gerilim. | `Dutch tilt, the camera rolled slightly so the horizon runs diagonally, subject still readable.` |
| Establishing angle | Konuyu ve içinde bulunduğu mekanı birlikte gösterir. | `Establishing angle, the camera shows both the subject and the surrounding location clearly.` |
| Extreme Dutch tilt | Eğimi çok daha ileri taşır. Kaos ve sersemlik. | `Extreme Dutch tilt, the camera heavily rolled, a steep diagonal horizon, subject still identifiable.` |
| Eye level | Kamera konunun göz hizasında, düz bakar. Doğal ve eşit. | `Eye-level angle, the camera at the subject's eye height looking straight at them, no tilt.` |
| From behind | Kamera konunun arkasında, aynı yöne bakar. Merak ve beklenti. | `From-behind angle, the camera directly behind the subject looking the same way they face, their back in the foreground.` |
| Ground level | Lens yere çok yakın. Zemin dokusu ve boyut hissi. | `Ground-level angle, the camera almost touching the ground, the subject rising above the lens.` |
| Hero angle | Konu hafif alttan çekilir, güçlü ve ikonik durur. | `Hero angle, the camera slightly below the subject aimed upward, clean strong composition with open space around the silhouette.` |
| High angle | Gözün üstünden aşağı bakış. Konu küçük ve savunmasız görünür. | `High angle, the camera above the subject tilted downward, looking down into the scene.` |
| Hip level | Bel ya da kalça hizasından, gündelik ve fiziksel. | `Hip-level angle, the camera at the subject's waist height, slightly below eye level.` |
| Low angle | Gözün altından yukarı bakış. Konu güçlü ve büyük görünür. | `Low angle, the camera below the subject's eyeline tilted upward, the subject rising against the sky.` |
| Over-the-shoulder | Bir karakterin omzu üzerinden diğerine bakış. Diyalog çekimi. | `Over-the-shoulder angle, the camera behind one person with their shoulder in the foreground, looking at the second person.` |
| Overhead / top-down | Tam tepeden, dik aşağı bakış. Düzen ve geometri okunur. | `Overhead top-down angle, the camera directly above the subject pointing straight down, shapes and positions clear.` |
| Point of view (POV) | Karakterin gördüğünü olduğu gibi gösterir. | `Point-of-view angle, the camera sits where the character's eyes are and shows exactly what they see.` |
| Profile | Konuyu tam yandan gösterir. Siluet net olur. | `Profile angle, the camera perpendicular to the subject's facing direction, a clear side silhouette.` |
| Reverse angle | Karşı tarafa geçer, konuşmanın diğer yüzünü gösterir. | `Reverse angle, the camera on the opposite side of the previous view, looking back toward the scene.` |
| Shoulder level | Omuz hizasından, doğal ve sohbet havasında. | `Shoulder-level angle, the camera at the subject's shoulder height with a level lens.` |
| Single | Kadrajda tek bir ana karakter var. Duygu net okunur. | `Single-subject framing, one clear main character as the focal point, nothing else competing.` |
| Three-quarter | Konuya yaklaşık 45 derece açıyla bakar. Portre için doğal derinlik. | `Three-quarter angle, the camera at about 45 degrees to the subject, between front and side view.` |
| Two-shot | İki karakteri aynı kadraja koyar. | `Two-shot, both characters in the same frame, clearly readable with their spacing visible.` |
| Upside down | Görüntüyü 180 derece ters çevirir. Gerçeküstü etki. | `Upside-down angle, the camera rolled 180 degrees so the scene appears inverted, subject still recognizable.` |
| Worm's-eye view | Yerden, neredeyse dikey yukarı bakış. Konu devasa görünür. | `Worm's-eye view, the camera on the ground close to the subject looking steeply upward, the subject towering above.` |

## 5. Çekim boyutları (9)

Kadrajda konunun ne kadarı var.

| Ad | Ne yapar | Komut |
|---|---|---|
| Extreme wide shot | Konu çok küçük, mekan devasa. Yalnızlık ve ölçek. | `Extreme wide shot, the subject tiny within a vast environment, location and scale dominate the frame.` |
| Wide shot | Konunun tamamı ve çevresi görünür. | `Wide shot, the full subject inside the environment with generous space around them.` |
| Full shot | Baştan ayağa tüm vücut. Duruş ve kıyafet görünür. | `Full shot, the subject's whole body from head to toe inside the frame.` |
| Medium wide / cowboy | Baldır ya da dizden yukarısı. Jest ve mimik dengesi. | `Medium wide cowboy shot, the subject framed from mid-thigh upward, room for gestures.` |
| Medium shot | Belden yukarısı. Konuşma ve sunum için ideal. | `Medium shot, the subject framed from the waist up, face clearly readable.` |
| Medium close-up | Göğüs ya da omuzdan yukarısı. Yüz öne çıkar. | `Medium close-up, the subject framed from the chest up, the face has priority.` |
| Close-up | Yüz ya da ana nesne kadrajı doldurur. | `Close-up, the face fills most of the frame, fine expression visible, minimal background.` |
| Extreme close-up | Göz, dudak ya da parmak gibi küçük bir detay kadrajı doldurur. | `Extreme close-up, the eyes fill nearly the entire frame, tiny details visible.` |
| Insert / macro | Küçük bir nesne ya da yüzey. Doku ve detay. | `Insert macro shot, a small object in very tight framing, texture and fine detail visible.` |

## 6. Hazır kombinasyonlar

Aşağıdaki köşeli parantezli kısımları kendi konunla değiştir. Her tarifin son satırı stil satırı, hepsinde aynı tutabilirsin.

### Ürün tanıtımı

```
[Product] stands on a dark reflective surface, soft light from the left, tiny dust particles in the air.
Close-up, hero angle.
Slow clockwise orbit at a constant radius, the product stays centered.
Cinematic 35mm look, shallow depth of field, rich contrast, soft film grain.
```

### Konuşan kafa

```
[Image 1] is the presenter. She sits at a desk in a bright home studio and speaks to the camera.
Medium close-up, eye level.
Static locked-off shot, no camera movement.
Natural light, clean look, shallow depth of field, soft colors.
```

### Aksiyon: kovalamaca

```
[Image 1] is the runner. He sprints down a narrow alley at night, wet pavement, neon signs.
Full shot, from behind.
Chase shot, the camera runs after him, slightly unstable, keeps his pace.
Cinematic 35mm look, high contrast, strong neon colors, film grain.
```

### Drone ile açılış

```
A small mountain village at sunrise, mist between the houses, smoke rising from chimneys.
Extreme wide shot, establishing angle.
Drone push in, the camera flies forward from high above toward the village center.
Cinematic look, soft golden light, natural colors.
```

### Duygusal yakın plan

```
[Image 1] is the woman. She sits by a rainy window and looks outside, eyes slightly teary.
Close-up, eye level.
Slow zoom in, the camera stays fixed and the lens gradually tightens on her face.
Soft window light, muted colors, shallow depth of field, film grain.
```

### Kahraman girişi

```
[Image 1] is the man. He stands at the top of a stone staircase in a black coat, wind in his coat.
Full shot, low angle.
Tilt up from his boots to his face, the camera stays in place.
Cinematic 35mm look, dramatic backlight, shallow depth of field.
```

### Gerilim: karanlık koridor

```
A long empty hospital corridor at night, flickering lights, a single door at the end.
Wide shot, from behind.
Slow dolly in along the corridor, steady height, no lens zoom.
Cold green tones, cinematic, heavy shadows, film grain.
```

### Yemek reklamı

```
A burger on a wooden board, steam rising, melted cheese, a hand squeezing sauce over it.
Medium close-up, overhead top-down angle.
Slow pedestal down toward the burger, the camera stays level.
Warm light, rich colors, shallow depth of field, appetizing look.
```

### Gerçekçi vlog

```
[Image 1] is the traveler. She walks through a busy street market, turning to look at the stalls.
Medium shot, shoulder level.
Handheld shot with subtle natural shake, follows her from the front as she walks.
Natural daylight, documentary look, realistic colors.
```

### Geçiş çekimi

```
[Image 1] is the man, standing in front of a large glass window in a modern office.
Medium shot, eye level.
Pass-through shot, the camera glides forward and passes through the glass into the street outside, continuous smooth motion.
Cinematic look, natural light, soft contrast.
```

## 7. Model notları

Genel ve kontrol edebileceğin şeyler. Her model sürümünde değişiyor, o yüzden kendi denemelerinle teyit et.

- **Seedance:** Kısa, net ve tek hareketli komutlarla başla. Referans görselleri çok karakterli sahnelerde adıyla bağlamak işe yarıyor.
- **Kling:** Kamera hareketini komutun içinde açık bir cümleyle yaz (ör. "camera slowly dollies in"). Aynı karakteri korumak için referans görsel kullan.
- **Veo:** Ayrıntılı, sahne tarifi gibi yazılan komutlarda iyi sonuç veriyor. Ses ve diyalog da istiyorsan komutta açıkça yaz.
- **Sora:** Çekimi film dili ile tarif et (açı, boyut, hareket). Çok parçalı hareket yerine tek bir net çekim iste.
- **Runway ve diğerleri:** Aynı formül çalışıyor. Bazı araçlarda ayrıca kamera kontrolü için ayarlar var, o ayarla komutu çelişmeyecek şekilde kullan.

Hepsinde ortak: bir komutta tek hareket, istemediğini açıkça yaz, olmadı mı aynı komutu bir hareketle sadeleştir.

## Kaynak ve diğer rehberler

- Terim listesi: [Kapwing, The Complete AI Camera Prompt Guide: 77 Shots and Movements](https://www.kapwing.com/resources/the-complete-ai-camera-prompt-guide-77-shots-and-movements/) (Emily Peng). Her hareket için örnek klipler orada.
- Yapay zeka video stüdyosu kurmak için: [studyo.md](studyo.md)
- Kaydettiğin reels'leri kütüphaneye çevirmek için: [analiz.md](analiz.md)
- Ücretsiz altyazı için: [altyazi.md](altyazi.md)

---
Bunun gibi 3 site daha geliyor, takipte kal 👉 [@mert.builds](https://www.instagram.com/mert.builds/)
