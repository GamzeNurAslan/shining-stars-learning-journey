# 🔄 ETL vs ELT — Veri Entegrasyonu Yaklaşımlarının Karşılaştırılması

Bu çalışma kapsamında veri mühendisliğinin temel kavramlarından olan **ETL (Extract, Transform, Load)** ve **ELT (Extract, Load, Transform)** yaklaşımları araştırılmış ve karşılaştırılmıştır.

Her iki yaklaşımın da temel amacı; farklı veri kaynaklarından gelen verileri toplamak, analize uygun hale getirmek ve hedef veri platformlarına taşımaktır.

Aralarındaki temel fark ise **dönüşüm işleminin hangi aşamada gerçekleştirildiğidir.**

---

## 📌 Neden ETL ve ELT'ye İhtiyaç Duyulur?

Gerçek hayatta veriler genellikle tek bir kaynaktan gelmez.

Bir kurumun verileri;

- Excel ve CSV dosyalarında,
- ERP sistemlerinde,
- CRM sistemlerinde,
- SQL veritabanlarında,
- API'lerde,
- web uygulamalarında,
- IoT cihazlarında,
- log dosyalarında,
- cloud servislerinde,
- streaming kaynaklarında

bulunabilir.

Bu kaynaklardan gelen veriler çoğu zaman doğrudan analize hazır değildir.

Örneğin verilerde;

- eksik değerler,
- duplicate kayıtlar,
- hatalı veri tipleri,
- farklı tarih formatları,
- standart olmayan metin değerleri,
- farklı para birimleri,
- gereksiz kolonlar

bulunabilir.

Bu nedenle verinin raporlama, veri analitiği veya makine öğrenmesi süreçlerinde kullanılmadan önce belirli işlemlerden geçirilmesi gerekir.

ETL ve ELT, bu veri entegrasyonu sürecinde kullanılan iki temel yaklaşımdır.

---

# 🟦 ETL Nedir?

**ETL**, aşağıdaki üç adımın baş harflerinden oluşur:

> **Extract → Transform → Load**

Türkçesi:

> **Veriyi Çıkar → Dönüştür → Yükle**

ETL yaklaşımında veri, hedef sisteme yüklenmeden **önce** temizlenir ve dönüştürülür.

### Temel ETL Akışı

```text
Data Sources
     ↓
  Extract
     ↓
 Transform
     ↓
    Load
     ↓
Data Warehouse
     ↓
Analytics / BI
```

---

## 1️⃣ Extract — Veriyi Kaynaktan Alma

İlk aşamada ihtiyaç duyulan veriler farklı kaynak sistemlerden alınır.

Örneğin:

```text
Excel
CRM
ERP
SQL Database
API
IoT
   ↓
Extract
```

Bu aşamanın amacı veriyi kaynak sistemlerden güvenilir şekilde elde etmektir.

Henüz iş kuralları veya analitik dönüşümler uygulanmaz.

---

## 2️⃣ Transform — Veriyi Dönüştürme

ETL sürecinin en önemli aşamalarından biridir.

Veri hedef sisteme ulaşmadan önce temizlenir, standartlaştırılır ve iş kurallarına uygun hale getirilir.

Transform aşamasında;

- eksik değerlerin düzenlenmesi,
- duplicate kayıtların kaldırılması,
- veri tiplerinin değiştirilmesi,
- tarih formatlarının standartlaştırılması,
- metin alanlarının temizlenmesi,
- tabloların join edilmesi,
- filtreleme yapılması,
- aggregation işlemleri,
- yeni kolonların oluşturulması,
- para birimi dönüşümleri,
- hassas verilerin maskelenmesi,
- iş kurallarının uygulanması

gibi işlemler gerçekleştirilebilir.

### Örnek

Kaynak veri:

```text
CustomerID | City      | Premium
-----------|-----------|-----------
1          | istanbul  | 12.500 TL
2          | ANKARA    | 8.200 TL
3          | izmir     | NULL
```

Dönüşümden sonra:

