"""OdakKoçu'nun tool-calling agent döngüsü."""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from datetime import timedelta

from .state import now
from .tools import FocusToolbox

SYSTEM_PROMPT = """Sen OdakKoçu adlı sıcak, doğal ve Türkçe konuşan kişisel yardımcı ve verimlilik agent'ısın.
Kullanıcı seninle serbestçe sohbet edebilir; sadece görev veya rutin komutlarını bekleme. Onu dinle, bağlamı koru, sorusuna doğrudan cevap ver ve gerektiğinde soru sor.
Genel sohbet, düşünce paylaşımı, motivasyon, karar verme, fikir üretme ve günlük planlama isteklerinde doğal bir arkadaş gibi konuş.
Zamanlayıcı, görev, Pomodoro, rutin, not, fikir, hatırlatıcı, liste veya gün özeti hakkında gerçek veriye dayalı işlem gerektiğinde mutlaka uygun tool'u çağır.
Kullanıcı günlük rutin istediğinde önce görevleri listele, sonra plan_day çağır. Kullanıcı 'ne yapmalıyım' veya 'bugünüm nasıl' dediğinde daily_summary kullan.
Kullanıcı bir şeyi hatırlatmanı isterse add_reminder, aklında tutmanı isterse add_note kullan. Kullanıcı görev silmek isterse delete_task, seans geçmişi kaydı silmek isterse delete_session kullan ve silinen kaydı açıkça bildir.
Belirsiz bir istekte kısa ve doğal bir netleştirme sorusu sor. Kullanıcı istemedikçe komut listesi, hazır örnekler veya uzun yetenek açıklamaları gösterme.
Cevapların Türkçe, konuşma akışına uygun, empatik ve uygulanabilir olsun. Zaman bilgisini dakika ve saat olarak anlaşılır yaz."""


@dataclass
class AgentResult:
    answer: str
    tool_calls: list[str] = field(default_factory=list)
    mode: str = "demo"


