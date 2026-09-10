# 🚚 Week 5 — Data Engineering & Apache Airflow

Bu hafta odağım **Veri Mühendisliği**, **ETL pipeline mantığı**, **veri kalitesi**, **idempotency** ve **Apache Airflow’un veri süreçlerindeki rolü** oldu.

Amaç yalnızca bir CSV dosyasını temizlemek değil; veriyi üretmekten başlayıp PostgreSQL’e yüklemeye kadar uzanan, tekrar çalıştırıldığında bozulmayan ve hatalı kayıtları kontrol altında tutan küçük bir **data pipeline** oluşturmaktı. 🚀

---

## 🧩 Proje Akışı

```text
🎲 Faker
   ↓
📄 Ham Veri
   ↓
🔍 Veri Keşfi
   ↓
🧹 Veri Temizleme
   ├── ✅ Temiz Veri
   └── 🚨 Karantina
   ↓
🐘 PostgreSQL
   ↓
🔁 Idempotent Load
   ↓
🧪 Data Quality Check
```

---

## 🎲 Sentetik Veri Üretimi

Gerçek kullanıcı verisi yerine **Faker (`tr_TR`)** kullanarak sentetik kargo verileri oluşturdum.

Veri setinde:

* 📦 Gönderi ID
* 🏢 Şube kodu
* 📍 Alıcı şehri
* ⚖️ Ağırlık
* 🚚 Gönderi durumu
* 📅 Kabul ve teslim tarihleri

bulunuyor.

Pipeline’ı test edebilmek için bilinçli olarak duplicate kayıtlar, eksik değerler, negatif ağırlıklar, hatalı tarihler ve farklı İstanbul yazımları ekledim.

```text
Toplam kayıt : 5050
Duplicate    : 50
Eksik şehir : 26
Eksik ağırlık: 12
```

---

## 🔍 Veri Keşfi ve Temizleme

Pandas ile veri setinin boyutunu, veri tiplerini, eksik değerleri, tekrar eden kayıtları ve sayısal dağılımları inceledim.

Bu aşamada örneğin:

```text
Minimum ağırlık: -3.5 kg
```

gibi mantıksal olarak hatalı değerler tespit edildi.

Duplicate kayıtlar temizlendikten sonra:

```text
5050 → 5000
```

kayıt kaldı.

Hatalı kayıtları tamamen silmek yerine ayrı bir **karantina dosyasına** aktardım.

| Durum                   |  Kayıt |
| ----------------------- | -----: |
| ⚖️ Geçersiz ağırlık     |     40 |
| 📍 Eksik şehir          |     25 |
| 📅 Hatalı teslim tarihi |     20 |
| ⚖️ Eksik ağırlık        |     12 |
| **Toplam**              | **97** |

Sonuçta:

```text
✅ Temiz veri : 4903
🚨 Karantina : 97
```

---

## 🇹🇷 Türkçe Karakter Standardizasyonu

Veri temizleme sırasında şu değerlerin aynı şehri ifade ettiğini ele aldım:

```text
ISTANBUL
İSTANBUL
Istanbul
istanbul
İstanbul
```

Bu değerleri tek bir formatta:

```text
İstanbul
```

olarak standartlaştırdım.

Bu bölüm özellikle Türkçe `I / İ / i` karakterlerinin veri temizleme süreçlerinde dikkatli ele alınması gerektiğini gösterdi.

---

## 🐳 Docker & PostgreSQL

PostgreSQL’i bilgisayara doğrudan kurmak yerine **Docker container** içerisinde çalıştırdım.

Bu süreçte:

* Image
* Container
* Port Mapping
* Volume

kavramlarını uygulamalı olarak kullandım.

Temiz veriyi **SQLAlchemy** aracılığıyla PostgreSQL’e aktardım.

```text
CSV kayıt sayısı        : 4903
Benzersiz gonderi_id    : 4903
PostgreSQL kayıt sayısı : 4903
```

---

## 💥 Duplicate Problemi & Idempotency

