# OdakKoçu demo akışı

## Problem

Öğrenci ne çalışacağını ve ne kadar süre çalışacağını planlamakta zorlanıyor. OdakKoçu görevleri zaman bloklarına böler, Pomodoro başlatır ve günün durumunu takip eder.

## Tool'lar

| Tool | Görevi |
| --- | --- |
| `start_timer` | Pomodoro başlatır. |
| `timer_status` | Gerçek kalan süreyi hesaplar. |
| `stop_timer` | Seansı kaydederek durdurur. |
| `add_task` | Görev ve tahmini süre ekler. |
| `plan_day` | Öncelikli görevleri saatli rutine çevirir. |
| `daily_summary` | Günün verimlilik özetini verir. |

## Canlı demo

```powershell
python -m odak_kocu.cli "25 dakika veri yapıları için Pomodoro başlat"
python -m odak_kocu.cli "görev ekle algoritma ödevini bitir"
python -m odak_kocu.cli "görev ekle sunum slaytlarını hazırla"
python -m odak_kocu.cli "bugünkü rutinimi planla"
python -m odak_kocu.cli "zamanlayıcı durumu"
```

Etkileşimli demo için:

```powershell
python -m odak_kocu.cli --chat
```

Sunumda özellikle şu üç noktayı gösterin: agent'ın tool seçmesi, zamanın gerçek saate göre azalması ve durumun ayrı komutlarda korunması.
