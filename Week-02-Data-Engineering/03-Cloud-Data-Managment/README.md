# ☁️ Cloud Data Management — Microsoft vs AWS vs Google Cloud

Bu çalışma kapsamında **Microsoft, Amazon Web Services (AWS) ve Google Cloud** platformlarının modern veri yönetimi (Data Management) yaklaşımları incelenmiş ve karşılaştırılmıştır.

Amaç yalnızca her platformda bulunan servisleri listelemek değil; aynı veri yaşam döngüsünün üç farklı cloud sağlayıcısında **nasıl tasarlandığını, hangi servislerin hangi görevi üstlendiğini ve hangi platformun hangi alanlarda öne çıktığını** anlamaktır.

---

# 📌 Data Management Nedir?

Data Management yalnızca veriyi bir veritabanında saklamak anlamına gelmez.

Modern bir veri platformunda veri;

- farklı kaynaklardan alınır,
- merkezi bir ortamda saklanır,
- temizlenir ve dönüştürülür,
- analiz edilebilir hale getirilir,
- güvenlik ve yetkilendirme kuralları uygulanır,
- kataloglanır,
- raporlama ve BI sistemlerine aktarılır.

Genel bir veri yaşam döngüsü aşağıdaki gibi düşünülebilir:

```text
Data Sources
      ↓
Data Ingestion
      ↓
Data Storage
      ↓
Data Processing / Transformation
      ↓
Analytics / Query
      ↓
Governance & Security
      ↓
Semantic / BI Layer
      ↓
Reports & Dashboards
```

Microsoft, AWS ve Google Cloud bu aşamaların tamamı için çözümler sunmaktadır.

Ancak üç platformun bu problemleri çözme biçimleri ve mimari yaklaşımları birbirinden farklıdır.

---

# 🟦 Microsoft Data Management

Microsoft tarafında modern veri ve analitik çalışmalarının merkezinde **Microsoft Fabric** bulunmaktadır.

Microsoft Fabric;

- veri entegrasyonu,
- veri mühendisliği,
- veri ambarı,
- gerçek zamanlı analitik,
- veri bilimi,
- semantic modeling,
- Business Intelligence

gibi farklı yetenekleri tek bir analitik platform altında bir araya getirmeyi amaçlamaktadır.

Fabric içerisindeki ortak veri katmanının merkezinde ise **OneLake** bulunmaktadır.

---

## 🔄 Microsoft Veri Akışı

Tipik bir Microsoft Fabric veri akışı şu şekilde oluşturulabilir:

```text
Excel / CSV / SQL / API / ERP / CRM
                 ↓
        Fabric Data Factory
     Pipeline / Dataflow Gen2
                 ↓
               OneLake
          ↙             ↘
    Lakehouse          Warehouse
          ↓               ↓
 Notebook / Spark     SQL / T-SQL
          ↘               ↙
          Curated Data
               ↓
        Semantic Model
               ↓
            Power BI
```

Bu yapı sayesinde veri ingestion aşamasından BI raporuna kadar aynı ekosistem içerisinde ilerleyebilir.

---

# 📥 Data Ingestion — Fabric Data Factory

Microsoft Fabric içerisinde veri alma ve orkestrasyon işlemlerinde **Fabric Data Factory** kullanılabilir.

Data Factory ile;

- farklı veri kaynaklarına bağlanılabilir,
- veriler taşınabilir,
- pipeline'lar oluşturulabilir,
- ETL ve ELT süreçleri tasarlanabilir,
- belirli zamanlarda çalışan işler planlanabilir.

Örneğin:

```text
SQL Database
Excel
REST API
ERP
CRM
     ↓
Fabric Data Factory
     ↓
OneLake
```

---

# 🧩 Dataflow Gen2

Microsoft tarafında düşük kodlu veri dönüşümleri için **Dataflow Gen2** kullanılabilir.

Dataflow Gen2, Power Query tabanlıdır.

Bu nedenle Excel veya Power BI üzerinde Power Query kullanan kişiler için tanıdık bir deneyim sunar.

Dataflow ile;

- kolon temizleme,
- veri tipi değiştirme,
- filtreleme,
- join,
- merge,
- aggregation,
- yeni kolon oluşturma

gibi dönüşümler gerçekleştirilebilir.

---

# 🌊 OneLake

Microsoft Fabric mimarisinin en önemli bileşenlerinden biri **OneLake**'tir.

OneLake, Fabric içerisinde merkezi veri depolama katmanı olarak kullanılmaktadır.

