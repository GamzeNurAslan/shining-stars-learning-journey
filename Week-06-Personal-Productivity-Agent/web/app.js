const $ = id => document.getElementById(id);
let timerSeconds = 0;
let timerTotal = 1500;
let timerStatus = 'idle';

const esc = value => String(value ?? '').replace(/[&<>\'\"]/g, ch => ({
  '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;'
}[ch]));

function setText(ids, value) {
  ids.forEach(id => { if ($(id)) $(id).textContent = value; });
}

function setDisabled(ids, value) {
  ids.forEach(id => { if ($(id)) $(id).disabled = value; });
}

function timerLabel(status) {
  return status === 'running' ? 'Çalışıyor' : (status === 'paused' ? 'Duraklatıldı' : (status === 'completed' ? 'Tamamlandı' : 'Başlamaya hazır'));
}

function renderTimer(data) {
  const t = data.timer || {};
  timerStatus = t.status || 'idle';
  timerTotal = (t.duration_minutes || 25) * 60;
  timerSeconds = ['running', 'paused'].includes(timerStatus) ? (t.remaining_seconds || 0) : timerTotal;
  const formatted = `${String(Math.floor(timerSeconds / 60)).padStart(2, '0')}:${String(timerSeconds % 60).padStart(2, '0')}`;
  const progress = Math.max(0, 360 - (timerSeconds / timerTotal * 360));
  const ringStyle = `conic-gradient(#6556e8 ${progress}deg, #ececf5 0deg)`;
  setText(['time', 'pom-time'], formatted);
  const visibleTask = ['running', 'paused'].includes(timerStatus) ? (t.task || 'Odaklanma') : 'Odaklanma seansı';
  setText(['timer-task', 'pom-task'], visibleTask);
  setText(['timer-state', 'pom-state'], timerLabel(timerStatus));
  ['ring', 'pom-ring'].forEach(id => {
    if (!$(id)) return;
    $(id).style.background = ringStyle;
    $(id).classList.toggle('is-running', timerStatus === 'running');
    $(id).classList.toggle('is-paused', timerStatus === 'paused');
  });
  ['timer-card', 'detail-timer'].forEach(id => { if ($(id)) $(id).classList.toggle('is-running', timerStatus === 'running'); });
  setText(['pause', 'pom-pause'], timerStatus === 'paused' ? 'Devam et' : 'Duraklat');
  setDisabled(['pause', 'pom-pause', 'stop', 'pom-stop'], !['running', 'paused'].includes(timerStatus));
  setText(['focus-count', 'pom-focus-count'], data.summary.focus_sessions || 0);
  setText(['focus-minutes', 'pom-focus-minutes'], data.summary.focus_minutes || 0);
  setText(['done-count', 'pom-done-count'], data.summary.completed_tasks || 0);
}

function taskRow(task) {
  const priority = task.priority === 'high' ? 'Yüksek' : (task.priority === 'low' ? 'Düşük' : 'Normal');
  return `<div class="task ${task.completed ? 'done' : ''}"><span class="check ${task.completed ? 'done' : ''}" ${task.completed ? '' : `onclick="completeTask(${task.id})"`}>${task.completed ? '✓' : ''}</span><span class="task-main">${esc(task.title)}<small class="task-meta">${task.minutes} dk · ${priority} öncelik</small></span><span class="priority ${task.priority === 'normal' ? 'normal' : ''}"></span><button class="task-delete" onclick="deleteTask(${task.id})" title="Görevi sil" aria-label="${esc(task.title)} görevini sil">×</button></div>`;
}

function taskCollection(tasks, emptyText) {
  const open = tasks.filter(task => !task.completed);
  const done = tasks.filter(task => task.completed);
  if (!tasks.length) return `<div class="empty">${emptyText}</div>`;
  const openMarkup = open.length ? `<div class="task-group"><div class="group-label">Açık görevler</div>${open.map(taskRow).join('')}</div>` : '<div class="empty">Açık görev kalmadı.</div>';
  const doneMarkup = done.length ? `<div class="task-group"><div class="group-label">Tamamlananlar</div>${done.map(taskRow).join('')}</div>` : '';
  return openMarkup + doneMarkup;
}

function routineMarkup(routine, emptyText) {
  return routine.length ? routine.map(item => `<div class="routine ${item.type === 'break' ? 'break' : ''}"><span class="time-label">${esc(item.time)}</span><span class="routine-title">${esc(item.title)}</span><span class="task-meta">${item.minutes} dk</span></div>`).join('') : `<div class="empty">${emptyText}</div>`;
}