Pipeline’ı iki kez `append` yöntemiyle çalıştırdığımda kayıt sayısı:

```text
4903 → 9806
```

oldu.

Bu durum aynı verinin tekrar yüklenmesi halinde duplicate kayıt oluşabileceğini gösterdi.

Sorunu çözmek için:

* `gonderi_id` alanını **Primary Key** yaptım.
* PostgreSQL’de **ON CONFLICT** kullandım.
* Mevcut kayıtları güncelleyen idempotent bir yükleme oluşturdum.

Final test:

```text
1. çalıştırma → 4903
2. çalıştırma → 4903
```

✅ Böylece pipeline tekrar çalıştırıldığında veri sayısı değişmedi.

---

## 🧪 Veri Kalite Kontrolü

Son aşamada **Great Expectations** kullanarak otomatik veri kalite testleri oluşturdum.

Kontroller:

* Satır sayısı doğru mu?
* `gonderi_id` boş mu?
* `sube_kodu` boş mu?
* `alici_sehir` boş mu?
* `agirlik_kg` boş mu?
* Ağırlık değerleri pozitif mi?

Final sonuç:

```text
[PASS] Satir sayisi 4903 olmali
[PASS] gonderi_id bos olmamali
[PASS] sube_kodu bos olmamali
[PASS] alici_sehir bos olmamali
[PASS] agirlik_kg bos olmamali
[PASS] agirlik_kg pozitif olmali

✅ Tum veri kalite kontrolleri basarili.
```

---

## 🌬️ Apache Airflow

Bu haftanın önemli konularından biri de **Apache Airflow** oldu.

Airflow; veri pipeline’larını zamanlamak, task’lar arasındaki bağımlılıkları yönetmek ve süreçleri takip etmek için kullanılan bir workflow orchestration aracıdır.

Bu projedeki akış Airflow’a taşındığında örneğin:

```text
generate_data
     ↓
clean_data
     ↓
load_postgresql
     ↓
data_quality_check
```

şeklinde bir **DAG** olarak modellenebilir.

Bu projede önce Airflow’a taşınabilecek sağlam bir pipeline mantığı oluşturdum.

---

## 🧠 Karşılaştığım Hatalar

Proje sırasında birkaç gerçek problemle de karşılaştım:

* 🐳 PostgreSQL container kapalı olduğu için `Connection refused` hatası aldım.
* 📄 Bir scriptin eski CSV dosyasını okumaya devam ettiğini fark ettim.
* 🐍 `read_csv()` satırında yaptığım küçük bir yazım hatasını düzelttim.
* 🔁 `append` kullanımının duplicate kayıt oluşturduğunu gördüm ve idempotent yükleme ile çözdüm.

Bu hatalar pipeline geliştirirken yalnızca kodu değil, **veri kaynağını, servisleri ve tekrar çalıştırma davranışını da kontrol etmek gerektiğini** gösterdi.

---

## 🛠️ Kullanılan Teknolojiler

`Python` • `Pandas` • `Faker` • `Docker` • `PostgreSQL` • `SQLAlchemy` • `Great Expectations` • `Apache Airflow Concepts`

---

## 📁 Proje Dosyaları

```text
kargo-etl-odevi/
│
├── docker-compose.yml
├── generate_data.py
├── kesfet.py
├── temizle.py
├── yukle.py
├── hata_uret.py
├── idempotent_yukle.py
├── kalite_kontrol.py
│
├── gonderiler_faker.csv
├── gonderiler_temiz.csv
├── gonderiler_karantina.csv
├── requirements.txt
└── README.md
```

---

## ✨ Haftadan Kalan

Bu haftanın sonunda veri mühendisliğinin yalnızca veriyi temizlemekten ibaret olmadığını daha net gördüm.

Bir pipeline’ın yalnızca **çalışması** değil; aynı zamanda **tekrar çalıştırılabilir, güvenilir, izlenebilir ve veri kalitesini kontrol edebilir** olması gerektiğini uygulamalı olarak deneyimledim. 🚀