Basit olarak:

> **OneLake = Microsoft Fabric ekosistemindeki merkezi data lake katmanı**

şeklinde düşünülebilir.

Farklı Fabric workload'ları aynı veri katmanından yararlanabilir.

Bu yaklaşım aynı verinin sürekli farklı sistemlere kopyalanması ihtiyacını azaltmayı amaçlar.

---

# 🏠 Fabric Lakehouse

Fabric Lakehouse, Data Lake ile Data Warehouse yaklaşımlarını bir araya getirmeyi amaçlayan bir yapıdır.

Lakehouse içerisinde veriler hem:

```text
Spark / Notebook
```

hem de:

```text
SQL
```

üzerinden kullanılabilir.

Bu sayede aynı veri üzerinde farklı ekipler çalışabilir.

Örneğin:

```text
Data Engineer
      ↓
Spark / PySpark
```

ve:

```text
Data Analyst
      ↓
SQL / Power BI
```

aynı veri platformundan yararlanabilir.

---

# 🏢 Fabric Warehouse

Daha ilişkisel ve analitik odaklı modeller için **Fabric Warehouse** kullanılabilir.

Örneğin;

- Fact tabloları,
- Dimension tabloları,
- Star Schema,
- Snowflake Schema,
- Data Mart

gibi yapılar Warehouse içerisinde oluşturulabilir.

Bu yapı özellikle kurumsal raporlama ve BI senaryolarında kullanılabilir.

---

# ⚡ Spark ve Notebook

Fabric içerisinde Notebook kullanılarak Spark tabanlı veri dönüşümleri yapılabilir.

Örneğin:

```text
Raw Data
   ↓
PySpark / Spark SQL
   ↓
Clean Data
   ↓
Analytics Tables
```

Notebook içerisinde;

- veri temizleme,
- join,
- aggregation,
- feature engineering,
- veri kalite kontrolleri,
- yeni tablolar oluşturma

gibi işlemler yapılabilir.

---

# 🥉 Medallion Architecture

Fabric Lakehouse ortamında modern veri mimarilerinde sık görülen:

```text
Bronze
  ↓
Silver
  ↓
Gold
```

yaklaşımı uygulanabilir.

### Bronze

Ham veri.

### Silver

Temizlenmiş ve standardize edilmiş veri.

### Gold

BI ve analitik kullanım için hazırlanmış veri.

Örneğin Gold katmanda:

```text
FactSales
FactClaims
DimCustomer
DimProduct
DimDate
```

gibi analitik tablolar oluşturulabilir.

---

# 📊 Semantic Model ve Power BI

Microsoft tarafındaki en önemli avantajlardan biri veri mühendisliği ile Power BI arasındaki güçlü entegrasyondur.

Veri hazırlandıktan sonra:

```text
Lakehouse / Warehouse
        ↓
Semantic Model
        ↓
Power BI
```

akışı kurulabilir.

Semantic Model içerisinde;

- Fact ve Dimension tabloları,
- relationships,
- measures,
- DAX hesaplamaları,
- business metrics

tanımlanabilir.

---

# 🚀 Microsoft'un Öne Çıkan Tarafı

Microsoft tarafında en dikkat çekici özellik:

> **Veri ingestion aşamasından Power BI raporuna kadar uçtan uca bütünleşik bir analitik deneyim sunmasıdır.**

Özellikle Microsoft ve Power BI ekosistemini kullanan şirketler açısından Fabric güçlü bir seçenek olabilir.

---

# 🟧 AWS Data Management

AWS tarafında Microsoft'tan biraz daha farklı bir yaklaşım bulunmaktadır.

AWS'de genellikle tek bir merkezi analitik ürün yerine, farklı veri problemleri için geliştirilmiş **uzmanlaşmış servisler** birlikte kullanılmaktadır.

Bu nedenle AWS veri mimarileri oldukça modüler şekilde tasarlanabilir.

---

## 🔄 AWS Veri Akışı

Tipik bir AWS veri akışı aşağıdaki gibi düşünülebilir:

```text
Databases / Files / Applications / Streams
                   ↓
            Glue / Kinesis
                   ↓
              Amazon S3
               Data Lake
                   ↓
          Glue Data Catalog
                   ↓
          Glue / Amazon EMR
                   ↓
          Athena / Redshift
                   ↓
        Amazon Quick Sight
```

Governance tarafında ise:

```text
Lake Formation
      +
Amazon DataZone
```

gibi servisler kullanılabilir.

