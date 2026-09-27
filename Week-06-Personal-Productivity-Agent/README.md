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

---

## 🧩 Problem ve Çözüm Yaklaşımı

Gün içinde yapılacak işleri, çalışma sürelerini, notları ve hatırlatıcıları farklı yerlerde tutmak odağı bölüyor. Bu projede amaç; kullanıcının doğal Türkçe cümlelerle günlük işlerini yönetebileceği tek bir çalışma alanı oluşturmaktı.

Uygulama yalnızca yazılan cümleye cevap vermiyor. İsteğin türünü anlayıp gerekli işlemi gerçekleştiriyor, sonucu kaydediyor ve sonraki komutlarda bu bilgiyi kullanıyor.

Örneğin:

```text
“Yarın saat 10'da sunum için hatırlatıcı ekle”
                 ↓
İsteği analiz et
                 ↓
Hatırlatıcı oluştur
                 ↓
JSON durum dosyasına kaydet
                 ↓
Kullanıcıya zamanı bildir
```

Bu yapı sayesinde sohbet, gerçek bir uygulama durumuyla birlikte ilerliyor.

---

## 🛠️ Kullanılan Tool'lar

| Tool | Görevi |
| --- | --- |
| `start_timer` | Belirli süre ve görev için Pomodoro başlatır. |
| `timer_status` | Aktif timer'ın kalan süresini hesaplar. |
| `pause_timer` | Çalışan timer'ı duraklatır. |
| `resume_timer` | Duraklatılmış timer'ı devam ettirir. |
| `stop_timer` | Odak seansını bitirip geçmişe kaydeder. |
| `add_task` | Öncelik ve tahmini süreyle görev ekler. |
| `list_tasks` | Açık veya tamamlanmış görevleri listeler. |
| `complete_task` | Bir görevi tamamlandı olarak işaretler. |
| `delete_task` | Görevi ve bağlı rutin kaydını siler. |
| `plan_day` | Açık görevleri zaman bloklarına böler. |
| `add_note` / `list_notes` | Not, fikir ve toplantı kayıtlarını yönetir. |
| `add_reminder` / `list_reminders` | Hatırlatıcı oluşturur ve listeler. |
| `add_list_item` / `list_items` | Alışveriş veya özel listeleri yönetir. |
| `daily_summary` | Günün görev, seans, not ve hatırlatıcı özetini verir. |

Tool çağrılarının isimleri arayüzde gösterildiği için kullanıcı, uygulamanın isteğini nasıl işlediğini takip edebiliyor.

---

## ⏱️ Timer Mantığı

Timer arka planda sürekli çalışan bir işlem olarak tasarlanmadı. Başlangıç ve bitiş zamanları kaydediliyor:

```json
{
  "status": "running",
  "task": "Matematik çalışması",
  "duration_minutes": 25,
  "started_at": "2026-09-27T10:00:00+03:00",
  "ends_at": "2026-09-27T10:25:00+03:00"
}
```

Kullanıcı durum sorguladığında kalan süre `ends_at - şu an` hesabıyla yeniden bulunuyor. Böylece uygulama kapatılıp tekrar açılsa bile zaman bilgisi kaybolmuyor.

Timer akışındaki durumlar:

```text
idle → running → paused → running → stopped
                    └──────────────→ completed
```

Bu yaklaşım, hem komut satırı hem de web arayüzü tarafından aynı durum bilgisinin kullanılmasını sağlıyor.

---

## 🗃️ Kalıcı Veri Yönetimi

Uygulama başlangıçta harici bir veritabanına ihtiyaç duymadan çalışıyor. Veriler `data/odak-state.json` dosyasında tutuluyor.

Dosyada aşağıdaki bölümler bulunuyor:

```text
timer       → aktif veya son timer bilgisi
tasks       → görevler ve tamamlanma durumları
routine     → günlük plan blokları
sessions    → tamamlanan odak seansları
notes       → not ve fikir kayıtları
reminders   → bekleyen hatırlatıcılar
lists       → alışveriş ve özel listeler
```

`StateStore` katmanı dosyanın okunması, varsayılan alanların oluşturulması ve güvenli biçimde kaydedilmesinden sorumlu. Böylece iş mantığı doğrudan dosya işlemlerine bağımlı kalmıyor.

---

## 🔄 Örnek Kullanım Senaryosu

Kullanıcının güne başlamasından gün sonu özetine kadar örnek akış:

```text
1. “Görev ekle veri yapıları çalış 60 dakika yüksek öncelik”
       ↓
2. “Görevlerimi göster”
       ↓
3. “Bugünkü rutinimi planla”
       ↓
4. “25 dakika veri yapıları için Pomodoro başlat”
       ↓
5. “Zamanlayıcı durumu”
       ↓
6. “Pomodoro'yu durdur”
       ↓
7. “Bugünüm nasıl?”
```

Bu akışın sonunda görev, rutin ve odak seansı aynı durum dosyasında saklanıyor. Günlük özet de bu kayıtları birlikte değerlendiriyor.

---

## 🧠 İki Çalışma Modu

### Demo modu

API anahtarı olmadan çalışır. Sık kullanılan Türkçe komutları yerel kurallarla tanır ve uygulamanın temel özelliklerini denemeye izin verir. Geliştirme ve sunum sırasında hızlı bir başlangıç sağlar.

### Gerçek LLM modu

`.env` içinde API anahtarı bulunduğunda doğal dil istekleri için Responses API kullanılır. Model, tanımlı tool şemalarını görür ve gerektiğinde bir veya birden fazla aracı sırayla çağırır.

```text
Kullanıcı isteği
      ↓
Model kararı
      ↓
Tool çağrısı
      ↓
Gerçek veri güncellemesi
      ↓
Türkçe sonuç
```

