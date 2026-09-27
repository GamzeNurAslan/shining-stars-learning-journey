# ⏱️ Week 6 — Personal Productivity Agent

Bu hafta kişisel verimlilik, tool kullanımı ve kalıcı durum yönetimi üzerine çalıştım.

Haftanın uygulamasında; Pomodoro, görev listesi, notlar, hatırlatıcılar ve günlük rutin planlamasını tek bir Türkçe kişisel verimlilik uygulamasında birleştirdim. Kullanıcı ister komut satırından ister web arayüzünden gününü planlayabiliyor, görevlerini takip edebiliyor ve odak seanslarını kaydedebiliyor.

---

## 🧭 Uygulama Akışı

```text
Kullanıcı mesajı
      ↓
OdakKoçu
      ↓
Mesajı anlama ve uygun tool'u seçme
      ↓
┌─────────────────────────────────────────────┐
│ Zamanlayıcı  │ Görevler  │ Notlar            │
│ Hatırlatıcı  │ Listeler  │ Günlük özet       │
└─────────────────────────────────────────────┘
      ↓
Kalıcı JSON durum dosyası + Türkçe cevap
```

---

## 🎯 Uygulamanın Yapabildikleri

- Belirlenen süreyle Pomodoro başlatma
- Zamanlayıcının gerçek kalan süresini kontrol etme
- Odak seansını duraklatma, devam ettirme ve kaydetme
- Görev ekleme, listeleme, tamamlama ve silme
- Görev önceliklerine göre günlük rutin oluşturma
- Not, fikir ve toplantı kaydı tutma
- Hatırlatıcı oluşturma ve bekleyen hatırlatıcıları listeleme
- Alışveriş ve özel listelere madde ekleme
- Günlük görev ve odak özeti oluşturma
- Aynı işlevleri web dashboard üzerinden kullanma

---

## 🧰 Kullanılan Teknolojiler

`Python` • `Flask` • `OpenAI Responses API` • `JSON State Management` • `Pytest` • `Ruff` • `HTML` • `CSS` • `JavaScript`

---

## 🗂️ Proje Yapısı

```text
Week-06-Personal-Productivity-Agent/
│
├── src/odak_kocu/
│   ├── agent.py       # Agent akışı ve doğal dil komutları
│   ├── cli.py         # Komut satırı arayüzü
│   ├── state.py       # Kalıcı durum yönetimi
│   ├── tools.py       # Görev, timer, not ve liste araçları
│   └── web.py         # Flask web sunucusu ve API uçları
│
├── web/
│   ├── index.html      # Dashboard arayüzü
│   ├── app.js          # Arayüz etkileşimleri
│   └── assets/         # Uygulama görselleri
│
├── tests/
│   └── test_focus.py   # Timer, görev ve agent testleri
│
├── docs/
│   ├── demo-script.md  # Demo akışı
│   └── deployment.md   # Yayınlama notları
│
├── .env.example
├── pyproject.toml
└── README.md
```

---

## 🚀 Kurulum

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
Copy-Item .env.example .env
```

API anahtarı olmadan demo modu kullanılabilir. Gerçek LLM modu için `.env` dosyasına kendi API anahtarını eklemek gerekir.

---

## 💬 Komut Satırı Kullanımı

```powershell
python -m odak_kocu.cli "25 dakika matematik için Pomodoro başlat"
python -m odak_kocu.cli "görev ekle sunum hazırla 45 dakika yüksek öncelik"
python -m odak_kocu.cli "bugünkü rutinimi planla"
python -m odak_kocu.cli "zamanlayıcı durumu"
python -m odak_kocu.cli --chat
```

---

## 🌐 Web Dashboard

```powershell
python -m odak_kocu.web
```

Ardından tarayıcıdan `http://127.0.0.1:8000` adresi açılır.

Dashboard üzerinden:

- aktif zamanlayıcı görülebilir,
- görev eklenebilir ve tamamlanabilir,
- günlük özet incelenebilir,
- notlar ve hatırlatıcılar takip edilebilir,
- tamamlanan odak seansları görüntülenebilir.

---

## 🧪 Testler

```powershell
python -m pytest -q
ruff check src tests
```

Test kapsamı:

- Timer başlatma ve kalan süre kontrolü
- Timer duraklatma ve devam ettirme
- Görev ve günlük rutin oluşturma
- Not, hatırlatıcı ve liste işlemleri
- Görev ve seans silme
- Doğal sohbet akışının korunması

---

## ✨ Haftadan Kalan

Bu hafta benim için en önemli kazanım, bir uygulamanın yalnızca cevap üretmesinin yeterli olmadığını görmekti. Kullanıcı isteğini anlaması, doğru aracı seçmesi, yaptığı işlemi kalıcı olarak kaydetmesi ve sonraki komutlarda bu durumu koruması gerekiyor.

Kısacası bu hafta; fikir aşamasındaki bir verimlilik yardımcısını, çalışan bir komut satırı aracı ve web dashboard'u olan küçük bir ürüne dönüştürdüm. 🚀📚