---

# 🪣 Amazon S3

AWS data lake mimarilerinin merkezinde çoğu zaman **Amazon S3** bulunur.

S3;

- ham veri,
- temizlenmiş veri,
- log dosyaları,
- CSV,
- JSON,
- Parquet

gibi çok farklı veri türlerini saklamak için kullanılabilir.

Örneğin:

```text
CSV
JSON
Application Logs
Database Export
IoT Data
       ↓
   Amazon S3
```

---

# 🧩 AWS Glue

AWS tarafında veri entegrasyonu ve ETL/ELT işlemlerinin önemli servislerinden biri **AWS Glue**'dur.

AWS Glue ile;

- veri kaynakları keşfedilebilir,
- ETL işlemleri gerçekleştirilebilir,
- Spark tabanlı dönüşümler yapılabilir,
- veri catalog işlemleri yapılabilir,
- pipeline'lar oluşturulabilir.

Örneğin:

```text
Amazon S3
    ↓
AWS Glue
    ↓
Clean / Curated Data
    ↓
Amazon S3
```

---

# 🔍 Glue Crawler

AWS Glue içerisindeki önemli özelliklerden biri **Crawler**'dır.

Crawler veri kaynaklarını tarayarak;

- kolon isimlerini,
- veri tiplerini,
- tablo yapısını,
- partition bilgilerini

tespit edebilir.

Bu bilgiler daha sonra **Glue Data Catalog** içerisine kaydedilebilir.

---

# 📚 Glue Data Catalog

Glue Data Catalog, verinin kendisini değil, veri hakkındaki bilgileri yani **metadata** bilgisini saklar.

Örneğin:

```text
Table Name
Column Name
Data Type
Location
Partition Information
```

gibi bilgiler Data Catalog içerisinde tutulabilir.

Bu catalog farklı AWS servisleri tarafından kullanılabilir.

---

# 🔎 Amazon Athena

**Amazon Athena**, Amazon S3 üzerindeki verileri SQL kullanarak sorgulamaya olanak sağlayan serverless bir analitik servistir.

Örneğin:

```text
Amazon S3
     ↓
Glue Data Catalog
     ↓
Amazon Athena
     ↓
SQL Query
```

Bu sayede veriyi klasik bir veritabanına taşımadan S3 üzerindeki veri SQL ile analiz edilebilir.

---

# 🏢 Amazon Redshift

AWS tarafındaki Data Warehouse hizmetlerinden biri **Amazon Redshift**'tir.

Redshift;

- büyük analitik veri kümeleri,
- Data Warehouse,
- BI,
- SQL tabanlı analitik

senaryolarında kullanılabilir.

Örneğin:

```text
Operational Systems
        ↓
     ETL / ELT
        ↓
     Redshift
        ↓
        BI
```

---

# 🐘 Amazon EMR

Apache Spark, Hadoop ve benzeri büyük veri teknolojilerinin kullanıldığı senaryolarda **Amazon EMR** kullanılabilir.

Örneğin:

```text
Amazon S3
    ↓
Amazon EMR
    ↓
Apache Spark
    ↓
Processed Data
```

EMR, daha fazla big data processing kontrolüne ihtiyaç duyulan senaryolarda kullanılabilir.

---

# ⚡ Streaming — Amazon Kinesis

Gerçek zamanlı veri işleme için AWS tarafında **Amazon Kinesis** kullanılabilir.

Örneğin:

```text
Application Events
        ↓
     Kinesis
        ↓
 Stream Processing
        ↓
        S3
     / Redshift
```

IoT verileri, uygulama event'leri veya kullanıcı hareketleri gibi sürekli üretilen veriler bu yapı üzerinden işlenebilir.

---

# 🔐 AWS Lake Formation

AWS tarafında Data Lake güvenliği ve governance işlemleri için **Lake Formation** kullanılabilir.

Lake Formation ile;

- veri erişimi,
- yetkilendirme,
- merkezi güvenlik politikaları,
- hassas veri kontrolü

yönetilebilir.

Büyük kurumsal veri platformlarında governance açısından önemli bir servistir.

---

# 🗂️ Amazon DataZone

Amazon DataZone veri keşfi, paylaşımı ve governance tarafında kullanılabilir.

Amaç farklı ekiplerin kurum içerisindeki veriyi:

- bulabilmesi,
- anlayabilmesi,
- paylaşabilmesi,
- kontrollü şekilde kullanabilmesi

için ortak bir yapı sağlamaktır.