class FocusAgent:
    def __init__(self, state_path: str = "data/odak-state.json", model: str | None = None) -> None:
        self.toolbox = FocusToolbox(state_path)
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-5-mini")
        self._client = None
        self._previous_response_id: str | None = None
        self._last_user_message = ""
        self._openai_unavailable = False
        if os.getenv("OPENAI_API_KEY"):
            try:
                from openai import OpenAI
                self._client = OpenAI()
            except ImportError:
                self._client = None

    @property
    def mode(self) -> str:
        return "openai" if self._client and not self._openai_unavailable else "demo"

    def run(self, message: str) -> AgentResult:
        if self._client and not self._openai_unavailable:
            try:
                return self._run_openai(message)
            except Exception:  # noqa: BLE001 - fall back to deterministic demo mode
                self._openai_unavailable = True
        return self._run_demo(message)

    def _run_openai(self, message: str) -> AgentResult:
        request = {"model": self.model, "instructions": SYSTEM_PROMPT, "input": message, "tools": self.toolbox.tool_schemas()}
        if self._previous_response_id:
            request["previous_response_id"] = self._previous_response_id
        response = self._client.responses.create(**request)
        calls = []
        for _ in range(8):
            function_calls = [item for item in response.output if item.type == "function_call"]
            if not function_calls:
                self._previous_response_id = response.id
                return AgentResult(response.output_text, calls, self.mode)
            outputs = []
            for item in function_calls:
                calls.append(item.name)
                result = self.toolbox.call(item.name, json.loads(item.arguments))
                outputs.append({"type": "function_call_output", "call_id": item.call_id, "output": json.dumps(result, ensure_ascii=False)})
            response = self._client.responses.create(model=self.model, instructions=SYSTEM_PROMPT, input=outputs, previous_response_id=response.id, tools=self.toolbox.tool_schemas())
        self._previous_response_id = response.id
        return AgentResult("İşlem adımlarının sınırına ulaştım; isteği biraz daha küçük parçalara bölelim.", calls, self.mode)

    def _run_demo(self, message: str) -> AgentResult:
        lower = message.lower()
        previous_message = self._last_user_message
        self._last_user_message = message
        calls = []
        if any(word in lower for word in ("merhaba", "selam", "hey", "günaydın", "iyi akşamlar")):
            answer = "Merhaba, buradayım. Aklından geçeni olduğu gibi anlatabilirsin; birlikte konuşur, gerekirse düzenler ve uygulamaya geçiririz."
        elif any(word in lower for word in ("nasılsın", "naber", "iyi misin")):
            answer = "İyiyim, buradayım ve seni dinliyorum. Sen bugün nasılsın?"
        elif any(phrase in lower for phrase in ("ben de iyiyim", "ben de iyi", "iyiyim aslında")):
            answer = "Buna sevindim 😊 Bugün sana iyi gelen bir şey oldu mu?"
        elif any(word in lower for word in ("teşekkür", "sağ ol", "eyvallah")):
            answer = "Rica ederim. Ne zaman istersen kaldığımız yerden devam ederiz."
        elif any(word in lower for word in ("moralim bozuk", "stresliyim", "yoruldum", "yorgunum", "odaklanamıyorum", "canım sıkkın")):
            answer = "Bayağı yorulmuşsun gibi geliyor 😌 Biraz yavaşlayalım; seni en çok ne yordu bugün?"
        elif any(word in lower for word in ("motivasyon", "cesaret ver", "gaza getir")):
            answer = "Her şeyi bir anda çözmek zorunda değilsin. Şu an sadece başlayabileceğin en küçük adımı seçelim; devamı geldikçe kolaylaşır."
        elif any(word in lower for word in ("yardım", "neler yapabilirsin", "ne yapabilirsin")):
            answer = "Buradayım. İstersen sohbet ederiz, istersen kafandaki işleri birlikte netleştiririz. Zamanını, notlarını, görevlerini ve planını da sen söylemeden gerektiğinde düzenleyebilirim."
        elif "hava" in lower or any(word in lower for word in ("soğuk", "serin", "sıcak", "yağmur", "güneşli")):
            answer = self._weather_reply(lower)
        elif any(word in lower for word in ("sıkıldım", "çok bunaldım", "keyfim yok")):
            answer = "Bazen böyle anlar geliyor. İstersen biraz laflayalım; aklını dağıtacak bir şey buluruz ya da seni bunaltan şeyi birlikte açarız."
        elif "dışarı" in lower and any(word in lower for word in ("istemiyorum", "çıkmak", "çıkmayacağım", "gitmek istem")):
            answer = "Anladım, bugün dışarı çıkmak pek içinden gelmiyor. Evde sakin bir şeyler yapmak mı istersin, yoksa biraz dinlenmeye mi ihtiyacın var?"
        elif any(word in lower for word in ("istemiyorum", "içimden gelmiyor", "canım istemiyor")):
            answer = "Anladım, şu an ona enerjin yok gibi. Kendini zorlamadan başka bir seçenek bulalım; ne yapmak istemediğini değil, şu an neyin iyi gelebileceğini düşünelim."
        elif any(word in lower for word in ("uykum var", "uyuyacağım", "uyuyamıyorum")):
            answer = "Bedenin biraz mola istiyor olabilir. Uyuyamıyorsan zihnini meşgul eden şeyi anlatabilirsin; uykuya geçeceksen de yarına kalanları birlikte sakinleştirebiliriz."
        elif any(word in lower for word in ("hatırlatıcılar", "hatırlatmalarım")):
            calls.append("list_reminders")
            result = self.toolbox.list_reminders()
            answer = "Bekleyen hatırlatıcı yok." if not result["reminders"] else "Bekleyen hatırlatıcılar:\n" + "\n".join(f"- {item['due_at'][11:16]} · {item['title']}" for item in result["reminders"])
        elif any(word in lower for word in ("hatırlat", "hatırlatıcı", "unutma")):
            calls.append("add_reminder")
            minutes = self._reminder_minutes(lower)
            title = re.sub(r"(bana|lütfen|şunu|hatırlatıcı|hatırlat|unutma|yarın|bugün|saat\s*\d{1,2}(?::\d{2})?)", "", message, flags=re.IGNORECASE)
            title = re.sub(r"\d+\s*(?:dakika|dk|saat)", "", title, flags=re.IGNORECASE).strip(" .,;-") or "Hatırlatıcı"
            result = self.toolbox.add_reminder(title, minutes)
            answer = f"Tamam, ‘{result['title']}’ için hatırlatıcı oluşturdum. Zamanı: {result['due_at'][11:16]}."
        elif any(word in lower for word in ("not al", "not düş", "aklımda", "fikir", "toplantı notu")):
            calls.append("add_note")
            category = "fikir" if "fikir" in lower else ("toplantı" if "toplantı" in lower else "not")
            content = re.sub(r"(not al|not düş|aklımda tut|aklımda|fikir:|toplantı notu:?)", "", message, flags=re.IGNORECASE).strip(" .,;-") or message.strip()
            result = self.toolbox.add_note(content, category)
            answer = f"Kaydettim. Bunu ‘{result['category']}’ başlığı altında sakladım."
        elif any(word in lower for word in ("notlarım", "fikirlerim", "kayıtlarım")):
            calls.append("list_notes")
            category = "fikir" if "fikir" in lower else ""
            result = self.toolbox.list_notes(category)
            answer = "Henüz kayıtlı not yok." if not result["notes"] else "Kayıtların:\n" + "\n".join(f"- {item['content']} ({item['category']})" for item in result["notes"][:8])
        elif any(word in lower for word in ("alışverişe ekle", "alışveriş listesi", "alışveriş listeme")):
            if "ekle" in lower:
                calls.append("add_list_item")
                item = re.sub(r".*?alışveriş(?:e| listeme| listesine)?\s*", "", message, flags=re.IGNORECASE).replace("ekle", "", 1).strip(" .,;-") or "Yeni madde"
                self.toolbox.add_list_item("alışveriş", item)
                answer = f"Alışveriş listesine ekledim: {item}"
            else:
                calls.append("list_items")
                result = self.toolbox.list_items("alışveriş")
                answer = "Alışveriş listen boş." if not result["items"] else "Alışveriş listen:\n" + "\n".join(f"- {item['text']}" for item in result["items"] if not item.get("completed"))
        elif any(word in lower for word in ("başlat", "pomodoro", "odaklan")):
            minutes = self._minutes(lower, 25)
            task = self._task_from_start(message)
            calls.append("start_timer")
            result = self.toolbox.start_timer(minutes, task)
            answer = result.get("error") or f"{result['task']} için {minutes} dakikalık odak seansı başladı. Bitiş: {result['ends_at'][11:16]}"
        elif any(word in lower for word in ("durdur", "bitir")):
            calls.append("stop_timer")
            result = self.toolbox.stop_timer()
            answer = result.get("message", f"{result.get('task', 'Odak seansı')} durumu: {result.get('status')}.")
        elif any(word in lower for word in ("duraklat", "beklet")):
            calls.append("pause_timer")
            result = self.toolbox.pause_timer()
            answer = result.get("error") or f"{result['task']} duraklatıldı. Kalan süre: {result['remaining_minutes']} dakika."
        elif any(word in lower for word in ("devam et", "sürdür", "kaldığın yerden")):
            calls.append("resume_timer")
            result = self.toolbox.resume_timer()
            answer = result.get("error") or f"{result['task']} devam ediyor. Yaklaşık {result['remaining_minutes']} dakika kaldı."
        elif any(word in lower for word in ("durum", "kaldı", "kaç dakika", "zamanlayıcı")):
            calls.append("timer_status")
            result = self.toolbox.timer_status()
            if result.get("status") == "running":
                answer = f"{result['task']} devam ediyor. Yaklaşık {result['remaining_minutes']} dakika kaldı."
            else:
                answer = result.get("message", f"Zamanlayıcı durumu: {result.get('status')}.")
        elif any(word in lower for word in ("görev ekle", "yapılacak ekle")):
            calls.append("add_task")
            title = re.sub(r".*?(görev ekle|yapılacak ekle)\s*", "", message, flags=re.IGNORECASE).strip() or "Yeni görev"
            minutes = self._minutes(lower, 25)
            priority = "high" if any(word in lower for word in ("yüksek", "önemli", "acil")) else ("low" if "düşük" in lower else "normal")
            title = re.sub(r"\d+\s*(?:dakika|dk)|yüksek öncelik|düşük öncelik|öncelikli|acil", "", title, flags=re.IGNORECASE).strip(" .,;-")
            result = self.toolbox.add_task(title or "Yeni görev", minutes, priority)
            answer = f"Görev eklendi: #{result['id']} {result['title']} · {result['minutes']} dk · {self._priority_label(result['priority'])}."
        elif any(word in lower for word in ("görevler", "yapılacaklar", "işlerimi göster")):
            calls.append("list_tasks")
            result = self.toolbox.list_tasks(True)
            open_tasks = [task for task in result["tasks"] if not task.get("completed")]
            done_tasks = [task for task in result["tasks"] if task.get("completed")]
            if not result["tasks"]:
                answer = "Henüz görev yok. Örneğin: görev ekle sunum hazırla 45 dakika yüksek öncelik."
            else:
                answer = f"Açık görevler: {len(open_tasks)} · Tamamlanan: {len(done_tasks)}\n" + "\n".join(f"#{task['id']} {task['title']} · {task['minutes']} dk" for task in open_tasks)
        elif any(word in lower for word in ("sil", "kaldır", "sileyim")) and any(word.isdigit() for word in lower.split()):
            match = re.search(r"(?:görev\s*)?(\d+)", lower)
            if "seans" in lower:
                calls.append("delete_session")
                result = self.toolbox.delete_session(int(match.group(1)) - 1)
                answer = result.get("error") or "Tamam, seans geçmişindeki kaydı sildim."
            else:
                calls.append("delete_task")
                result = self.toolbox.delete_task(int(match.group(1)))
                answer = result.get("error") or f"Tamam, ‘{result['deleted']['title']}’ görevini sildim."
        elif any(word in lower for word in ("tamamlandı", "tamamla", "bitti")):
            match = re.search(r"(?:görev\s*)?(\d+)", lower)
            if not match:
                answer = "Tamamlanan görevin numarasını da yazabilir misin? Örneğin: görev 2 tamamlandı."
            else:
                calls.append("complete_task")
                result = self.toolbox.complete_task(int(match.group(1)))
                answer = result.get("error", f"Tamamlandı: {result['title']}")
        elif any(word in lower for word in ("rutin", "planla", "günümü")):
            calls.extend(["list_tasks", "plan_day"])
            tasks = self.toolbox.list_tasks()
            result = self.toolbox.plan_day(self._minutes(lower, 240), self._start_time(lower))
            if not result.get("routine"):
                answer = result["message"] + (" Açık görev bulunmuyor." if not tasks["tasks"] else "")
            else:
                answer = "Bugünkü rutin:\n" + "\n".join(f"- {item['time']} | {item['title']} ({item['minutes']} dk)" for item in result["routine"])
        elif any(word in lower for word in ("özet", "ne yapmalıyım", "bugünüm nasıl", "bugün ne yapayım", "bugünkü işler")):
            calls.append("daily_summary")
            result = self.toolbox.daily_summary()
            answer = f"Bugünün özeti:\n• {result['open_tasks']} açık, {result['completed_tasks']} tamamlanmış görev\n• {result['focus_sessions']} odak seansı ({result['focus_minutes']} dakika)\n• {result['notes']} kayıtlı not\n• {result['reminders']} hatırlatıcı"
        elif any(word in lower for word in ("düzenle", "organize et", "çok işim var", "nereden başlayayım", "bana yardım et")):
            calls.append("daily_summary")
            result = self.toolbox.daily_summary()
            answer = f"Önce tabloyu sadeleştirelim: {result['open_tasks']} açık görev, {result['reminders']} hatırlatıcı ve {result['notes']} kayıtlı not var.\n\nÖnerim: en önemli görevi seçelim, ona bir süre verelim ve ilk Pomodoro’yu başlatalım. ‘Görevlerimi göster’ veya doğrudan ne yapman gerektiğini yazabilirsin."
        else:
            answer = self._conversational_reply(message, lower, previous_message)
        return AgentResult(answer, calls, self.mode)

    @staticmethod
    def _weather_reply(message: str) -> str:
        if any(word in message for word in ("soğuk", "serin")):
            return "Evet, bugün biraz serin hissettiriyor olabilir. Dışarı çıkacak mısın, yoksa günü içeride mi geçireceksin?"
        if "yağmur" in message:
            return "Yağmur havasının ayrı bir ruhu var. Sen böyle havaları seviyor musun, yoksa güneşli bir gün mü daha iyi geliyor?"
        if any(word in message for word in ("sıcak", "güneşli")):
            return "Güzel, biraz güneş iyi gelebilir. Böyle bir havada dışarı çıkmak mı istersin, yoksa sakin bir gün mü planlıyorsun?"
        return "Hava bugün nasıl gidiyor? Senin bulunduğun yerdeki durumu merak ettim."

    @staticmethod
    def _conversational_reply(message: str, lower: str, previous_message: str = "") -> str:
        if lower.startswith(("yok ", "yok,", "hayır ")) or lower.endswith((" gibi ya", " galiba", " sanırım")):
            return "Anladım 🙂 Biraz kararsız veya isteksiz gibisin. Acele etmeyelim; bugün sana en kolay gelecek şeyi seçebiliriz 🌿"
        if message.rstrip().endswith("?") or any(word in lower.split() for word in ("nasıl", "neden", "sence", "ne")):
            replies = (
                "Güzel bir soru 🤔 Bunu birlikte açalım; senin için en önemli kısmı ne?",
                "Bunu düşünmen çok normal 🙂 Sen şu an bu konuda ne hissediyorsun?",
                "Bence bunu adım adım konuşabiliriz 🌿 Aklındaki ilk düşünce ne?",
            )
            return replies[sum(map(ord, lower)) % len(replies)]
        if any(word in lower for word in ("bugün", "az önce", "şimdi", "sonra", "çünkü")):
            return "Anladım 🙂 Gününün içinden bir şeyi paylaşıyorsun. Bu durum sende nasıl bir his bıraktı?"
        if previous_message and any(word in previous_message.lower() for word in ("hava", "soğuk", "serin", "yağmur")):
            return "Anladım 🙂 Hava da ruh halini biraz etkilemiş olabilir. Şimdi sana iyi gelecek şey ne olurdu?"
        replies = (
            "Hımm, bunu duyunca merak ettim 🙂 Sen bu konuda ne düşünüyorsun?",
            "Seni takip ediyorum 🌿 Bu konu sende nasıl bir his uyandırdı?",
            "Bunu konuşmak güzel olabilir 😊 Aklında bununla ilgili başka ne var?",
        )
        return replies[sum(map(ord, lower)) % len(replies)]

    @staticmethod
    def _minutes(message: str, default: int) -> int:
        match = re.search(r"(\d+)\s*(?:dakika|dk)", message)
        if match:
            return int(match.group(1))
        hours = re.search(r"(\d+)\s*saat", message)
        return int(hours.group(1)) * 60 if hours else default

    @staticmethod
    def _task_from_start(message: str) -> str:
        task = re.sub(r"\d+\s*(?:dakika|dk)", "", message, flags=re.IGNORECASE)
        task = re.sub(r"\b(?:pomodoro|başlat|odaklanma|odaklan|için|bir)\b", "", task, flags=re.IGNORECASE)
        return " ".join(task.split()).strip(" .,?") or "Odaklanma"

    @staticmethod
    def _start_time(message: str) -> str:
        match = re.search(r"(?:saat|\bat)\s*(\d{1,2}(?::\d{2})?)", message)
        if not match:
            return "09:00"
        value = match.group(1)
        return value if ":" in value else f"{value}:00"

    @staticmethod
    def _priority_label(priority: str) -> str:
        return {"high": "yüksek öncelik", "low": "düşük öncelik", "normal": "normal öncelik"}.get(priority, priority)

    @staticmethod
    def _reminder_minutes(message: str) -> int:
        clock = re.search(r"saat\s*(\d{1,2})(?::(\d{2}))?", message)
        if clock:
            target = now().replace(hour=int(clock.group(1)), minute=int(clock.group(2) or 0), second=0, microsecond=0)
            if "yarın" in message or target <= now():
                target += timedelta(days=1)
            return max(1, int((target - now()).total_seconds() // 60))
        minute_match = re.search(r"(\d+)\s*(?:dakika|dk)", message)
        if minute_match:
            return int(minute_match.group(1))
        hour_match = re.search(r"(\d+)\s*saat", message)
        if hour_match:
            return int(hour_match.group(1)) * 60
        return 60
