# ☁️ Week 03 | Azure SQL & CRM Analytics

> Azure SQL üzerinde CRM verisi oluşturmak, veriyi modellemek ve Power BI ile anlamlı KPI'lara dönüştürmek.

Bu hafta odağım; yalnızca bir dashboard hazırlamak değil, verinin Azure SQL'de tutulduğu ve Power BI tarafından kullanıldığı daha gerçekçi bir CRM analitiği akışı oluşturmaktı.

---

## 🎯 Week 03 Assignment

- Azure hesabı oluşturmak
- Azure SQL üzerinde bir veritabanı oluşturmak
- CRM alanına yönelik örnek bir veri seti hazırlamak
- Veri setini Azure SQL veritabanına aktarmak
- Azure SQL ile Power BI bağlantısını kurmak
- CRM KPI'larını kullanarak interaktif bir dashboard hazırlamak

---

## 🧱 Data Model

CRM senaryosu için birden fazla tablo kullandım:

- `Customers`
- `Sales`
- `Leads`
- `Interactions`
- `SupportTickets`
- `Campaigns`
- `CampaignResponses`
- `Products`
- `ProductCategories`
- `Channels`
- `CustomerSegments`

Bu yapı sayesinde yalnızca satış verisini değil; müşteri, kampanya, etkileşim ve segment boyutlarını birlikte analiz edebildim.

---

## 📊 CRM KPIs

Dashboard üzerinde takip ettiğim temel CRM metrikleri:

| KPI | Sonuç |
|---|---:|
| Active Customers | 85 |
| Churn Rate | %16,67 |
| Conversion Rate | %40,00 |
| Repeat Purchase Rate | %68,18 |
| Average Order Value (AOV) | ₺11.235,00 |
| Purchase Frequency | 2,18 |
| Customer Lifetime Value (CLV) | ₺24.512,73 |
| Discount Rate | %15,91 |

---

## 📈 Additional Analyses

Temel KPI'ların yanında dashboard'a farklı analiz alanları da ekledim:

- Ürün kategorisine göre net ciro
- Müşteri segment dağılımı
- Aylık net ciro trendi
- Kampanya ROAS performansı
- Satış kanalına göre net ciro

Dashboard ayrıca:

- **Şehir**
- **Müşteri Segmenti**

filtreleriyle interaktif olarak kullanılabiliyor.

---

## ☁️ Azure SQL

CRM verilerini lokal bir dosyada bırakmak yerine Azure SQL üzerinde konumlandırdım.

Bu süreçte:

`Dataset → Azure SQL → Data Model → Power BI → CRM Dashboard`

şeklinde uçtan uca bir veri akışı oluşturdum.

Azure SQL tarafında tabloları oluşturduktan sonra örnek verileri aktardım ve Power BI Desktop üzerinden doğrudan veritabanına bağlandım.

---

## 📊 Power BI Dashboard

Dashboard tasarımında **navy + lilac** renk paleti kullandım.

Tasarımda özellikle:

- KPI kartlarının kolay okunabilir olmasına
- Grafiklerin birbiriyle tutarlı görünmesine
- CRM metriklerinin tek ekranda takip edilebilmesine
- Filtrelerin kullanıcı deneyimini desteklemesine
- Shining Stars görsel kimliğine uyum sağlamasına

odaklandım.

---

## 🛠️ Technologies

`Microsoft Azure`  
`Azure SQL Database`  
`SQL`  
`Power BI`  
`DAX`  
`Data Modeling`  
`CRM Analytics`

---

## 💡 What I Learned

Bu çalışma sayesinde yalnızca Power BI görselleştirmeleriyle değil, verinin kaynağından dashboard'a kadar olan süreçle ilgilenme fırsatı buldum.

Özellikle;

- Azure SQL üzerinde ilişkisel veri yapısı oluşturma,
- CRM verisini tablolara ayırma,
- tablolar arasında ilişkiler kurma,
- DAX ile KPI hesaplama,
- iş metriklerini görselleştirme,
- dashboard tasarımını kullanıcı açısından değerlendirme

konularında pratik yaptım.

---

## ✨ Key Takeaway

CRM analitiğinde önemli olan yalnızca veriyi göstermek değil;

**müşterinin davranışını, değerini, sadakatini ve kampanyalara verdiği tepkiyi birlikte okuyabilmek.**

Bu hafta Azure SQL ile Power BI'ı bir araya getirerek bu süreci uçtan uca deneyimlemiş oldum.

---

⭐ **Shining Stars Learning Journey — Week 03**