---

# 📊 Amazon Quick Sight

AWS tarafında BI ve dashboard çözümleri için **Amazon Quick Sight** kullanılabilir.

Quick Sight ile;

- dashboard,
- visualization,
- analytical reporting,
- embedded analytics

senaryoları oluşturulabilir.

---

# 🚀 AWS'nin Öne Çıkan Tarafı

AWS'nin en belirgin özelliklerinden biri:

> **Farklı veri ihtiyaçları için çok sayıda uzmanlaşmış servis sunmasıdır.**

Bu yaklaşım yüksek mimari esneklik sağlar.

Ancak çok sayıda servis bulunduğu için doğru servislerin seçilmesi ve birlikte yönetilmesi daha fazla mimari bilgi gerektirebilir.

---

# 🟥 Google Cloud Data Management

Google Cloud tarafında veri ve analitik ekosisteminin merkezinde özellikle **BigQuery** önemli bir rol oynar.

Google Cloud'un yaklaşımında;

- serverless analytics,
- streaming,
- büyük veri,
- data science,
- AI

özellikleri ön plana çıkmaktadır.

---

## 🔄 Google Cloud Veri Akışı

Tipik bir veri akışı:

```text
Applications / Databases / Files / Events
                    ↓
             Pub/Sub / Dataflow
                    ↓
        BigQuery / Cloud Storage
                    ↓
     BigQuery SQL / Dataflow
          Dataproc / Spark
                    ↓
                 Looker
```

Governance ve catalog tarafında ise Google Cloud'un metadata ve data governance servisleri kullanılabilir.

---

# 🏢 BigQuery

Google Cloud tarafındaki en önemli veri analitik platformlarından biri **BigQuery**'dir.

BigQuery'nin önemli özelliklerinden biri **serverless** yapısıdır.

Bu sayede kullanıcılar klasik anlamda:

```text
Server oluştur
Cluster yönet
Capacity ayarla
```

gibi altyapı işlemleriyle daha az uğraşarak analitik sorgulara odaklanabilir.

BigQuery üzerinde SQL kullanılarak büyük veri kümeleri analiz edilebilir.

---

# ☁️ Cloud Storage

Google Cloud içerisindeki object storage servisi **Cloud Storage**'dır.

Data Lake senaryolarında;

- CSV,
- JSON,
- Parquet,
- log dosyaları,
- büyük veri dosyaları

Cloud Storage üzerinde saklanabilir.

Örneğin:

```text
Files
Logs
Exports
Raw Data
    ↓
Cloud Storage
```

---

# 📡 Pub/Sub

Gerçek zamanlı event ve mesaj ingestion işlemlerinde **Pub/Sub** kullanılabilir.

Örneğin:

```text
Mobile App
Website
IoT Device
Application
     ↓
   Pub/Sub
```

Pub/Sub producer ve consumer sistemlerini birbirinden ayırarak ölçeklenebilir event-driven mimariler kurulmasını sağlar.

---

# 🌊 Dataflow

Google Cloud tarafında veri processing için önemli servislerden biri **Dataflow**'dur.

Dataflow, Apache Beam tabanlıdır.

En dikkat çekici özelliklerinden biri aynı programlama modeli üzerinden hem:

```text
Batch Processing
```

hem de:

```text
Streaming Processing
```

senaryolarının oluşturulabilmesidir.

Örneğin:

```text
Pub/Sub
   ↓
Dataflow
   ↓
BigQuery
```

gerçek zamanlı analitik senaryolarında kullanılabilir.

---

# 🐘 Dataproc

Apache Spark ve Hadoop tabanlı işlemler için **Dataproc** kullanılabilir.

Örneğin:

```text
Cloud Storage
      ↓
   Dataproc
      ↓
Apache Spark
      ↓
BigQuery / Storage
```

Dataproc özellikle mevcut Spark veya Hadoop workload'larının Google Cloud üzerinde çalıştırılmasında kullanılabilir.

---

# 🔄 Workflow Orchestration

Veri pipeline'larının belirli sırayla çalıştırılması gerektiğinde Apache Airflow tabanlı orchestration çözümleri kullanılabilir.

Örneğin:

```text
Load Data
   ↓
Transform
   ↓
Data Quality Check
   ↓
Create Analytics Table
   ↓
Refresh BI
```

gibi bir workflow oluşturulabilir.

---

# 🗂️ Data Catalog ve Governance

Google Cloud tarafında veri catalog ve governance sistemleri sayesinde;

