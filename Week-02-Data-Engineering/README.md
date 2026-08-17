# ⭐ Week 02 — Data Modeling & Data Engineering

Bu hafta ilişkisel veri modelleme, modern veri mimarileri ve veri mühendisliğinin temel kavramları üzerine çalıştım.

## 🧩 Sektörel Veri Modelleme

Finans, sigortacılık ve üretim sektörleri için ayrı veri modelleri oluşturdum.

Her sektörde iş süreçlerine uygun **Fact** ve **Dimension** tabloları tasarladım, Excel üzerinde örnek veri setleri hazırladım ve Power BI içerisinde tablolar arasındaki ilişkileri oluşturdum.

Bu çalışma sırasında özellikle şu kavramlar üzerinde durdum:

- Fact ve Dimension tabloları
- Primary Key ve Foreign Key
- One-to-Many (`1:*`) ilişkiler
- Single Direction Filtering
- Aktif ve inaktif ilişkiler
- Star Schema
- Snowflake Schema
- Veri modeli performansı

Temel ilişki yapısı:

```text
Dimension (1) → (*) Fact
```

Dimension tarafındaki Primary Key tekil değerlerden oluşurken, aynı değer Fact tablosunda Foreign Key olarak birden fazla kez bulunabilir.

---

## ⭐ Star Schema

Star Schema yaklaşımında Fact tablolar merkezde, onları açıklayan Dimension tablolar ise çevrede yer alır.

```text
              DimCustomer
                   |
DimDate —— FactSales —— DimProduct
                   |
              DimChannel
```

Bu yapı veri modelini daha anlaşılır hale getirirken BI sorgularının ve ilişkilerin daha kontrollü yönetilmesini sağlar.

---

## 🏗️ Medallion Data Architecture

Modern veri platformlarında verinin işlenme sürecini ifade eden **Bronze → Silver → Gold** mimarisini inceledim.

```text
Bronze
Ham Veri
   ↓
Silver
Temizlenmiş Veri
   ↓
Gold
Analize Hazır Veri
```

Bronze katmanda ham veriler tutulurken, Silver katmanda veri temizlenir ve standardize edilir. Gold katmanda ise raporlama ve analitik için en değerli veri setleri hazırlanır.

---

## 🔄 ETL vs ELT

Veri entegrasyonunda kullanılan iki temel yaklaşımı araştırdım:

```text
ETL
Extract → Transform → Load
```

```text
ELT
Extract → Load → Transform
```

ETL'de veri hedef sisteme yüklenmeden önce dönüştürülürken, ELT'de veri önce hedef platforma alınır ve dönüşüm işlemleri daha sonra gerçekleştirilir.

Detaylı çalışma:

➡️ `02-ETL-vs-ELT/README.md`

---

## ☁️ Microsoft Fabric

Microsoft Fabric'in veri mühendisliği, veri analitiği, data science ve BI süreçlerini tek platform altında birleştiren yapısını inceledim.

Örnek Fabric akışı:

```text
Data Source
    ↓
Pipeline
    ↓
Lakehouse
    ↓
Notebook / Spark SQL
    ↓
Semantic Model
    ↓
Power BI
```

Bu yapı sayesinde verinin kaynaktan alınmasından raporlanmasına kadar uçtan uca bir veri süreci oluşturulabilir.

---

## 🏢 Kurumsal Power BI

Power BI raporlarının yalnızca görsel raporlar olarak değil, kurumsal bir veri modeli ve marka yapısı içerisinde nasıl ele alınabileceği üzerine çalışmaya başladım.

Bu kapsamda raporların **Shining Stars Company** çatısı altında kurumsal bir yapıya dönüştürülmesi hedeflenmektedir.

---

## 🧠 Week 02 — Key Learnings

Bu hafta;

`Fact & Dimension` • `Primary Key` • `Foreign Key` • `Star Schema` • `Snowflake Schema` • `ETL` • `ELT` • `Medallion Architecture` • `Microsoft Fabric` • `Lakehouse` • `Spark SQL` • `Semantic Model` • `Power BI`

konularını hem teorik hem de uygulamalı olarak inceleme fırsatı buldum.

---

⭐ **Shining Stars Learning Journey — Week 02**