```text
CustomerID | City      | PremiumTRY
-----------|-----------|-----------
1          | İstanbul  | 12500
2          | Ankara    | 8200
3          | İzmir     | 0
```

Veri artık daha standart ve analize hazır hale gelmiştir.

---

## 3️⃣ Load — Hedef Sisteme Yükleme

Veri temizlenip dönüştürüldükten sonra hedef sisteme yüklenir.

Örneğin:

```text
Clean Data
    ↓
Data Warehouse
    ↓
Semantic Model
    ↓
Power BI
```

ETL yaklaşımında temel mantık şudur:

> **Hedef sisteme mümkün olduğunca temizlenmiş ve kullanıma hazır veri yüklenir.**

---

# 🟥 ELT Nedir?

**ELT**, aşağıdaki üç adımın baş harflerinden oluşur:

> **Extract → Load → Transform**

Türkçesi:

> **Veriyi Çıkar → Yükle → Dönüştür**

ELT yaklaşımında veri kaynaktan alındıktan sonra önce hedef veri platformuna yüklenir.

Dönüşüm işlemleri ise **yüklemeden sonra**, hedef sistem içerisinde gerçekleştirilir.

### Temel ELT Akışı

```text
Data Sources
     ↓
  Extract
     ↓
    Load
     ↓
Data Lake / Lakehouse
     ↓
 Transform
     ↓
Analytics / BI
```

---

## ELT Nasıl Çalışır?

Örneğin bir Excel dosyasındaki verinin Lakehouse ortamına alındığını düşünelim:

```text
Excel
  ↓
Extract
  ↓
Lakehouse
  ↓
Load
  ↓
Spark / SQL / Notebook
  ↓
Transform
  ↓
Semantic Model
  ↓
Power BI
```

Veri önce Lakehouse ortamına yüklenir.

Daha sonra;

- SQL,
- Spark,
- PySpark,
- Notebook

gibi teknolojiler kullanılarak dönüştürülür.

Buradaki en önemli fark şudur:

> **ELT'de hedef veri platformunun işlem gücü dönüşüm amacıyla kullanılır.**

---

# ⚖️ ETL ve ELT Arasındaki Temel Fark

En kısa haliyle:

```text
ETL
Extract → Transform → Load
Önce dönüştür, sonra yükle.

ELT
Extract → Load → Transform
Önce yükle, sonra dönüştür.
```

Ancak fark yalnızca sıralama değildir.

Bu farklılık;

- veri mimarisini,
- depolama stratejisini,
- performansı,
- maliyeti,
- güvenliği,
- ölçeklenebilirliği,
- veri bilimi kullanımını,
- veri yönetişimini

de etkileyebilir.

---

# 📊 ETL ve ELT Karşılaştırması

| Özellik | ETL | ELT |
|---|---|---|
| Açılım | Extract – Transform – Load | Extract – Load – Transform |
| İşlem sırası | Çıkar → Dönüştür → Yükle | Çıkar → Yükle → Dönüştür |
| Dönüşüm zamanı | Yüklemeden önce | Yüklemeden sonra |
| Dönüşüm yeri | ETL işlem katmanı | Hedef veri platformu |
| Ham verinin korunması | Her zaman korunmayabilir | Genellikle korunabilir |
| Cloud kullanımı | Kullanılabilir | Çok yaygın |
| Büyük veri | Kullanılabilir | Büyük veri için oldukça uygundur |
| Yeniden işleme | Kaynağa tekrar dönmek gerekebilir | Ham veri üzerinden tekrar yapılabilir |
| Esneklik | Daha kontrollü | Daha esnek |
| Data Lake / Lakehouse | Kullanılabilir | Çok yaygın |
| Data Warehouse | Geleneksel kullanım alanıdır | Modern warehouse sistemlerinde de kullanılır |
| İşlem gücü | ETL aracında | Hedef sistemde |
| Data Science | Kullanılabilir | Ham veri erişimi nedeniyle avantajlıdır |
| Governance ihtiyacı | Önemlidir | Ham veri nedeniyle özellikle önemlidir |

---

# ✅ ETL'nin Avantajları

### Veri Kalitesi