- metadata yönetimi,
- data discovery,
- data lineage,
- veri kalite kontrolleri,
- business glossary

gibi süreçler yönetilebilir.

Bu yapı özellikle büyük organizasyonlarda verinin nerede bulunduğunu ve nasıl kullanıldığını anlamak açısından önemlidir.

---

# 📊 Looker

Google Cloud tarafındaki kurumsal BI çözümlerinden biri **Looker**'dır.

Looker ile;

- dashboard,
- raporlama,
- embedded analytics,
- semantic modeling

senaryoları oluşturulabilir.

Looker tarafında **LookML** kullanılarak ortak business metric tanımları oluşturulabilir.

---

# 🚀 Google Cloud'un Öne Çıkan Tarafı

Google Cloud tarafında özellikle:

> **BigQuery'nin serverless analitik yaklaşımı ve Pub/Sub + Dataflow ile batch ve streaming veri işleme yetenekleri**

öne çıkmaktadır.

BigQuery merkezli mimari birçok analitik senaryonun daha sade şekilde tasarlanmasını sağlayabilir.

---

# 📊 Microsoft vs AWS vs Google Cloud

| Kriter | Microsoft | AWS | Google Cloud |
|---|---|---|---|
| Ana yaklaşım | Bütünleşik analitik platform | Modüler servis mimarisi | BigQuery merkezli serverless yaklaşım |
| Ana veri platformu | Microsoft Fabric | AWS Data & Analytics Services | Google Cloud Data Platform |
| Data Lake | OneLake | Amazon S3 | Cloud Storage |
| Lakehouse | Fabric Lakehouse | S3 tabanlı Lakehouse mimarileri | Google Cloud Lakehouse |
| Data Warehouse | Fabric Warehouse | Amazon Redshift | BigQuery |
| Data Integration | Fabric Data Factory | AWS Glue | Dataflow |
| Low-Code Dönüşüm | Dataflow Gen2 | Glue Studio | Çeşitli managed araçlar |
| Spark | Fabric Spark | Amazon EMR / Glue | Dataproc |
| Serverless SQL | Fabric SQL çözümleri | Amazon Athena | BigQuery |
| Streaming | Fabric Real-Time Intelligence | Amazon Kinesis | Pub/Sub + Dataflow |
| Metadata / Catalog | OneLake Catalog | Glue Data Catalog | Google Cloud Catalog çözümleri |
| Governance | Microsoft Purview | Lake Formation / DataZone | Google Cloud Governance çözümleri |
| Semantic Layer | Power BI Semantic Model | BI / Dataset katmanları | LookML |
| BI | Power BI | Amazon Quick Sight | Looker |
| ETL | ✅ | ✅ | ✅ |
| ELT | ✅ | ✅ | ✅ |
| Batch | ✅ | ✅ | ✅ |
| Streaming | ✅ | ✅ | ✅ |
| Data Science | ✅ | ✅ | ✅ |
| En belirgin güçlü yön | Entegrasyon | Esneklik ve servis çeşitliliği | Serverless analytics ve streaming |

---

# 🔄 Aynı Veri Üç Platformda Nasıl İlerler?

Aynı Excel veya CSV dosyasını üç platformda kullandığımızı düşünelim.

---

## 🟦 Microsoft

```text
Excel / CSV
     ↓
Fabric Data Factory
     ↓
OneLake
     ↓
Fabric Lakehouse
     ↓
Notebook / Spark SQL
     ↓
Gold Tables
     ↓
Semantic Model
     ↓
Power BI
```

---

## 🟧 AWS

```text
Excel / CSV
     ↓
Amazon S3
     ↓
Glue Crawler
     ↓
Glue Data Catalog
     ↓
AWS Glue
     ↓
Athena / Redshift
     ↓
Amazon Quick Sight
```

---

## 🟥 Google Cloud

```text
Excel / CSV
     ↓
Cloud Storage / BigQuery
     ↓
Dataflow / BigQuery SQL
     ↓
Curated BigQuery Tables
     ↓
Looker
```

Gerçek zamanlı bir senaryoda:

```text
Application Events
       ↓
     Pub/Sub
       ↓
    Dataflow
       ↓
    BigQuery
       ↓
     Looker
```

---

# 🎯 Hangi Platform Hangi Alanda Öne Çıkıyor?

## 🟦 Microsoft

Özellikle;

- Microsoft ekosistemi kullanan şirketlerde,
- Power BI yoğun kullanılan ortamlarda,
- veri mühendisliği ve BI süreçlerinin tek platform altında tutulmak istendiği durumlarda

