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

async function state() {
  try {
    const response = await fetch(`/api/state?ts=${Date.now()}`);
    render(await response.json());
  } catch (error) {
    addBubble('Sunucuya bağlanamadım. PowerShell penceresinde web sunucusunun açık olduğundan emin ol.', 'bot');
  }
}

async function command(message) {
  addBubble(message, 'user');
  addBubble('İşliyorum…', 'bot');
  const pending = $('chat').lastElementChild;
  try {
    const response = await fetch('/api/command', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ message }) });
    const data = await response.json();
    pending.remove();
    addBubble(data.answer || data.error, 'bot');
    if (data.state) render(data.state);
  } catch (error) {
    pending.textContent = 'Bir bağlantı sorunu oldu. Sunucuyu kontrol edelim.';
  }
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
window.deleteSession = async index => {
  if (!window.confirm('Bu seans kaydı silinsin mi?')) return;
  const response = await fetch(`/api/sessions/${index}`, { method: 'DELETE' });
  const data = await response.json();
  if (response.ok) render(data.state);
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

async function saveTaskForm(formId, titleId, minutesId, priorityId) {
  const title = $(titleId).value.trim();
  if (!title) { $(titleId).focus(); return; }
  const button = $(`${formId.replace('form', 'save')}`);
  if (button) { button.disabled = true; button.textContent = 'Kaydediliyor…'; }
  try {
    const response = await fetch('/api/tasks', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ title, minutes: Number($(minutesId).value), priority: $(priorityId).value }) });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Görev kaydedilemedi.');
    $(formId).hidden = true;
    $(titleId).value = '';
    render(data.state);
  } catch (error) {
    window.alert(error.message);
  } finally {
    if (button) { button.disabled = false; button.textContent = 'Görevi kaydet'; }
  }
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
