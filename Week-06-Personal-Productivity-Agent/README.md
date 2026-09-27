# OdakKoçu

Pomodoro, görev listesi, notlar, hatırlatıcılar ve günlük rutin planlamasını tek bir Türkçe AI agent içinde birleştiren kişisel organizasyon asistanı.

## Ne yapabilir?

- İstenilen süreyle Pomodoro başlatır.
- Zamanlayıcının gerçek kalan süresini kontrol eder.
- Zamanlayıcıyı durdurur ve odak seansını kaydeder.
- Görev ekler ve açık görevleri listeler.
- Görevleri tamamlar; artık gerekmeyen görevleri arayüzden kalıcı olarak silebilir.
- Görev önceliklerine göre günlük rutin hazırlar.
- Günlük tamamlanan görev ve odak seansı özetini verir.
- Not, fikir ve toplantı kaydı tutar.
- Hatırlatıcı oluşturur ve bekleyenleri listeler.
- Alışveriş veya özel liste maddelerini saklar.
- Belirsiz istekleri açıklığa kavuşturur ve bir sonraki adımı önerir.
- Agent'ın kullandığı tool sırasını gösterir.
- Durumu `data/odak-state.json` dosyasında saklar.

## Kurulum

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
Copy-Item .env.example .env
```

## Demo modu

API anahtarı olmadan çalışır:

```powershell
python -m odak_kocu.cli "25 dakika matematik için Pomodoro başlat"
python -m odak_kocu.cli "zamanlayıcı durumu"
python -m odak_kocu.cli "görev ekle sunum hazırla"
python -m odak_kocu.cli "bugünkü rutinimi planla"
python -m odak_kocu.cli --chat
python -m odak_kocu.web
```

Tarayıcıda `http://127.0.0.1:8000` adresini açarak görsel dashboard'u kullanabilirsiniz.

## Gerçek LLM modu

`.env` içine `OPENAI_API_KEY` eklenince aynı tool'lar OpenAI Responses API kullanan agent tarafından seçilir:

```text
OPENAI_API_KEY=...
OPENAI_MODEL=gpt-5-mini
```

## Agent mimarisi

```text
Kullanıcı komutu
      |
      v
OdakKoçu agent
      |
      +--> start_timer / timer_status / stop_timer
      +--> add_task / list_tasks / complete_task
      +--> add_note / list_notes / add_reminder
      +--> add_list_item / list_items / plan_day / daily_summary
      |
      v
Kalıcı JSON durum dosyası + Türkçe cevap
```

## Proje yapısı

```text
src/odak_kocu/   agent, tool'lar, durum ve CLI
data/            kalıcı yerel durum dosyası
docs/            demo ve sonraki deploy planı
tests/           timer ve rutin davranış testleri
```

## Sunum akışı

Detaylı 3-5 dakikalık demo için [docs/demo-script.md](docs/demo-script.md) dosyasına bakın.