Veriler hedef sisteme gitmeden önce kalite kontrollerinden geçirilebilir.

### Kontrollü Veri Yükleme

Hedef sisteme yalnızca ihtiyaç duyulan veri aktarılabilir.

### Güvenlik

Hassas bilgiler yüklemeden önce maskelenebilir veya anonimleştirilebilir.

Örneğin:

```text
TC Kimlik No
Telefon
Kredi Kartı
Adres
Sağlık Bilgisi
```

gibi alanlar hedef sisteme aktarılmadan önce dönüştürülebilir.

### Hedef Sistem Üzerindeki Yük

Dönüşüm başka bir ortamda gerçekleştirildiği için hedef sistem üzerindeki işlem yükü azaltılabilir.

---

# ❌ ETL'nin Dezavantajları

### Ham Veri Kaybedilebilir

Dönüşüm sırasında kullanılmadığı düşünülen bazı alanlar hedef sisteme aktarılmayabilir.

Örneğin kaynak sistemde:

```text
CustomerID
Name
City
Age
Occupation
Income
RiskScore
```

alanları bulunurken Data Warehouse'a yalnızca:

```text
CustomerID
City
Age
```

aktarılmış olabilir.

Daha sonra `Income` alanına ihtiyaç duyulduğunda kaynak sisteme tekrar dönmek gerekebilir.

### Büyük Veri Dönüşümleri

Çok büyük veri hacimlerinde verinin tamamını yüklemeden önce dönüştürmek zaman alabilir.

### Daha Az Esneklik

Değişen analiz ihtiyaçlarında mevcut ETL pipeline'larının yeniden düzenlenmesi gerekebilir.

---

# ✅ ELT'nin Avantajları

### Ham Verinin Korunması

Ham veri hedef ortamda saklanabilir.

Örneğin:

```text
Raw Data
   ↓
Clean Data
   ↓
Analytics Data
```

Böylece yeni analiz ihtiyaçlarında kaynak sistemden tekrar veri çekme ihtiyacı azalabilir.

### Büyük Veri Desteği

Modern cloud sistemlerinin yüksek işlem ve depolama kapasitesinden yararlanılabilir.

### Esneklik

Aynı ham veri farklı amaçlarla kullanılabilir.

Örneğin:

```text
Ham Müşteri Verisi
        ↓
     Analyst
        ↓
   Satış Analizi
```

aynı veri:

```text
Ham Müşteri Verisi
        ↓
  Data Scientist
        ↓
 Churn Prediction
```

için de kullanılabilir.

### Modern Veri Mimarileriyle Uyum

ELT özellikle;

- Data Lake,
- Lakehouse,
- Cloud Data Warehouse,
- Big Data,
- Data Science

senaryolarında yaygın olarak kullanılmaktadır.

---

# ❌ ELT'nin Dezavantajları

### Güvenlik

Ham verinin hedef sistemde bulunması hassas bilgilerin korunmasını daha önemli hale getirir.

### Data Governance

Kontrolsüz biçimde depolanan veriler zamanla karmaşık hale gelebilir.

İyi yönetilmeyen bir Data Lake'in:

> **Data Lake → Data Swamp**

haline gelmesi mümkündür.

Bu nedenle;

- metadata yönetimi,
- data catalog,
- data lineage,
- veri kalitesi,
- erişim kontrolü,
- isimlendirme standartları

önemlidir.

### Maliyet Yönetimi

Ham verinin tamamını sürekli saklamak ve tekrar tekrar işlemek gereksiz maliyet oluşturabilir.

---

# 🏗️ Schema-on-Write ve Schema-on-Read

ETL ve ELT ile birlikte sık karşılaşılan iki kavram da **Schema-on-Write** ve **Schema-on-Read**'dir.

## Schema-on-Write

Veri sisteme yazılmadan önce yapısı belirlenir.

Örneğin:

```text
CustomerKey     INT
CustomerName    VARCHAR
PremiumTRY      DECIMAL
PolicyDate      DATE
```

Veri bu yapıya uygun hale getirildikten sonra sisteme yüklenir.

