# ☁️ Week 4 — BigQuery & Data Warehouse DWH

> ⭐ **Shining Stars | Learning Journey**

This week, I focused on **Google BigQuery and Data Warehouse concepts** through hands-on experiments and a small data project.

Instead of learning only from theory, I worked with real datasets, tested query optimization, explored analytical data modeling, and transformed my findings into a visible project.

### 🔎 Research → ☁️ BigQuery → 🧱 Data Modeling → 📊 Analysis → 🚀 Project

---

## ☁️ BigQuery Experiment

I used **Google Cloud BigQuery Sandbox** with the NYC Citi Bike public dataset to understand how query design affects the amount of data processed.

My first query processed approximately:

```text
1.15 GB
```

After selecting only the necessary columns:

```text
667.06 MB
```

Then, instead of repeatedly querying the raw data, I created a pre-aggregated analytical table.

The processed data dropped to:

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

This experiment showed me that query optimization is not only about writing shorter SQL.

> 💡 **How data is modeled and prepared can make a much bigger difference.**

---

## 🧪 Does LIMIT Reduce Data Scanned?

I also tested whether adding:

```sql
LIMIT 100
```

would reduce the amount of processed data.

The result remained:

```text
667.06 MB
```

even after removing `LIMIT`.

This helped me understand that:

> **LIMIT reduces the number of rows returned, but it does not necessarily reduce the amount of data scanned.**

---

## 🧱 Data Warehouse Perspective

The biggest difference appeared when I stopped querying raw data repeatedly and created an analytical summary table.

This made concepts such as:

- 🧱 Data Modeling
- ⭐ Star Schema
- 📦 Aggregate Tables
- 📊 Analytical Layers
- ⚡ Query Optimization

much more meaningful.

Instead of only asking:

> “How can I make this query faster?”

I started asking:

> **“Do I really need to calculate the same analytical result from raw data every time?”**

---

## 📊 Job Market Analysis

I also analyzed **20 data-focused job postings from Türkiye and the global market**.

I converted technical requirements into a small dataset and analyzed them using BigQuery and SQL.

Some of the strongest signals were:

| Skill | Frequency |
|---|---:|
| 🗄️ SQL | 80% |
| 🐍 Python | 75% |
| 🛡️ Governance / Data Quality | 75% |
| ⚙️ CI/CD | 65% |
| ☁️ GCP | 60% |
| 🧱 Data Modeling | 60% |
| 🔍 BigQuery | 55% |

One of my main observations was that technologies usually do not appear alone.

They form a stack:

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

This changed my learning perspective from:

**“Which technology should I learn?”**

to:

**“How do these technologies work together in a real data system?”**

---

## 🕸️ Exploring Ontology & Knowledge Graphs

As part of my trend research, I also explored:

`Ontology` • `Knowledge Graphs` • `Semantic Layer` • `SPARQL`

I created a small Telecom-focused model:

```text
Customer → Order → Product
Customer → Ticket → Issue Type
Customer → Churn Risk
```

Then I queried these relationships using **SPARQL**.

Example:

```text
High Churn Risk
+
Connection Problem

↓

Customer101 → RouterX → Ticket77
```

This introduced me to the idea that giving an AI system access to data may not always be enough.

It may also need to understand **what the data means and how different entities are related**. 🤖

---

## 🤗 Turning the Research into a Project

I did not want this week's work to remain only as a report.

So I transformed the research into visible outputs:

- 📊 **Hugging Face Dataset** — job market data
- 🚀 **Hugging Face Space** — interactive Türkiye vs Global analysis
- 🕸️ **Semantic Data Demo** — Ontology & Knowledge Graph experiment
- 💻 **GitHub** — technical implementation

The final workflow became:

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

My new learning approach is:

### 🔎 Research → 🛠️ Build → 💥 Break → 📏 Measure → 🧠 Explain

---

## 🛠️ Technologies & Concepts

`SQL` • `Python` • `BigQuery` • `Data Warehouse`  
`Data Modeling` • `Data Quality` • `Governance`  
`Airflow` • `dbt / Dataform`  
`Ontology` • `Knowledge Graph` • `SPARQL`  
`Hugging Face` • `Google Cloud`

---

## ⭐ Final Takeaway

This week helped me understand that working with data is not only about writing queries.

It is also about:

**how the data is modeled, how efficiently it is processed, how reliable it is, and how it can be transformed into something useful.**

> ☁️ **From raw data to meaningful insights.**

---

<div align="center">

### ⭐ Shining Stars — Week 4

## ☁️ BigQuery & Data Warehouse

**COMPLETED ✨**

</div>