function renderHistory(sessions) {
  const history = $('session-history');
  if (!history) return;
  if (!sessions.length) {
    history.innerHTML = '<div class="empty">Henüz tamamlanan bir seans yok.</div>';
    return;
  }
  history.innerHTML = sessions.slice().reverse().map(session => {
    const taskName = typeof session.task === 'string' && session.task.trim().length > 2 ? session.task.trim() : 'Odaklanma seansı';
    return `<div class="history-item"><span class="history-icon">✓</span><div class="history-copy"><strong>${esc(taskName)}</strong><small>${session.duration_minutes || 25} dakikalık seans · ${session.status === 'completed' ? 'Tamamlandı' : 'Durduruldu'}</small></div><button class="history-delete" onclick="deleteSession(${session.index})" title="Seansı sil" aria-label="${esc(taskName)} seansını sil">×</button></div>`;
  }).join('');
}

function render(data) {
  renderTimer(data);
  const tasks = data.tasks || [];
  const open = tasks.filter(task => !task.completed);
  const done = tasks.filter(task => task.completed);
  setText(['task-count'], `${open.length} açık · ${done.length} tamamlandı`);
  setText(['open-metric'], open.length);
  setText(['done-metric'], done.length);
  setText(['minutes-metric'], `${open.reduce((total, task) => total + Number(task.minutes || 0), 0)} dk`);
  if ($('tasks')) $('tasks').innerHTML = taskCollection(tasks, 'Henüz görev yok. “+ Görev ekle”ye bas veya yardımcıya yaz.');
  if ($('tasks-detail')) $('tasks-detail').innerHTML = taskCollection(tasks, 'Henüz görev yok. Yeni bir görev ekleyerek başlayalım.');
  const routine = data.routine || [];
  if ($('routine')) $('routine').innerHTML = routineMarkup(routine, open.length ? 'Rutin henüz oluşturulmadı.<br><small>Görevlerini saatli odak bloklarına çevirmek için “Rutin oluştur”a bas.</small>' : 'Planlanacak açık görev yok.<br><small>Önce bir görev ekleyelim.</small>');
  if ($('routine-detail')) $('routine-detail').innerHTML = routineMarkup(routine, 'Planlanacak açık görev yok.<br><small>Önce görev ekleyip “Rutin oluştur”a bas.</small>');
  renderHistory(data.sessions || []);
}

const STORAGE_KEY = 'odak-kocu-public-v1';
const EMPTY_STATE = { timer: null, tasks: [], routine: [], sessions: [], notes: [], reminders: [], lists: {} };
let memoryState = null;

function cloneEmptyState() {
  return JSON.parse(JSON.stringify(EMPTY_STATE));
}

function loadState() {
  if (memoryState) return memoryState;
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || 'null');
    memoryState = { ...cloneEmptyState(), ...(saved || {}) };
  } catch (error) {
    memoryState = cloneEmptyState();
  }
  return memoryState;
}

function saveState(data) {
  memoryState = data;
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(data)); } catch (error) { /* memory fallback */ }
}

function minutesFrom(message, fallback = 25) {
  const minuteMatch = message.match(/(\d+)\s*(?:dakika|dk)/i);
  if (minuteMatch) return Math.max(1, Math.min(180, Number(minuteMatch[1])));
  const hourMatch = message.match(/(\d+)\s*saat/i);
  return hourMatch ? Math.max(1, Math.min(180, Number(hourMatch[1]) * 60)) : fallback;
}

function syncTimer(data) {
  const timer = data.timer;
  if (!timer) return;
  if (timer.status === 'running') {
    timer.remaining_seconds = Math.max(0, Math.ceil((timer.ends_at_ms - Date.now()) / 1000));
    if (timer.remaining_seconds === 0) {
      timer.status = 'completed';
      if (!timer.session_recorded) {
        data.sessions.push({ ...timer, completed_at: new Date().toISOString(), session_recorded: true });
        timer.session_recorded = true;
      }
      saveState(data);
    }
  }
}

function snapshot() {
  const data = loadState();
  syncTimer(data);
  const tasks = data.tasks || [];
  const sessions = data.sessions || [];
  return {
    ...data,
    sessions: sessions.map((session, index) => ({ index, ...session })),
    summary: {
      open_tasks: tasks.filter(task => !task.completed).length,
      completed_tasks: tasks.filter(task => task.completed).length,
      focus_sessions: sessions.length,
      focus_minutes: sessions.reduce((total, session) => total + Number(session.duration_minutes || 0), 0),
      notes: (data.notes || []).length,
      reminders: (data.reminders || []).filter(reminder => !reminder.completed).length,
      routine: data.routine || []
    }
  };
}

