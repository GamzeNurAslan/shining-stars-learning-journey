"""OdakKoçu'nun gerçek iş yapan araçları."""

from __future__ import annotations

from datetime import datetime, timedelta

from .state import ISTANBUL, StateStore, now


class FocusToolbox:
    def __init__(self, state_path: str = "data/odak-state.json") -> None:
        self.store = StateStore(state_path)

    def start_timer(self, minutes: int = 25, task: str = "Odaklanma") -> dict:
        data = self.store.load()
        current = data.get("timer")
        if current and current.get("status") == "running":
            return {"error": "Zaten çalışan bir zamanlayıcı var.", "timer": current}
        minutes = max(1, min(int(minutes), 180))
        started = now()
        timer = {"status": "running", "task": task.strip() or "Odaklanma", "duration_minutes": minutes, "started_at": started.isoformat(), "ends_at": (started + timedelta(minutes=minutes)).isoformat()}
        data["timer"] = timer
        self.store.save(data)
        return self._timer_view(timer)

    def timer_status(self) -> dict:
        data = self.store.load()
        timer = data.get("timer")
        if not timer:
            return {"status": "idle", "message": "Şu anda çalışan bir zamanlayıcı yok."}
        if timer.get("status") == "running":
            end = datetime.fromisoformat(timer["ends_at"])
            if now() >= end:
                timer["status"] = "completed"
                data["timer"] = timer
                data.setdefault("sessions", []).append({**timer, "completed_at": now().isoformat()})
                self.store.save(data)
        return self._timer_view(timer)

    def stop_timer(self) -> dict:
        data = self.store.load()
        timer = data.get("timer")
        if not timer or timer.get("status") not in {"running", "paused"}:
            return {"status": "idle", "message": "Durdurulacak çalışan veya duraklatılmış zamanlayıcı yok."}
        timer["status"] = "stopped"
        timer["stopped_at"] = now().isoformat()
        data["timer"] = timer
        data.setdefault("sessions", []).append(timer)
        self.store.save(data)
        return self._timer_view(timer)

    def pause_timer(self) -> dict:
        data = self.store.load()
        timer = data.get("timer")
        if not timer or timer.get("status") != "running":
            return {"error": "Duraklatılacak çalışan bir zamanlayıcı yok."}
        remaining = max(0, int((datetime.fromisoformat(timer["ends_at"]) - now()).total_seconds()))
        timer["status"] = "paused"
        timer["remaining_seconds"] = remaining
        timer["paused_at"] = now().isoformat()
        data["timer"] = timer
        self.store.save(data)
        return self._timer_view(timer)

    def resume_timer(self) -> dict:
        data = self.store.load()
        timer = data.get("timer")
        if not timer or timer.get("status") != "paused":
            return {"error": "Devam ettirilecek duraklatılmış bir zamanlayıcı yok."}
        remaining = max(1, int(timer.get("remaining_seconds", 0)))
        timer["status"] = "running"
        timer["ends_at"] = (now() + timedelta(seconds=remaining)).isoformat()
        data["timer"] = timer
        self.store.save(data)
        return self._timer_view(timer)

    def add_task(self, title: str, minutes: int = 25, priority: str = "normal") -> dict:
        data = self.store.load()
        task_id = max([int(item.get("id", 0)) for item in data.get("tasks", [])] or [0]) + 1
        task = {"id": task_id, "title": title.strip(), "minutes": max(5, min(int(minutes), 480)), "priority": priority if priority in {"low", "normal", "high"} else "normal", "completed": False, "created_at": now().isoformat()}
        data.setdefault("tasks", []).append(task)
        self.store.save(data)
        return task

    def list_tasks(self, include_completed: bool = False) -> dict:
        tasks = self.store.load().get("tasks", [])
        if not include_completed:
            tasks = [task for task in tasks if not task.get("completed")]
        return {"tasks": tasks, "count": len(tasks)}

    def complete_task(self, task_id: int) -> dict:
        data = self.store.load()
        for task in data.get("tasks", []):
            if task.get("id") == int(task_id):
                task["completed"] = True
                task["completed_at"] = now().isoformat()
                self.store.save(data)
                return task
        return {"error": "Bu numarada görev bulunamadı."}

    def delete_task(self, task_id: int) -> dict:
        data = self.store.load()
        tasks = data.get("tasks", [])
        for index, task in enumerate(tasks):
            if task.get("id") == int(task_id):
                deleted = tasks.pop(index)
                data["tasks"] = tasks
                data["routine"] = [item for item in data.get("routine", []) if item.get("task_id") != int(task_id)]
                self.store.save(data)
                return {"deleted": deleted}
        return {"error": "Bu numarada görev bulunamadı."}

    def plan_day(self, available_minutes: int = 240, start_time: str = "09:00") -> dict:
        data = self.store.load()
        tasks = [task for task in data.get("tasks", []) if not task.get("completed")]
        tasks.sort(key=lambda task: {"high": 0, "normal": 1, "low": 2}.get(task.get("priority"), 1))
        if not tasks:
            return {"routine": [], "message": "Önce planlamak istediğin görevleri ekleyelim."}
        try:
            cursor = datetime.strptime(start_time, "%H:%M").replace(tzinfo=ISTANBUL)
        except ValueError:
            cursor = datetime.strptime("09:00", "%H:%M").replace(tzinfo=ISTANBUL)
        remaining = max(25, int(available_minutes))
        routine = []
        for task in tasks:
            if remaining < 25:
                break
            block = min(task["minutes"], remaining, 50)
            routine.append({"time": cursor.strftime("%H:%M"), "title": task["title"], "minutes": block, "task_id": task["id"]})
            cursor += timedelta(minutes=block)
            remaining -= block
            if remaining >= 5:
                routine.append({"time": cursor.strftime("%H:%M"), "title": "Mola", "minutes": 5, "type": "break"})
                cursor += timedelta(minutes=5)
                remaining -= 5
        data["routine"] = routine
        self.store.save(data)
        return {"routine": routine, "planned_minutes": available_minutes - remaining}

    def daily_summary(self) -> dict:
        data = self.store.load()
        tasks = data.get("tasks", [])
        sessions = data.get("sessions", [])
        return {"open_tasks": len([task for task in tasks if not task.get("completed")]), "completed_tasks": len([task for task in tasks if task.get("completed")]), "focus_sessions": len(sessions), "focus_minutes": sum(int(session.get("duration_minutes", 0)) for session in sessions), "notes": len(data.get("notes", [])), "reminders": len(data.get("reminders", [])), "routine": data.get("routine", [])}

    def delete_session(self, session_index: int) -> dict:
        data = self.store.load()
        sessions = data.get("sessions", [])
        index = int(session_index)
        if index < 0 or index >= len(sessions):
            return {"error": "Bu numarada seans bulunamadı."}
        deleted = sessions.pop(index)
        data["sessions"] = sessions
        self.store.save(data)
        return {"deleted": deleted}

    def add_note(self, content: str, category: str = "not") -> dict:
        data = self.store.load()
        notes = data.setdefault("notes", [])
        note = {"id": max([int(item.get("id", 0)) for item in notes] or [0]) + 1, "content": content.strip(), "category": category.strip() or "not", "created_at": now().isoformat()}
        notes.append(note)
        self.store.save(data)
        return note

    def list_notes(self, category: str = "") -> dict:
        notes = self.store.load().get("notes", [])
        if category:
            notes = [note for note in notes if note.get("category") == category]
        return {"notes": list(reversed(notes)), "count": len(notes)}

    def add_reminder(self, title: str, minutes_from_now: int = 60) -> dict:
        data = self.store.load()
        reminders = data.setdefault("reminders", [])
        due = now() + timedelta(minutes=max(1, min(int(minutes_from_now), 10080)))
        reminder = {"id": max([int(item.get("id", 0)) for item in reminders] or [0]) + 1, "title": title.strip(), "due_at": due.isoformat(), "completed": False, "created_at": now().isoformat()}
        reminders.append(reminder)
        self.store.save(data)
        return reminder

    def list_reminders(self, include_completed: bool = False) -> dict:
        reminders = self.store.load().get("reminders", [])
        if not include_completed:
            reminders = [reminder for reminder in reminders if not reminder.get("completed")]
        for reminder in reminders:
            due = datetime.fromisoformat(reminder["due_at"])
            reminder["status"] = "vakti geldi" if now() >= due else "bekliyor"
        reminders.sort(key=lambda reminder: reminder["due_at"])
        return {"reminders": reminders, "count": len(reminders)}

    def add_list_item(self, list_name: str, item: str) -> dict:
        data = self.store.load()
        lists = data.setdefault("lists", {})
        values = lists.setdefault(list_name.strip() or "genel", [])
        entry = {"id": len(values) + 1, "text": item.strip(), "completed": False, "created_at": now().isoformat()}
        values.append(entry)
        self.store.save(data)
        return {"list_name": list_name, "item": entry}

    def list_items(self, list_name: str = "all") -> dict:
        lists = self.store.load().get("lists", {})
        if list_name == "all":
            return {"lists": lists, "count": sum(len(items) for items in lists.values())}
        items = lists.get(list_name, [])
        return {"list_name": list_name, "items": items, "count": len(items)}

    @staticmethod
    def _timer_view(timer: dict) -> dict:
        result = dict(timer)
        if timer.get("status") == "running":
            seconds = max(0, int((datetime.fromisoformat(timer["ends_at"]) - now()).total_seconds()))
            result["remaining_seconds"] = seconds
            result["remaining_minutes"] = (seconds + 59) // 60
        elif timer.get("status") == "paused":
            seconds = max(0, int(timer.get("remaining_seconds", 0)))
            result["remaining_minutes"] = (seconds + 59) // 60
        return result

    def tool_schemas(self) -> list[dict]:
        integer = {"type": "integer"}
        return [self._function("start_timer", "Belirli dakika ve görev için Pomodoro başlat.", {"minutes": integer, "task": {"type": "string"}}, ["minutes", "task"]), self._function("timer_status", "Çalışan zamanlayıcının kalan süresini kontrol et.", {}, []), self._function("pause_timer", "Çalışan Pomodoro'yu duraklat.", {}, []), self._function("resume_timer", "Duraklatılmış Pomodoro'yu devam ettir.", {}, []), self._function("stop_timer", "Çalışan veya duraklatılmış Pomodoro'yu bitir ve kaydet.", {}, []), self._function("add_task", "Günlük görev listesine görev ekle.", {"title": {"type": "string"}, "minutes": integer, "priority": {"type": "string", "enum": ["low", "normal", "high"]}}, ["title", "minutes", "priority"]), self._function("list_tasks", "Görevleri listele.", {"include_completed": {"type": "boolean"}}, ["include_completed"]), self._function("complete_task", "Numarası verilen görevi tamamlandı olarak işaretle.", {"task_id": integer}, ["task_id"]), self._function("delete_task", "Numarası verilen görevi ve varsa rutin kaydını kalıcı olarak sil.", {"task_id": integer}, ["task_id"]), self._function("delete_session", "Seans geçmişindeki numarası verilen kaydı sil.", {"session_index": integer}, ["session_index"]), self._function("plan_day", "Açık görevleri önceliğe göre günlük rutin haline getir.", {"available_minutes": integer, "start_time": {"type": "string"}}, ["available_minutes", "start_time"]), self._function("add_note", "Kullanıcının fikrini veya notunu kaydet.", {"content": {"type": "string"}, "category": {"type": "string"}}, ["content", "category"]), self._function("list_notes", "Kayıtlı notları ve fikirleri listele.", {"category": {"type": "string"}}, ["category"]), self._function("add_reminder", "Belirli süre sonrasına hatırlatıcı ekle.", {"title": {"type": "string"}, "minutes_from_now": integer}, ["title", "minutes_from_now"]), self._function("list_reminders", "Bekleyen hatırlatıcıları listele.", {"include_completed": {"type": "boolean"}}, ["include_completed"]), self._function("add_list_item", "Alışveriş veya özel listeye madde ekle.", {"list_name": {"type": "string"}, "item": {"type": "string"}}, ["list_name", "item"]), self._function("list_items", "Alışveriş ve diğer listeleri göster.", {"list_name": {"type": "string"}}, ["list_name"]), self._function("daily_summary", "Bugünkü görev, odak seansı, not ve hatırlatıcı özetini getir.", {}, [])]

    @staticmethod
    def _function(name: str, description: str, properties: dict, required: list[str]) -> dict:
        return {"type": "function", "name": name, "description": description, "parameters": {"type": "object", "properties": properties, "required": required, "additionalProperties": False}, "strict": True}

    def call(self, name: str, arguments: dict) -> dict:
        method = getattr(self, name, None)
        if not method or name.startswith("_") or name == "call":
            return {"error": f"Bilinmeyen tool: {name}"}
        return method(**arguments)
