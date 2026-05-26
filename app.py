<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>العبقري 2 - لوحة الكرات</title>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
:root {
  --bg: #f5f5f0;
  --surface: #ffffff;
  --surface2: #f0eeea;
  --border: rgba(0,0,0,0.12);
  --border2: rgba(0,0,0,0.22);
  --text: #1a1a1a;
  --text2: #666;
  --blue: #185FA5;
  --blue-dark: #0C447C;
  --green: #1D9E75;
  --green-dark: #0F6E56;
  --red: #E24B4A;
  --gold: #d4af37;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #1a1a1a;
    --surface: #252525;
    --surface2: #2e2e2e;
    --border: rgba(255,255,255,0.12);
    --border2: rgba(255,255,255,0.22);
    --text: #f0f0f0;
    --text2: #999;
  }
}
body {
  background: var(--bg);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  color: var(--text);
  min-height: 100vh;
}
#app { padding: 14px; max-width: 440px; margin: 0 auto; }
.title {
  font-size: 16px; font-weight: 600;
  text-align: center;
  margin-bottom: 12px;
  letter-spacing: 0.3px;
}
.counter-bar { display: flex; gap: 8px; justify-content: center; margin-bottom: 10px; }
.counter-box {
  flex: 1;
  background: var(--surface);
  border: 0.5px solid var(--border);
  border-radius: 10px;
  padding: 8px 12px;
  text-align: center;
}
.counter-box .lbl { font-size: 11px; color: var(--text2); margin-bottom: 2px; }
.counter-box .val { font-size: 20px; font-weight: 600; color: var(--text); }
.counter-box.warn .val { color: var(--red); }
.counter-box.ok .val { color: var(--green); }
.phase-label {
  font-size: 12px; color: var(--text2);
  text-align: center; margin-bottom: 6px;
}
.msg {
  font-size: 12px; text-align: center;
  min-height: 18px; margin-bottom: 6px;
  color: var(--red);
}
.msg.green { color: var(--green); }
.grid {
  display: grid;
  grid-template-columns: repeat(10, 1fr);
  gap: 4px;
  margin-bottom: 12px;
}
.ball {
  aspect-ratio: 1;
  border-radius: 50%;
  border: 1.5px solid var(--border2);
  background: var(--surface);
  display: flex; align-items: center; justify-content: center;
  font-size: 11px; font-weight: 500;
  color: var(--text);
  cursor: pointer;
  transition: background 0.1s, color 0.1s, border-color 0.1s, transform 0.08s;
  -webkit-tap-highlight-color: transparent;
  user-select: none;
}
.ball:active:not(.locked) { transform: scale(0.9); }
.ball.sel1 { background: var(--blue); color: #fff; border-color: var(--blue); }
.ball.sel2 { background: var(--green); color: #fff; border-color: var(--green); }
.ball.locked { opacity: 0.3; cursor: default; }
.ball.sel1.locked { opacity: 0.55; }
.sel-row { display: flex; gap: 8px; margin-bottom: 10px; }
.sel-box {
  flex: 1;
  background: var(--surface);
  border: 0.5px solid var(--border);
  border-radius: 10px;
  padding: 8px;
  min-height: 56px;
}
.sel-box .sel-title {
  font-size: 11px; color: var(--text2);
  margin-bottom: 5px;
}
.sel-nums { display: flex; flex-wrap: wrap; gap: 3px; }
.num-chip {
  font-size: 10px; font-weight: 600;
  padding: 2px 5px;
  border-radius: 4px;
  color: #fff;
}
.chip1 { background: var(--blue); }
.chip2 { background: var(--green); }
.action-btn {
  width: 100%;
  padding: 13px;
  border-radius: 10px;
  border: 0.5px solid var(--border2);
  background: var(--surface);
  font-size: 14px; font-weight: 600;
  color: var(--text);
  cursor: pointer;
  margin-bottom: 8px;
  -webkit-tap-highlight-color: transparent;
  transition: background 0.1s, transform 0.08s;
  font-family: inherit;
}
.action-btn:active:not(:disabled) { transform: scale(0.98); }
.action-btn.primary { background: var(--blue); color: #fff; border-color: var(--blue); }
.action-btn.primary:active { background: var(--blue-dark); }
.action-btn.success { background: var(--green); color: #fff; border-color: var(--green); }
.action-btn.success:active { background: var(--green-dark); }
.action-btn:disabled { opacity: 0.38; cursor: default; }
.divider { height: 0.5px; background: var(--border); margin: 4px 0 12px; }

/* تصميم البطاقات الذكية */
#cards-area { display: none; margin-top: 15px; }
.cards-title { text-align: center; font-size: 16px; font-weight: bold; color: var(--text); margin-bottom: 12px; }
.cards-grid { display: grid; grid-template-columns: 1fr; gap: 10px; }
.card-box {
  background: var(--surface);
  border: 1.5px solid var(--gold);
  border-radius: 10px;
  padding: 15px;
  text-align: center;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}
.card-name { font-size: 13px; color: var(--text2); margin-bottom: 8px; font-weight: bold; }
.card-nums { font-size: 24px; font-weight: bold; color: var(--blue); letter-spacing: 5px; direction: ltr; }
</style>
</head>
<body>
<div id="app">
  <div class="title">🎱 العبقري 2 — لوحة الكرات</div>

  <div class="counter-bar">
    <div class="counter-box" id="cnt-box">
      <div class="lbl">تم اختيار</div>
      <div class="val" id="cnt-val">0 / 50</div>
    </div>
    <div class="counter-box" id="phase-box">
      <div class="lbl">المرحلة</div>
      <div class="val" id="phase-val">الأولى</div>
    </div>
  </div>

  <div class="phase-label" id="phase-hint">اختر 50 كرة للسحب الأول</div>
  <div class="msg" id="msg-area"></div>

  <div class="grid" id="ball-grid"></div>

  <div class="sel-row">
    <div class="sel-box">
      <div class="sel-title">🔵 السحب الأول</div>
      <div class="sel-nums" id="sel1-nums"></div>
    </div>
    <div class="sel-box">
      <div class="sel-title">🟢 السحب الثاني</div>
      <div class="sel-nums" id="sel2-nums"></div>
    </div>
  </div>

  <button class="action-btn primary" id="confirm-btn" disabled>تأكيد السحب الأول (0/50)</button>
  <button class="action-btn success" id="filter-btn" style="display:none">🚀 تشغيل خوارزمية الفلترة والتوليد</button>
  
  <div id="cards-area">
    <div class="cards-title">🎯 البطاقات الست الذكية</div>
    <div class="cards-grid" id="cards-container"></div>
  </div>

  <div class="divider"></div>
  <button class="action-btn" id="reset-btn">↺ إعادة تعيين الكل</button>
</div>

<script>
const MAX = 50;
let phase = 1, sel1 = [], sel2 = [], current = [];

const grid = document.getElementById('ball-grid');
const cntVal = document.getElementById('cnt-val');
const cntBox = document.getElementById('cnt-box');
const phaseVal = document.getElementById('phase-val');
const phaseHint = document.getElementById('phase-hint');
const msgArea = document.getElementById('msg-area');
const confirmBtn = document.getElementById('confirm-btn');
const filterBtn = document.getElementById('filter-btn');
const sel1Nums = document.getElementById('sel1-nums');
const sel2Nums = document.getElementById('sel2-nums');
const cardsArea = document.getElementById('cards-area');
const cardsContainer = document.getElementById('cards-container');

function buildGrid() {
  grid.innerHTML = '';
  for (let i = 1; i <= 90; i++) {
    const b = document.createElement('div');
    b.className = 'ball';
    b.textContent = i;
    b.dataset.n = i;
    b.addEventListener('click', () => toggleBall(i, b));
    grid.appendChild(b);
  }
}

function getBallEl(n) { return grid.querySelector('[data-n="' + n + '"]'); }

function toggleBall(n, el) {
  if (el.classList.contains('locked')) return;
  const idx = current.indexOf(n);
  if (idx === -1) {
    if (current.length >= MAX) {
      showMsg('وصلت للحد الأقصى 50 كرة!', true);
      return;
    }
    current.push(n);
    el.classList.add(phase === 1 ? 'sel1' : 'sel2');
  } else {
    current.splice(idx, 1);
    el.classList.remove('sel1', 'sel2');
  }
  updateUI();
}

function updateUI() {
  const cnt = current.length;
  cntVal.textContent = cnt + ' / ' + MAX;
  cntBox.className = 'counter-box' + (cnt === MAX ? ' ok' : cnt > MAX ? ' warn' : '');
  confirmBtn.textContent = (phase === 1 ? 'تأكيد السحب الأول' : 'تأكيد السحب الثاني') + ' (' + cnt + '/50)';
  confirmBtn.disabled = cnt !== MAX;
  if (cnt < MAX) {
    showMsg(cnt > 0 ? 'تبقى ' + (MAX - cnt) + ' كرة' : '', false);
  } else {
    showMsg('ممتاز! اضغط التأكيد ✓', false);
  }
  renderChips(sel1Nums, sel1, 'chip1');
  renderChips(sel2Nums, sel2, 'chip2');
}

function renderChips(container, arr, cls) {
  container.innerHTML = '';
  arr.slice().sort((a, b) => a - b).forEach(n => {
    const c = document.createElement('span');
    c.className = 'num-chip ' + cls;
    c.textContent = n;
    container.appendChild(c);
  });
}

function showMsg(txt, isError) {
  msgArea.textContent = txt;
  msgArea.className = 'msg' + (isError ? '' : ' green');
}

confirmBtn.addEventListener('click', () => {
  if (current.length !== MAX) return;
  if (phase === 1) {
    sel1 = [...current];
    current = [];
    phase = 2;
    phaseVal.textContent = 'الثانية';
    phaseHint.textContent = 'الآن اختر 50 كرة للسحب الثاني';
    confirmBtn.disabled = true;
    renderChips(sel1Nums, sel1, 'chip1');
    resetGrid(false);
    showMsg('تم حفظ السحب الأول، اختر 50 كرة جديدة', false);
  } else {
    sel2 = [...current];
    phase = 3;
    phaseHint.textContent = 'اكتمل السحبان — جاهز للفلترة والتوليد';
    confirmBtn.style.display = 'none';
    filterBtn.style.display = 'block';
    renderChips(sel2Nums, sel2, 'chip2');
    lockAll();
    showMsg('تم السحب الثاني بنجاح ✓', false);
  }
});

// =======================================
// محرك العبقري 2 - خوارزميات التوليد
// =======================================
filterBtn.addEventListener('click', () => {
  filterBtn.disabled = true;
  showMsg('جاري حساب الاحتمالات وتوليد البطاقات...', false);
  
  // بناء الوعاء النشط (الفلترة المتقدمة)
  let pool = [];
  for(let i=1; i<=90; i++) {
    let inD1 = sel1.includes(i);
    let inD2 = sel2.includes(i);
    // القاعدة: المشترك + اللي في الثاني مو بالأول + اللي ما طلع بالثنين
    if (!inD1 || inD2) pool.push(i); 
  }
  pool.sort((a,b) => a-b);

  // دالة الحماية لملء البطاقة بـ 5 أرقام فريدة
  function finalize(c, p) {
    let cSet = new Set(c);
    let attempts = 0;
    while (cSet.size < 5 && attempts < 200) {
      let rnd = p[Math.floor(Math.random() * p.length)];
      cSet.add(rnd);
      attempts++;
    }
    return Array.from(cSet).slice(0,5).sort((a,b)=>a-b);
  }

  let low = pool.filter(n => n <= 45);
  let high = pool.filter(n => n > 45);
  
  // دالة مساعدة للسحب العشوائي
  let getRnd = (arr, n) => {
    let shuffled = [...arr].sort(() => 0.5 - Math.random());
    return shuffled.slice(0, n);
  };

  let cards = {};

  // 1. نظرية التطرف (تيبيت)
  let t_pool = [...pool];
  cards['تيبيت (الأطراف)'] = finalize([...t_pool.slice(0,3), ...t_pool.slice(-2)], pool);

  // 2. نظرية التوازن (جرانفيل)
  cards['جرانفيل (توازن)'] = finalize([...getRnd(low, Math.min(low.length, 3)), ...getRnd(high, Math.min(high.length, 2))], pool);

  // 3. نظرية التكتل المتجاور (ضمان الأزواج)
  let pairs = [];
  for(let n of pool) { if(pool.includes(n+1)) pairs.push([n, n+1]); }
  let c3 = [];
  if(pairs.length > 0) {
    let p1 = pairs[Math.floor(Math.random() * pairs.length)];
    c3.push(p1[0], p1[1]);
    let p2 = pairs[Math