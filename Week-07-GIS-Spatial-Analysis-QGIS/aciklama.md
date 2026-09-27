# Elazığ Eğitim ve Araştırma Hastanesi Çevresindeki Optikçiler

## Araştırma sorusu

Elazığ Eğitim ve Araştırma Hastanesi'nin 1 km çevresinde kaç optikçi vardır?

## Kullanılan araçlar

- QGIS 3.44
- OpenStreetMap altlığı
- QuickOSM eklentisi
- GeoPackage veri formatı
- ChatGPT (iş akışını öğrenmek ve hata çözmek için)

## Veri ve yöntem

1. QGIS'e OpenStreetMap altlığı eklendi.
2. Hastane için `hastane` adlı nokta katmanı oluşturuldu ve Elazığ Eğitim ve Araştırma Hastanesi noktası eklendi.
3. QuickOSM ile `shop=optician` ve optik/gözlük adlarını arayan sorgular çalıştırıldı. Ancak OpenStreetMap sunucusundan bu alan için sonuç dönmedi.
4. Bu nedenle kamuya açık işletme listelerindeki adresler kullanılarak altı optikçi QGIS'te `optikciler` nokta katmanına manuel olarak eklendi:
   - Gözde Optik
   - Ercömert Optik
   - Işık Optik
   - Yasin Optik
   - Opsel Optik
   - Retina Optik
5. Hastane katmanı mesafe hesabı için EPSG:32637 (WGS 84 / UTM zone 37N) koordinat sistemine yeniden projelendirildi.
6. Hastane noktasının çevresinde 1000 metre yarıçaplı tampon oluşturuldu.
7. `Poligondaki noktaları hesapla` aracı ile tampon içindeki optikçi noktaları sayıldı.

## Sonuç

Hastanenin 1 km çevresinde **6 optikçi** bulunmaktadır.

Sonuç GeoPackage dosyası: `elazig_optik_projesi.gpkg`

GeoPackage içindeki temel katmanlar:

- `hastane`
- `optikciler`
- `sonuc_1km_optikci_sayisi`

## Veri sınırlılığı

QuickOSM sorgusu sonuç vermediği için optikçi noktaları kamuya açık adres bilgileri kullanılarak manuel olarak sayısallaştırılmıştır. Bu nedenle sonuç, adres kaynaklarının güncelliğine ve manuel nokta yerleştirmesine bağlıdır. Haritada OpenStreetMap altlığı kullanıldığı için harita üzerinde `© OpenStreetMap contributors` gösterilmelidir.

## Kullanılan kaynaklar

- https://yellowpages.com.tr/gozlukculer-ve-kontakt-lensler-merkez-elazig-c
- https://tavsiyemiz.com/hizmet/gozde-optik-elazig-68063d7a3efbc
- https://enyakinnerde.com/gozlukculer-optik/632119-ercomert-optik

## Yapay zekâ kullanımı

ChatGPT; ödev yönergesini anlamak, QGIS araçlarının kullanımını öğrenmek, QuickOSM sorgusunu düzenlemek ve hata mesajlarını yorumlamak amacıyla kullanılmıştır.