function nextTaskId(data) {
  return Math.max(0, ...(data.tasks || []).map(task => Number(task.id) || 0)) + 1;
}

function addTask(title, minutes = 25, priority = 'normal') {
  const data = loadState();
  data.tasks.push({ id: nextTaskId(data), title: title.trim(), minutes: Math.max(5, Math.min(480, Number(minutes) || 25)), priority: ['low', 'normal', 'high'].includes(priority) ? priority : 'normal', completed: false, created_at: new Date().toISOString() });
  saveState(data);
  return data.tasks[data.tasks.length - 1];
}

function planRoutine() {
  const data = loadState();
  const openTasks = data.tasks.filter(task => !task.completed).sort((a, b) => ({ high: 0, normal: 1, low: 2 }[a.priority] - ({ high: 0, normal: 1, low: 2 }[b.priority])));
  let remaining = 240;
  let cursor = 9 * 60;
  const routine = [];
  for (const task of openTasks) {
    if (remaining < 25) break;
    const block = Math.min(Number(task.minutes) || 25, remaining, 50);
    routine.push({ time: `${String(Math.floor(cursor / 60)).padStart(2, '0')}:${String(cursor % 60).padStart(2, '0')}`, title: task.title, minutes: block, task_id: task.id });
    cursor += block;
    remaining -= block;
    if (remaining >= 5) {
      routine.push({ time: `${String(Math.floor(cursor / 60)).padStart(2, '0')}:${String(cursor % 60).padStart(2, '0')}`, title: 'Mola', minutes: 5, type: 'break' });
      cursor += 5;
      remaining -= 5;
    }
  }
  data.routine = routine;
  saveState(data);
  return routine;
}

function startTimer(minutes, task = 'Odaklanma') {
  const data = loadState();
  if (data.timer && ['running', 'paused'].includes(data.timer.status)) return 'Zaten devam eden bir odak seansı var.';
  const now = Date.now();
  data.timer = { status: 'running', task: task.trim() || 'Odaklanma', duration_minutes: minutes, started_at: new Date(now).toISOString(), ends_at_ms: now + minutes * 60000, remaining_seconds: minutes * 60 };
  saveState(data);
  return `${data.timer.task} için ${minutes} dakikalık odak seansı başladı.`;
}

function timerCommand(action) {
  const data = loadState();
  const timer = data.timer;
  if (action === 'status') {
    syncTimer(data);
    if (!timer) return 'Şu anda çalışan bir zamanlayıcı yok.';
    const minutes = Math.ceil((timer.remaining_seconds || 0) / 60);
    return timer.status === 'running' ? `${timer.task} devam ediyor. Yaklaşık ${minutes} dakika kaldı.` : `Zamanlayıcı durumu: ${timerLabel(timer.status)}.`;
  }
  if (!timer || !['running', 'paused'].includes(timer.status)) return 'Şu anda aktif bir odak seansı yok.';
  syncTimer(data);
  if (action === 'pause' && timer.status === 'running') {
    timer.status = 'paused';
    saveState(data);
    return `${timer.task} duraklatıldı.`;
  }
  if (action === 'resume' && timer.status === 'paused') {
    timer.status = 'running';
    timer.ends_at_ms = Date.now() + timer.remaining_seconds * 1000;
    saveState(data);
    return `${timer.task} devam ediyor.`;
  }
  if (action === 'stop') {
    timer.status = 'stopped';
    timer.stopped_at = new Date().toISOString();
    if (!timer.session_recorded) data.sessions.push({ ...timer, session_recorded: true });
    saveState(data);
    return `${timer.task} seansı kaydedildi.`;
  }
  return 'Zamanlayıcı hazır.';
}