API erişilemez olduğunda uygulama kontrollü biçimde demo moduna döner. Böylece temel kullanım tamamen durmaz.

---

## 🌐 API Uçları

Web katmanı, dashboard ile çekirdek uygulama arasında küçük bir HTTP API sunuyor:

| Metot | Uç | Açıklama |
| --- | --- | --- |
| `GET` | `/` | Dashboard sayfasını açar. |
| `GET` | `/api/state` | Timer, görev, rutin ve özet durumunu döndürür. |
| `POST` | `/api/command` | Türkçe kullanıcı komutunu çalıştırır. |
| `POST` | `/api/tasks` | Form üzerinden doğrudan görev oluşturur. |
| `DELETE` | `/api/sessions/<index>` | Seans geçmişindeki kaydı siler. |

Komut endpoint'i hem cevabı hem kullanılan tool listesini hem de güncel durumu birlikte döndürür. Bu yapı, arayüzün yeni bir işlemden sonra sayfayı yeniden yüklemeden güncellenmesine yardımcı oluyor.

---

## 🎨 Web Arayüzü Yaklaşımı

Dashboard'da önemli bilgiler tek bakışta görülebilecek şekilde ayrıldı:

- üst bölümde aktif timer ve kalan süre,
- görevler bölümünde öncelik ve tamamlanma durumu,
- günlük özet bölümünde toplam çalışma ve görev sayıları,
- notlar ve hatırlatıcılar için ayrı kartlar,
- tamamlanan seanslar için geçmiş görünümü.

Arayüz JavaScript ile API'den gelen durumu yeniliyor. Python tarafındaki tool'lar ve web tarafındaki ekran aynı `FocusAgent` ve `FocusToolbox` nesneleri üzerinden çalıştığı için iki kullanım biçimi arasında veri tutarsızlığı oluşmuyor.

---

## 🧪 Test Senaryoları

Projede temel iş akışlarını kontrol eden dokuz test bulunuyor. Testlerde her senaryo için geçici bir JSON durum dosyası kullanılıyor; böylece gerçek kullanıcı verisi değiştirilmeden işlemler deneniyor.

Kontrol edilen başlıklar:

| Alan | Kontrol |
| --- | --- |
| Timer | Başlatma, durum sorgulama, duraklatma ve devam ettirme |
| Görev | Ekleme, listeleme, tamamlama ve silme |
| Rutin | Önceliğe göre zaman blokları oluşturma |
| Notlar | Not ve fikir kaydetme, listeleme |
| Hatırlatıcı | Süre hesaplama ve kayıt oluşturma |
| Listeler | Alışveriş listesine madde ekleme |
| Sohbet | Günlük ve doğal konuşma akışının korunması |
| Seans | Odak geçmişindeki kayıtların silinmesi |

Son kontrol sonucu: `9 passed` ve Ruff kontrolleri temiz.

---

## 🔐 Konfigürasyon ve Güvenlik

- Gerçek API anahtarı yalnızca yerel `.env` dosyasında tutulur.
- `.env`, `data/`, `.venv/`, cache klasörleri ve log dosyaları `.gitignore` ile dışarıda bırakılır.
- Reposuna yalnızca boş değerler içeren `.env.example` dosyası eklenir.
- Uygulama varsayılan olarak `127.0.0.1:8000` üzerinde çalışır.
- Üretim ortamına geçerken JSON yerine daha kontrollü bir veri tabanı ve ortam değişkeni yönetimi kullanılmalıdır.

---

## 📌 Tasarım Kararları

### Neden önce JSON dosyası?

Projenin hedefi hızlıca çalışan bir ürün ortaya koymaktı. JSON dosyası sayesinde veritabanı kurulumu olmadan timer, görev ve not akışları test edilebildi. `StateStore` katmanı ileride SQLite, PostgreSQL veya bir cloud storage servisiyle değiştirilebilecek şekilde ayrıştırıldı.

### Neden hem CLI hem web arayüzü?

Komut satırı, agent ve tool akışını hızlı test etmek için pratik. Web dashboard ise aynı işlevleri görsel olarak incelemeyi ve sunum sırasında uygulamayı daha anlaşılır göstermeyi sağlıyor.

### Neden demo modu?

Bir uygulamanın dış servise erişim olmadan da temel işlevlerini gösterebilmesi geliştirme sürecini kolaylaştırıyor. Demo modu, bağlantı veya anahtar problemi olduğunda projeyi tamamen kullanılamaz hâle getirmiyor.

---

## 🚧 Sonraki Adımlar

- JSON state yerine SQLite veya PostgreSQL kullanmak
- Kullanıcı bazlı hesap ve veri izolasyonu eklemek
- Hatırlatıcılar için gerçek bildirim sistemi oluşturmak
- Dashboard'a haftalık grafikler eklemek
- Görevleri sürükle-bırak ile yeniden sıralamak
- Timer ve rutin için mobil uyumlu görünümü geliştirmek
- API ve web katmanı için daha kapsamlı entegrasyon testleri yazmak
- Uygulamayı Docker ile tek komutla çalıştırmak

---

## ✨ Genel Değerlendirme

Bu çalışma, doğal dil ile gerçek uygulama durumunun bir araya geldiği küçük ama tamamlanabilir bir ürün örneği oldu. Kullanıcıdan gelen bir cümle; analiz, tool seçimi, veri güncellemesi ve anlaşılır bir cevap döngüsünden geçiyor.

Haftanın sonunda elimde yalnızca bir fikir değil; kurulabilen, test edilebilen, komut satırından ve tarayıcıdan kullanılabilen bir kişisel verimlilik uygulaması bulunuyor. 🚀
