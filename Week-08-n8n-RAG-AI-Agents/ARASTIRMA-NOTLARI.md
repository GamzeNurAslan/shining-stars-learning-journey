# Araştırma Notları

Bu proje iki katmanı ayırır: eğitim için sabit ve kurgusal KampRota belgeleri; gerçek dünyada güncellenmesi gereken hava ve yol verileri.

## Canlı veri kaynakları

- Meteoroloji Genel Müdürlüğü MeteoUYARI sistemi meteorolojik uyarıları renk kodlarıyla yayımlar. Sarı potansiyel tehlike, turuncu tehlikeli, kırmızı çok tehlikeli durumları belirtir: https://www.mgm.gov.tr/meteouyari/meteouyari-nedir.aspx
- Karayolları Genel Müdürlüğü kapalı yollar listesini yol adı, kapanma nedeni, kesim ve güncelleme bilgileriyle yayımlar: https://www.kgm.gov.tr/Sayfalar/KGM/SiteTr/YolDanisma/TrafigeKapaliYollar.aspx?hl=tr-TR
- KGM ayrıca çalışma yapılan yollar ve güzergâh analizi sayfalarını sunar: https://www.kgm.gov.tr/Sayfalar/KGM/SiteTr/YolDanisma/CalismaYapilanYollar.aspx
- Acil durumda Türkiye'de aranacak numara 112'dir; proje asistanı saha müdahalesi veya tahliye kararı vermez: https://www.afad.gov.tr/

## Tasarım kararı

MGM ve KGM sayfaları doğrudan bilgi bankasına gömülmedi. Çünkü hava ve yol durumu hızla değişir. Agent bu kaynakları `hava_durumu` ve `yol_durumu` araçlarıyla sorgular; cevapta güncel web bilgisini `[kaynak: web]` etiketiyle ayırır.

KampRota belgeleri kurgusaldır. Gerçek bir kamp alanı, fiyat veya güvenlik kuralı gibi sunulmamalıdır. Gerçek kullanıma geçerken tesis sahibinin güncel belgeleri, resmî uyarılar ve yerel idare duyuruları ayrıca doğrulanmalıdır.

## Testte beklenen davranış

1. “Yarın yol açık mı?” sorusunda `yol_durumu` çağrılır.
2. “KR-ALP'te karavan kabul edilir mi?” sorusunda `belge_arama` çağrılır.
3. “Yağmur yağarsa ücretsiz iptal mi?” sorusunda sabit politika belgeden, güncel uyarı web'den alınır.
4. “Fırtınada çadırımı nereye taşıyayım?” sorusunda asistan kesin saha talimatı vermez; görevliye, resmî uyarılara ve acil durumda 112'ye yönlendirir.