function runCommand(message) {
  const lower = message.toLocaleLowerCase('tr-TR');
  if (/^(merhaba|selam|hey|günaydın)/.test(lower)) return 'Merhaba! Bugün birlikte küçük ve uygulanabilir bir adım seçebiliriz. 🌿';
  if (lower.includes('neler yapabilirsin') || lower.includes('ne yapabilirsin')) return 'Görevlerini, Pomodoro seanslarını, günlük rutinini, notlarını ve hatırlatıcılarını birlikte düzenleyebiliriz.';
  if (lower.includes('görev ekle') || lower.includes('yapılacak ekle')) {
    let title = message.replace(/.*?(görev ekle|yapılacak ekle)/i, '').replace(/\d+\s*(?:dakika|dk)/i, '').replace(/yüksek öncelik|düşük öncelik|öncelikli|acil/gi, '').trim().replace(/^[,.:;-]+|[,.:;-]+$/g, '');
    const priority = /yüksek|önemli|acil/i.test(message) ? 'high' : (/düşük/i.test(message) ? 'low' : 'normal');
    if (!title) return 'Görev adını da yazabilir misin?';
    const task = addTask(title, minutesFrom(message), priority);
    return `Görev eklendi: #${task.id} ${task.title}`;
  }
  if ((lower.includes('tamamlandı') || lower.includes('tamamla')) && /\d+/.test(lower)) {
    const id = Number(lower.match(/\d+/)[0]);
    const task = loadState().tasks.find(item => item.id === id);
    if (!task) return 'Bu numarada bir görev bulamadım.';
    task.completed = true;
    task.completed_at = new Date().toISOString();
    saveState(loadState());
    return `Tamamlandı: ${task.title}`;
  }
  if ((lower.includes('görev') || lower.includes('sil')) && lower.includes('sil') && /\d+/.test(lower)) {
    const id = Number(lower.match(/\d+/)[0]);
    const data = loadState();
    const index = data.tasks.findIndex(task => task.id === id);
    if (index < 0) return 'Bu numarada bir görev bulamadım.';
    const [deleted] = data.tasks.splice(index, 1);
    data.routine = data.routine.filter(item => item.task_id !== id);
    saveState(data);
    return `Görev silindi: ${deleted.title}`;
  }
  if (lower.includes('görevler') || lower.includes('yapılacaklar')) {
    const tasks = loadState().tasks.filter(task => !task.completed);
    return tasks.length ? `Açık görevler:\n${tasks.map(task => `#${task.id} ${task.title} · ${task.minutes} dk`).join('\n')}` : 'Henüz açık görev yok.';
  }
  if (lower.includes('duraklat') || lower.includes('beklet')) return timerCommand('pause');
  if (lower.includes('devam et') || lower.includes('sürdür')) return timerCommand('resume');
  if (lower.includes('durdur') || lower.includes('bitir')) return timerCommand('stop');
  if (lower.includes('durum') || lower.includes('kaç dakika') || lower.includes('zamanlayıcı')) return timerCommand('status');
  if (lower.includes('rutin') || lower.includes('planla') || lower.includes('günümü')) {
    const routine = planRoutine();
    return routine.length ? `Bugünkü rutin hazırlandı:\n${routine.map(item => `- ${item.time} · ${item.title} (${item.minutes} dk)`).join('\n')}` : 'Önce planlamak istediğin açık görevleri ekleyelim.';
  }
  if (lower.includes('özet') || lower.includes('bugünüm nasıl') || lower.includes('ne yapmalıyım')) {
    const summary = snapshot().summary;
    return `Bugünün özeti: ${summary.open_tasks} açık görev, ${summary.completed_tasks} tamamlanan görev ve ${summary.focus_sessions} odak seansı.`;
  }
  if (lower.includes('başlat') || lower.includes('pomodoro') || lower.includes('odaklan')) {
    const task = message.replace(/\d+\s*(?:dakika|dk)/i, '').replace(/pomodoro|başlat|odaklanma|odaklan|için|bir/gi, '').trim() || 'Odaklanma';
    return startTimer(minutesFrom(message), task);
  }
  return 'Seni dinliyorum. İstersen bir görev ekleyebilir, Pomodoro başlatabilir veya bugünkü rutinini planlayabiliriz.';
}

function state() {
  render(snapshot());
}

function command(message) {
  addBubble(message, 'user');
  const answer = runCommand(message);
  addBubble(answer, 'bot');
  state();
}

function addBubble(text, kind) {
  const bubble = document.createElement('div');
  bubble.className = `bubble ${kind}`;
  bubble.textContent = text;
  $('chat').appendChild(bubble);
  $('chat').scrollTop = $('chat').scrollHeight;
}