Bu yaklaşım geleneksel Data Warehouse sistemlerinde yaygındır.

---

## Schema-on-Read

Veri daha ham ve esnek biçimde saklanabilir.

Şema, verinin okunması ve analiz edilmesi sırasında uygulanabilir.

Bu yaklaşım özellikle Data Lake sistemlerinde kullanılabilir.

Modern Lakehouse sistemlerinde ise Schema-on-Write ve Schema-on-Read yaklaşımları birlikte kullanılabilir.

---

# 🥉 Bronze – Silver – Gold Yaklaşımı

Modern Lakehouse ve ELT projelerinde sık kullanılan yaklaşımlardan biri **Medallion Architecture**'dır.

```text
BRONZE
Ham Veri
   ↓
SILVER
Temizlenmiş Veri
   ↓
GOLD
Analize Hazır Veri
```

## Bronze Layer

Kaynak sistemden gelen veri mümkün olduğunca ham biçimde tutulur.

Örneğin:

```text
Excel
API
Database
IoT
Log
```

verileri doğrudan Bronze katmana alınabilir.

## Silver Layer

Bu katmanda veri;

- temizlenir,
- duplicate kayıtlardan arındırılır,
- veri tipleri düzeltilir,
- standardize edilir,
- join işlemleri yapılır,
- iş kuralları uygulanır.

## Gold Layer

Veri artık BI ve analitik uygulamalar için hazırlanır.

Örneğin:

```text
FactSales
FactClaims
DimCustomer
DimProduct
DimDate
```

gibi Fact ve Dimension tabloları oluşturulabilir.

Gold katman Star Schema gibi analitik veri modellerinin oluşturulması için kullanılabilir.

---

# 🏢 ETL Ne Zaman Tercih Edilebilir?

ETL yaklaşımı;

- hedef sisteme yalnızca temiz veri gönderilmesi gerekiyorsa,
- güçlü veri kalite kuralları varsa,
- hassas veriler yüklemeden önce dönüştürülecekse,
- hedef sistemin işlem kapasitesi sınırlıysa,
- veri yapısı önceden net olarak tanımlanmışsa,
- geleneksel Data Warehouse mimarisi kullanılıyorsa

tercih edilebilir.

---

# ☁️ ELT Ne Zaman Tercih Edilebilir?

ELT yaklaşımı;

- yüksek veri hacimleri varsa,
- cloud platformları kullanılıyorsa,
- Data Lake veya Lakehouse mimarisi bulunuyorsa,
- ham veri korunmak isteniyorsa,
- aynı veri farklı ekipler tarafından kullanılacaksa,
- Data Science çalışmaları yapılacaksa,
- Spark gibi dağıtık işlem teknolojileri kullanılacaksa,
- hedef veri platformunun işlem gücü yüksekse

avantaj sağlayabilir.

---

# 🔀 ETL ve ELT Birlikte Kullanılabilir mi?

Evet.

Gerçek dünya projelerinde bir veri pipeline'ının tamamen ETL veya tamamen ELT olması gerekmez.

Örneğin:

```text
Kaynak Sistem
      ↓
Hassas Veriyi Maskele
      ↓
Lakehouse'a Yükle
      ↓
Spark / SQL ile Dönüştür
      ↓
Gold Tables
      ↓
Semantic Model
      ↓
Power BI
```

Bu örnekte verinin bazı dönüşümleri yüklemeden önce yapılırken, daha kapsamlı dönüşümler yüklemeden sonra gerçekleştirilmektedir.

Bu nedenle modern projelerde **hibrit ETL/ELT mimarileri** kullanılabilir.

---

# 🧩 Microsoft Fabric ile ELT Örneği

Microsoft Fabric üzerinde örnek bir ELT süreci aşağıdaki gibi oluşturulabilir:

```text
Excel / CSV / Database
          ↓
       Extract
          ↓
 Fabric Data Factory
          ↓
        Load
          ↓
 OneLake / Lakehouse
          ↓
 Notebook / Spark SQL
          ↓
      Transform
          ↓
    Silver Tables
          ↓
      Gold Tables
          ↓
   Semantic Model
          ↓
      Power BI
```