öne çıkabilir.

En belirgin avantajı:

> **Fabric + OneLake + Semantic Model + Power BI entegrasyonu**

olarak değerlendirilebilir.

---

## 🟧 AWS

Özellikle;

- çok özelleştirilmiş cloud mimarilerinde,
- büyük servis çeşitliliğine ihtiyaç duyulduğunda,
- farklı workload'lar için farklı teknolojilerin seçilmek istendiği durumlarda

öne çıkabilir.

En belirgin avantajı:

> **Modülerlik ve mimari esneklik**

olarak değerlendirilebilir.

---

## 🟥 Google Cloud

Özellikle;

- serverless analytics,
- BigQuery,
- gerçek zamanlı veri,
- batch + streaming,
- data science ve AI

odaklı projelerde öne çıkabilir.

En belirgin avantajı:

> **BigQuery + Pub/Sub + Dataflow tabanlı güçlü analitik mimari**

olarak değerlendirilebilir.

---

# ❓ Hangisi Daha İyi?

Tek bir platformun bütün kullanım senaryolarında diğerlerinden daha iyi olduğunu söylemek doğru değildir.

Platform seçimi yapılırken;

- şirketin mevcut teknoloji altyapısı,
- veri hacmi,
- veri kaynakları,
- gerçek zamanlı veri ihtiyacı,
- güvenlik gereksinimleri,
- governance ihtiyaçları,
- ekip yetkinlikleri,
- BI araçları,
- Data Science gereksinimleri,
- maliyet,
- vendor ecosystem,
- mimari esneklik

gibi faktörler değerlendirilmelidir.

Bu nedenle:

> **“Hangi cloud platformu en iyi?”**

sorusundan ziyade;

> **“Bu şirketin veri mimarisi ve iş ihtiyaçları için hangi platform daha uygun?”**

sorusunu sormak daha doğru bir yaklaşımdır.

---

# 🧠 Bu Çalışmada Öğrendiklerim

Bu çalışma kapsamında;

- modern Data Management yaşam döngüsünü,
- Data Ingestion kavramını,
- Data Lake ve Lakehouse yapılarını,
- Data Warehouse kullanımını,
- batch ve streaming veri işleme farkını,
- metadata ve Data Catalog kavramlarını,
- Data Governance'ın önemini,
- Microsoft Fabric mimarisini,
- OneLake ve Fabric Lakehouse yapılarını,
- AWS S3, Glue, Athena, EMR ve Redshift servislerini,
- Google BigQuery, Pub/Sub, Dataflow ve Dataproc servislerini,
- cloud platformlarında ETL ve ELT süreçlerini,
- BI ve Semantic Layer yaklaşımlarını

karşılaştırmalı olarak inceleme fırsatı buldum.

---

# 📌 Kısa Özet

```text
MICROSOFT
Fabric + OneLake + Power BI
→ Bütünleşik analitik deneyim

AWS
S3 + Glue + Athena / Redshift
→ Modülerlik ve servis çeşitliliği

GOOGLE CLOUD
BigQuery + Pub/Sub + Dataflow
→ Serverless analytics ve streaming
```

Üç platform da modern veri yönetimi ihtiyaçlarını karşılayabilecek güçlü servisler sunmaktadır.

Farklılık ise bu servislerin **nasıl bir mimari felsefe altında bir araya getirildiğinde** ortaya çıkmaktadır.

---

# 📚 Kaynaklar

Bu araştırma kapsamında ağırlıklı olarak aşağıdaki resmi dokümantasyonlardan yararlanılmıştır:

- Microsoft Learn — Microsoft Fabric Documentation
- Microsoft Learn — OneLake Documentation
- Microsoft Learn — Fabric Data Factory
- Microsoft Learn — Fabric Lakehouse
- Microsoft Learn — Power BI Semantic Models
- AWS Documentation — Amazon S3
- AWS Documentation — AWS Glue
- AWS Documentation — Glue Data Catalog
- AWS Documentation — Amazon Athena
- AWS Documentation — Amazon Redshift
- AWS Documentation — AWS Lake Formation
- AWS Documentation — Amazon EMR
- Google Cloud Documentation — BigQuery
- Google Cloud Documentation — Pub/Sub
- Google Cloud Documentation — Dataflow
- Google Cloud Documentation — Dataproc
- Google Cloud Documentation — Looker

---

⭐ **Shining Stars Learning Journey — Week 02**
