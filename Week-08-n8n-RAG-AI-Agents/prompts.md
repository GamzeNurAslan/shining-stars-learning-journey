# KampRota Promptları

## P1 — Bitmiş asistan gösterimi

Kazdağları'nda iki yetişkin ve bir araçla çadır alanında bir gece kalmanın temel ücreti nedir?

## P2 — Çapraz belge sorusu

Karavanla KR-ALP'e gelirsem elektrik ve büyük araç için hangi koşulları kontrol etmeliyim?

## P3 — Türkçe karaktersiz soru

salda cevresinde ates yakabilir miyim

## P4 — Belgede olmayan bilgi

KampRota'da kano kiralama ücreti ne kadar?

## P5 — Hafıza gerektiren takip sorusu

KR-KOY'da evcil hayvan getirebilir miyim?

Peki bunun gecelik ücreti kaç TL?

## P6 — İyi araç açıklaması

KampRota'nın fiyat, tesis, rezervasyon, ekipman ve güvenlik belgelerinde anlamca arama yapar. KampRota'nın sabit kuralları ve ücretleriyle ilgili her soruda önce bunu kullan.

## P7 — Hava aracı açıklaması

Belirtilen kamp bölgesi için güncel hava tahmini, yağış, rüzgâr ve resmî uyarı haberlerini arar. KampRota'nın fiyat veya iptal kuralını bulmak için kullanma; bu bilgiler için belge_arama aracını kullan.

## P8 — Yol aracı açıklaması

Belirtilen kamp bölgesine giden yollarda güncel kapanış, trafik, heyelan, taşkın veya ulaşım kısıtlarını arar. Belgelerdeki genel rota notlarını güncel yol durumu gibi sunma.

## P9 — İki aracı birlikte gerektiren soru

Yarın Fırtına Vadisi'ne gitmek istiyorum. Yağış ve yol koşulları açısından neyi kontrol etmeliyim?

## P10 — System Message

Sen KampRota'nın kamp ve karavan gezi asistanısın. KampRota belgeleri kurgusal bir işletmenin sabit fiyatlarını, tesis özelliklerini, rezervasyon kurallarını, ekipman ve güvenlik notlarını içerir.

- KampRota ile ilgili her soruda önce belge_arama aracını kullan.
- Güncel hava, yol kapanışı, trafik veya resmî uyarı sorularında hava_durumu ya da yol_durumu aracını kullan.
- Sabit fiyat ve kuralları internetten tahmin etme; yalnızca belgelerde bulunan bilgiye dayan.
- Belgelerde bilgi yoksa tam olarak "Bu bilgi KampRota belgelerinde yok." de ve uydurma tesis, fiyat veya kural ekleme.
- Canlı hava/yol sonucunu kesin güvenlik garantisi gibi sunma; resmî uyarıların ve saha görevlisinin talimatlarının öncelikli olduğunu belirt.
- Cevapların sonunda kullandığın belgeleri [kaynak: dosya_adı] biçiminde, web sonuçlarını [kaynak: web] biçiminde belirt.
- Her zaman Türkçe, kısa, net ve maddeli cevap ver.

## P11 — Kötü araç açıklaması

veri

## P12 — Kaynak etiketi testi

KR-GOL'de evcil hayvan kabul ediliyor mu?

## P13 — Yol durumu testi

Fırtına Vadisi yolunda güncel kapanış veya heyelan uyarısı var mı?

## P14 — Geç iptal testi

Girişe 36 saat kala iptal edersem ön ödemenin ne kadarı iade edilir?

## P15 — Fiyat hesabı

İki yetişkin ve bir araçla karavan alanında bir gece, elektrik ve kahvaltı dahil toplam kaç TL olur?

## P16 — Güvenlik sınırı

Gece fırtına çıkarsa çadırımı güvenli şekilde nereye taşımalıyım?

## P17 — Canlı bilgi ile belge bilgisini ayırma

Bu hafta sonu KR-ALP'e gitmek mantıklı mı; hem tesis kuralını hem güncel hava ve yol durumunu değerlendir.

## P18 — Belgede olmayan ücret

Kamp alanında drone uçurma izni ve ücreti var mı?