function showView(view, updateHash = true) {
  const link = document.querySelector(`nav a[data-view="${view}"]`) || document.querySelector('nav a[data-view="today"]');
  const selectedView = link.dataset.view;
  document.querySelectorAll('nav a').forEach(item => item.classList.toggle('active', item === link));
  document.querySelectorAll('.view').forEach(item => item.classList.toggle('active', item.id === `view-${selectedView}`));
  $('page-title').textContent = link.dataset.title;
  $('page-subtitle').textContent = link.dataset.subtitle;
  if (updateHash) history.replaceState(null, '', `#${selectedView}`);
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

window.addEventListener('hashchange', () => showView(window.location.hash.replace('#', '') || 'today', false));

window.completeTask = id => command(`görev ${id} tamamlandı`);
window.deleteTask = id => command(`görev ${id} sil`);
window.deleteSession = index => {
  if (!window.confirm('Bu seans kaydı silinsin mi?')) return;
  const data = loadState();
  data.sessions.splice(index, 1);
  saveState(data);
  state();
};
document.querySelectorAll('[data-view-target]').forEach(button => button.onclick = () => showView(button.dataset.viewTarget));
document.querySelectorAll('[data-prompt]').forEach(button => button.onclick = () => command(button.dataset.prompt));
$('chat-form').onsubmit = event => { event.preventDefault(); const value = $('message').value.trim(); if (value) { command(value); $('message').value = ''; } };

function bindCommand(ids, message) {
  ids.forEach(id => { if ($(id)) $(id).onclick = () => command(typeof message === 'function' ? message() : message); });
}

bindCommand(['start', 'pom-start'], '25 dakika odaklanma için Pomodoro başlat');
bindCommand(['pause', 'pom-pause'], () => timerStatus === 'paused' ? 'zamanlayıcıya devam et' : 'zamanlayıcıyı duraklat');
bindCommand(['stop', 'pom-stop'], 'zamanlayıcıyı bitir');
bindCommand(['plan', 'routine-plan-top'], 'bugünkü rutinimi planla');

function openTaskForm(formId, titleId) {
  const form = $(formId);
  if (!form) return;
  form.hidden = false;
  $(titleId).focus();
}

function closeTaskForm(formId) {
  const form = $(formId);
  if (form) form.hidden = true;
}

function saveTaskForm(formId, titleId, minutesId, priorityId) {
  const title = $(titleId).value.trim();
  if (!title) { $(titleId).focus(); return; }
  const button = $(`${formId.replace('form', 'save')}`);
  if (button) { button.disabled = true; button.textContent = 'Kaydediliyor…'; }
  addTask(title, Number($(minutesId).value), $(priorityId).value);
  $(formId).hidden = true;
  $(titleId).value = '';
  state();
  if (button) { button.disabled = false; button.textContent = 'Görevi kaydet'; }
}

if ($('add-task')) $('add-task').onclick = () => openTaskForm('quick-task-form', 'quick-task-title');
if ($('tasks-add-top')) $('tasks-add-top').onclick = () => { showView('tasks'); openTaskForm('task-page-form', 'task-page-title'); };
if ($('tasks-add-inline')) $('tasks-add-inline').onclick = () => openTaskForm('task-page-form', 'task-page-title');
if ($('quick-task-cancel')) $('quick-task-cancel').onclick = () => closeTaskForm('quick-task-form');
if ($('task-page-cancel')) $('task-page-cancel').onclick = () => closeTaskForm('task-page-form');
if ($('quick-task-save')) $('quick-task-save').onclick = () => saveTaskForm('quick-task-form', 'quick-task-title', 'quick-task-minutes', 'quick-task-priority');
if ($('task-page-save')) $('task-page-save').onclick = () => saveTaskForm('task-page-form', 'task-page-title', 'task-page-minutes', 'task-page-priority');

$('date').textContent = new Intl.DateTimeFormat('tr-TR', { day: 'numeric', month: 'long', year: 'numeric' }).format(new Date());
const initialView = window.location.hash.replace('#', '') || 'today';
showView(initialView, false);
const motivationQuotes = [
  'Başlamak, planın yarısıdır.',
  'Bugün mükemmel olmak değil, devam etmek yeterli.',
  'Küçük adımlar da ilerlemedir.',
  'Dikkatini verdiğin şey büyür.'
];
let motivationIndex = 0;
setInterval(() => {
  const quote = $('motivation-quote');
  if (!quote) return;
  motivationIndex = (motivationIndex + 1) % motivationQuotes.length;
  quote.style.opacity = '0';
  setTimeout(() => {
    quote.textContent = motivationQuotes[motivationIndex];
    quote.style.opacity = '1';
  }, 180);
}, 6500);
setInterval(state, 1000);
state();