Veri önce Fabric Lakehouse ortamına alınır.

Daha sonra Notebook, Spark veya SQL kullanılarak dönüşüm işlemleri gerçekleştirilir.

Analize hazır Fact ve Dimension tabloları oluşturulduktan sonra Semantic Model üzerinden Power BI raporları hazırlanabilir.

---

# 🛡️ Sigortacılık Verisi Üzerinden Örnek ELT Senaryosu

Örneğin aşağıdaki sigortacılık tablolarının bulunduğunu düşünelim:

```text
FactPolicy
FactClaims
FactPremiumPayments
FactQuotes

DimCustomer
DimInsuranceProduct
DimPolicy
DimDate
```

Bu tablolar ilk olarak Lakehouse ortamına yüklenebilir.

Daha sonra SQL veya Spark kullanılarak;

- hasar kayıtları temizlenebilir,
- prim tutarları kontrol edilebilir,
- müşteri ve poliçe kayıtları birleştirilebilir,
- toplam prim hesaplanabilir,
- toplam hasar hesaplanabilir,
- tekliften poliçeye dönüşüm oranı oluşturulabilir,
- yeni analitik tablolar hazırlanabilir.

Sonrasında Fact ve Dimension tabloları üzerinden Semantic Model oluşturularak Power BI raporu hazırlanabilir.

---

# 🎯 ETL mi ELT mi Daha İyi?

Bu sorunun tek bir doğru cevabı yoktur.

Doğru yaklaşım projenin ihtiyacına göre belirlenmelidir.

Karar verirken;

- veri hacmi,
- veri çeşitliliği,
- hedef platform,
- güvenlik gereksinimleri,
- işlem kapasitesi,
- maliyet,
- cloud kullanımı,
- veri kalitesi,
- Data Science ihtiyacı,
- gerçek zamanlı veri gereksinimi,
- governance politikaları,
- ham verinin saklanma ihtiyacı

gibi faktörler değerlendirilmelidir.

Bu nedenle:

> **“ETL mi daha iyi, ELT mi?”**

sorusundan ziyade;

> **“Bu proje ve veri mimarisi için hangi yaklaşım daha uygun?”**

sorusunu sormak daha doğrudur.

---

# 🧠 Bu Çalışmada Öğrendiklerim

Bu çalışma kapsamında;

- ETL ve ELT arasındaki farkları,
- Extract, Transform ve Load aşamalarını,
- veri dönüşümünün mimari üzerindeki etkisini,
- Data Warehouse ve Lakehouse yaklaşımlarını,
- Schema-on-Write ve Schema-on-Read kavramlarını,
- Bronze, Silver ve Gold katmanlarını,
- ham veri saklamanın avantaj ve risklerini,
- modern cloud platformlarında ELT'nin önemini,
- ETL ve ELT'nin birlikte kullanılabileceğini,
- Microsoft Fabric üzerinde ELT akışının nasıl kurulabileceğini

inceleme fırsatı buldum.

---

# 📌 Kısa Özet

```text
ETL
Extract → Transform → Load
Önce dönüştür, sonra yükle.

ELT
Extract → Load → Transform
Önce yükle, sonra dönüştür.
```

ETL daha kontrollü bir yükleme süreci sunarken, ELT modern cloud ve Lakehouse sistemlerinin işlem gücünden yararlanarak daha esnek veri işleme senaryoları oluşturulmasına imkân sağlayabilir.

Her iki yaklaşımın da avantajları ve dezavantajları bulunmaktadır.

Doğru seçim, kullanılan teknoloji ve iş gereksinimlerine göre yapılmalıdır.

---

## 📚 Kaynaklar

Bu araştırma sırasında aşağıdaki kaynakların resmi dokümantasyonlarından yararlanılmıştır:

- Microsoft Learn
- AWS Documentation
- Google Cloud Documentation
- IBM Data & AI
- Snowflake Documentation

---

⭐ **Shining Stars Learning Journey — Week 02**
