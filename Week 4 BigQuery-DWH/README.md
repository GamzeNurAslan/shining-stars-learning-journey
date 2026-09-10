# ☁️ Week 4 — BigQuery & Data Warehouse DWH

> ⭐ **Shining Stars | Learning Journey**

Bu hafta odağım **Google BigQuery ve Data Warehouse** kavramlarını sadece teoride öğrenmek değil, gerçek veriler üzerinde deneyerek anlamaktı.

Çalışmayı şu akışta ilerlettim:

### 🔎 Research → ☁️ BigQuery → 🧱 Data Modeling → 📊 Analysis → 🚀 Project

---

## ☁️ BigQuery Experiment

Google Cloud **BigQuery Sandbox** üzerinde NYC Citi Bike public dataset'ini kullanarak küçük bir query optimization deneyi yaptım.

İlk sorguda işlenen veri:

```text
1.15 GB
```

Sadece gerçekten ihtiyacım olan sütunları seçtiğimde:

```text
667.06 MB
```

Daha sonra raw data'yı her seferinde yeniden sorgulamak yerine pre-aggregated bir analytics table oluşturdum:

```text
20.03 KB
```

### 📉 Result

```text
1.15 GB
   ↓
667.06 MB
   ↓
20.03 KB
```

Bu deney bana optimization'ın yalnızca daha kısa SQL yazmak olmadığını gösterdi.

> 💡 **Data modeling ve verinin nasıl hazırlandığı, query performance üzerinde çok büyük bir etkiye sahip.**

Ayrıca `LIMIT 100` kullanmanın scanned data miktarını tek başına azaltmadığını da test ederek gördüm.

---

## 🧱 Data Warehouse Perspective

Bu çalışma sayesinde şu kavramları uygulamalı olarak daha iyi anlamaya başladım:

`Data Modeling` • `Aggregate Tables` • `Analytical Layers` • `Query Optimization`

Kendime sorduğum soru da değişti:

> ❌ “Bu query'yi nasıl daha kısa yazarım?”

yerine:

> ✅ **“Aynı analizi her seferinde raw data üzerinden hesaplamak zorunda mıyım?”**

Bu bakış açısı benim için Data Warehouse mantığını çok daha anlaşılır hale getirdi.

---

## 📊 Job Market Analysis

Trend araştırması kapsamında Türkiye ve global pazardan seçtiğim **20 data-focused job posting** üzerinde küçük bir analiz yaptım.

İlanlarda geçen teknik yetkinlikleri dataset'e dönüştürüp BigQuery ve SQL ile analiz ettim.

Öne çıkan bazı skill'ler:

| Skill | Frequency |
|---|---:|
| 🗄️ SQL | 80% |
| 🐍 Python | 75% |
| 🛡️ Governance / Data Quality | 75% |
| ⚙️ CI/CD | 65% |
| ☁️ GCP | 60% |
| 🧱 Data Modeling | 60% |
| 🔍 BigQuery | 55% |

Buradaki en önemli çıkarımlarımdan biri:

> **Technologies don't work alone — they form a stack.**

```text
SQL
 ↓
Data Modeling
 ↓
dbt / Dataform
 ↓
Airflow
 ↓
Data Quality & Governance
```

Yani artık sadece **“Hangi teknolojiyi öğrenmeliyim?”** diye değil,

**“Bu teknolojiler gerçek bir data pipeline içerisinde nasıl birlikte çalışıyor?”**

diye düşünmeye başladım.

---

## 🕸️ Ontology & Knowledge Graph

Bu haftaki araştırmanın farklı bir bölümünde **Ontology, Knowledge Graph ve Semantic Layer** kavramlarını da inceledim.

Telecom domain'i için küçük bir model oluşturdum:

```text
Customer → Order → Product
Customer → Ticket → Issue Type
Customer → Churn Risk
```

Ardından ilişkileri **SPARQL** ile sorguladım.

Örnek:

```text
High Churn Risk
+
Connection Problem

↓

Customer101 → RouterX → Ticket77
```

Bu çalışma bana şu fikri düşündürdü:

> 🤖 **Giving an AI access to data is not always enough.  
> It may also need to understand what that data means.**

---

## 🤗 From Research to Project

Çalışmanın sadece bir rapor olarak kalmasını istemedim.

Bu nedenle araştırmayı farklı çıktılara dönüştürdüm:

- 📊 **Hugging Face Dataset** — Job Market data
- 🚀 **Hugging Face Space** — Türkiye vs Global interactive analysis
- 🕸️ **Semantic Data Demo** — Ontology & Knowledge Graph
- 💻 **GitHub** — Technical side of the project

Final workflow:

```text
🔎 Research
      ↓
📊 Dataset
      ↓
☁️ BigQuery
      ↓
🧱 Data Modeling
      ↓
📈 Analysis
      ↓
🤗 Interactive Project
```

---

## 🧭 My Learning Roadmap

```text
SQL + Data Modeling
        ↓
BigQuery
        ↓
dbt / Dataform
        ↓
Airflow
        ↓
Data Quality & Governance
        ↓
Knowledge Graph
        ↓
AI Agents
```

Bu haftadan sonra kendi learning approach'umu da şöyle tanımlıyorum:

### 🔎 Research → 🛠️ Build → 💥 Break → 📏 Measure → 🧠 Explain

---

## 🛠️ Tech Stack & Concepts

`SQL` • `Python` • `BigQuery` • `Data Warehouse`  
`Data Modeling` • `Data Quality` • `Governance`  
`Airflow` • `dbt / Dataform`  
`Ontology` • `Knowledge Graph` • `SPARQL`  
`Google Cloud` • `Hugging Face`

---

## ⭐ Final Takeaway

Bu hafta benim için sadece BigQuery üzerinde query çalıştırmak değildi.

Raw data'nın nasıl işlendiğini, data modeling'in neden önemli olduğunu ve iyi tasarlanmış bir analytical layer'ın performansı nasıl değiştirebildiğini uygulamalı olarak gördüm.

Aynı zamanda trendleri yalnızca takip etmek yerine onları **data ile ölçmeye ve küçük projelerle test etmeye** çalıştım.

> ⭐ **Don't just follow trends. Understand the data behind them.**

---

<div align="center">

### ⭐ Shining Stars — Week 4

## ☁️ BigQuery & Data Warehouse

**Learning by Building 🚀**

</div>
