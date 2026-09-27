from odak_kocu.agent import FocusAgent
from odak_kocu.tools import FocusToolbox


def test_timer_starts_and_reports_status(tmp_path):
    toolbox = FocusToolbox(tmp_path / "state.json")
    started = toolbox.start_timer(25, "Ders çalışma")
    assert started["status"] == "running"
    status = toolbox.timer_status()
    assert status["task"] == "Ders çalışma"
    assert status["remaining_seconds"] > 0


def test_tasks_and_daily_plan(tmp_path):
    toolbox = FocusToolbox(tmp_path / "state.json")
    task = toolbox.add_task("Rapor yaz", 40, "high")
    toolbox.add_task("Kitap oku", 25, "normal")
    plan = toolbox.plan_day(120, "09:00")
    assert plan["routine"][0]["title"] == "Rapor yaz"
    assert toolbox.complete_task(task["id"])["completed"] is True


def test_timer_can_pause_and_resume(tmp_path):
    toolbox = FocusToolbox(tmp_path / "state.json")
    toolbox.start_timer(25, "Ders çalışma")
    paused = toolbox.pause_timer()
    assert paused["status"] == "paused"
    resumed = toolbox.resume_timer()
    assert resumed["status"] == "running"


def test_demo_agent_understands_task_listing(tmp_path):
    agent = FocusAgent(tmp_path / "state.json")
    agent.toolbox.add_task("Sunum hazırla", 45, "high")
    result = agent.run("Görevlerimi göster")
    assert "Sunum hazırla" in result.answer
    assert result.tool_calls == ["list_tasks"]


def test_notes_reminders_and_lists(tmp_path):
    toolbox = FocusToolbox(tmp_path / "state.json")
    note = toolbox.add_note("Toplantıda yeni fikir çıktı", "toplantı")
    reminder = toolbox.add_reminder("Mola ver", 30)
    item = toolbox.add_list_item("alışveriş", "Süt")
    assert toolbox.list_notes("toplantı")["notes"][0]["id"] == note["id"]
    assert toolbox.list_reminders()["reminders"][0]["id"] == reminder["id"]
    assert toolbox.list_items("alışveriş")["items"][0]["id"] == item["item"]["id"]


def test_demo_agent_can_capture_a_reminder(tmp_path):
    agent = FocusAgent(tmp_path / "state.json")
    result = agent.run("30 dakika sonra mola vermeyi hatırlat")
    assert "hatırlatıcı" in result.answer
    assert result.tool_calls == ["add_reminder"]


def test_demo_agent_keeps_casual_conversation_flow(tmp_path):
    agent = FocusAgent(tmp_path / "state.json")
    positive = agent.run("ben de iyiyim")
    tired = agent.run("yani biraz yorgunum aslında")
    assert "Buna sevindim" in positive.answer
    assert "Bayağı yorulmuşsun" in tired.answer
    assert "Devam et, seni bölmeden dinliyorum" not in tired.answer


def test_completed_task_can_be_deleted(tmp_path):
    toolbox = FocusToolbox(tmp_path / "state.json")
    task = toolbox.add_task("Eski işi temizle", 25)
    toolbox.complete_task(task["id"])
    deleted = toolbox.delete_task(task["id"])
    assert deleted["deleted"]["title"] == "Eski işi temizle"
    assert toolbox.list_tasks(True)["tasks"] == []


def test_focus_session_can_be_deleted(tmp_path):
    toolbox = FocusToolbox(tmp_path / "state.json")
    toolbox.start_timer(25, "Eski seans")
    toolbox.stop_timer()
    deleted = toolbox.delete_session(0)
    assert deleted["deleted"]["task"] == "Eski seans"
    assert toolbox.daily_summary()["focus_sessions"] == 0
