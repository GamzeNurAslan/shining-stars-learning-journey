

# 🗺️ Week 07 — GIS Spatial Analysis with QGIS

Bu hafta coğrafi veriler, açık kaynak CBS araçları ve konuma dayalı analiz üzerine çalıştım.

Uygulamada Elazığ Eğitim ve Araştırma Hastanesi merkez alınarak 1 km çevresindeki optikçiler analiz edildi. Çalışmanın sonucunda hastanenin 1 km çevresinde **6 optikçi** bulundu.

https://github.com/GamzeNurAslan/shining-stars-learning-journey/blob/main/Week-07-GIS-Spatial-Analysis-QGIS/Ekran%20g%C3%B6r%C3%BCnt%C3%BCs%C3%BC%202026-09-27%20152012.png

---

## 🎯 Projenin Amacı

Hastane çevresindeki optikçileri harita üzerinde göstermek ve belirlenen 1 km yarıçaplı alan içinde kaç optikçi bulunduğunu hesaplamak.

## 🧭 Uygulama Akışı

```text
Hastane noktasını oluştur
          ↓
Hastanenin çevresinde 1 km tampon oluştur
          ↓
Optikçi noktalarını haritaya ekle
          ↓
Tampon alanındaki noktaları say
          ↓
Sonuç: 6 optikçi
```

---

## 🛠️ Kullanılan Araçlar

- QGIS
- OpenStreetMap
- QuickOSM
- GeoPackage
- EPSG:32637 — WGS 84 / UTM zone 37N

## ✅ Uygulamada Yapılanlar

- OpenStreetMap altlığı QGIS'e eklendi.
- Elazığ Eğitim ve Araştırma Hastanesi nokta olarak oluşturuldu.
- QuickOSM ile optikçi verisi sorgulandı.
- OpenStreetMap'te sonuç bulunamadığı için kamuya açık işletme adresleri kullanılarak 6 optikçi manuel olarak sayısallaştırıldı.
- Hastane katmanı metre cinsinden analiz yapabilmek için EPSG:32637 koordinat sistemine dönüştürüldü.
- Hastane çevresinde 1000 metrelik tampon alan oluşturuldu.
- Tampon alanındaki optikçi noktaları sayıldı.

## 📊 Sonuç

Elazığ Eğitim ve Araştırma Hastanesi'nin 1 km çevresinde **6 optikçi** bulunmaktadır.

## 📁 Dosyalar

- `elazig_optik_projesi.qgz` — QGIS proje dosyası
- `elazig_optik_projesi.gpkg` — hastane, optikçi, tampon ve sonuç katmanları
- `aciklama.md` — yöntem, kaynaklar ve ayrıntılı açıklama

## ✨ Genel Değerlendirme

Bu çalışma, bir konum etrafında belirli bir mesafe oluşturarak o alan içindeki işletmelerin sayılmasını gösteren temel bir CBS mekânsal analiz örneğidir. QGIS kullanılarak veri oluşturma, koordinat sistemi dönüştürme, tampon analizi ve nokta sayımı uygulandı.
