import streamlit as st
import streamlit.components.v1 as components

# إعداد الصفحة
st.set_page_config(page_title="العبقري 2", layout="centered", initial_sidebar_state="collapsed")

# إخفاء قوائم ستريملت
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# كود الواجهة والذكاء الاصطناعي مدمج بالكامل هنا
html_code = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>لوحة الكرات — العبقري 2</title>
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap" rel="stylesheet">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
:root {
  --bg: #0d0d0f;
  --surface: #16161a;
  --surface2: #1e1e24;
  --surface3: #26262e;
  --border: rgba(255,255,255,0.08);
  --border2: rgba(255,255,255,0.15);
  --text: #f0f0f0;
  --text2: #888;
  --text3: #555;
  --blue: #3b82f6;
  --blue-dark: #1d4ed8;
  --blue-glow: rgba(59,130,246,0.2);
  --green: #10b981;
  --green-dark: #047857;
  --green-glow: rgba(16,185,129,0.2);
  --gold: #f59e0b;
  --gold-glow: rgba(245,158,11,0.15);
  --red: #ef4444;
  --radius: 12px;
  --radius-sm: 8px;
}
body {
  background: var(--bg);
  font-family: 'Tajawal', sans-serif;
  color: var(--text);
  min-height: 100vh;
  padding-bottom: 40px;
}

.header {
  text-align: center;
  padding: 20px 16px 14px;
  border-bottom: 0.5px solid var(--border);
  background: var(--surface);
  margin-bottom: 14px;
  position: sticky;
  top: 0;
  z-index: 10;
}
.header h1 {
  font-size: 17px;
  font-weight: 700;
  letter-spacing: 0.5px;
  color: var(--text);
}
.header .sub {
  font-size: 11px;
  color: var(--text2);
  margin-top: 3px;
}

#app { padding: 0 12px; max-width: 440px; margin: 0 auto; }

.counter-bar { display: flex; gap: 8px; margin-bottom: 10px; }
.counter-box {
  flex: 1;
  background: var(--surface);
  border: 0.5px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 8px 10px;
  text-align: center;
}
.counter-box .lbl { font-size: 10px; color: var(--text2); margin-bottom: 2px; }
.counter-box .val { font-size: 20px; font-weight: 700; color: var(--text); }
.counter-box.ok .val { color: var(--green); }
.counter-box.warn .val { color: var(--red); }
.counter-box.phase-active { border-color: var(--blue); background: rgba(59,130,246,0.07); }

.phase-label { font-size: 12px; color: var(--text2); text-align: center; margin-bottom: 5px; }
.msg { font-size: 12px; text-align: center; min-height: 18px; margin-bottom: 6px; color: var(--red); }
.msg.green { color: var(--green); }
.msg.gold { color: var(--gold); }

.grid {
  display: grid;
  grid-template-columns: repeat(10, 1fr);
  gap: 3px;
  margin-bottom: 12px;
}
.ball {
  aspect-ratio: 1;
  border-radius: 50%;
  border: 1px solid var(--border2);
  background: var(--surface2);
  display: flex; align-items: center; justify-content: center;
  font-size: 10px; font-weight: 500;
  color: var(--text2);
  cursor: pointer;
  transition: all 0.1s;
  -webkit-tap-highlight-color: transparent;
  user-select: none;
}
.ball:active:not(.locked) { transform: scale(0.85); }
.ball.sel1 { background: var(--blue); color: #fff; border-color: var(--blue); box-shadow: 0 0 8px var(--blue-glow); font-weight: 700; }
.ball.sel2 { background: var(--green); color: #fff; border-color: var(--green); box-shadow: 0 0 8px var(--green-glow); font-weight: 700; }
.ball.locked { opacity: 0.28; cursor: default; }
.ball.sel1.locked { opacity: 0.5; }

.sel-row { display: flex; gap: 8px; margin-bottom: 10px; }
.sel-box {
  flex: 1;
  background: var(--surface);
  border: 0.5px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 8px;
  min-height: 54px;
}
.sel-box.active1 { border-color: rgba(59,130,246,0.4); }
.sel-box.active2 { border-color: rgba(16,185,129,0.4); }
.sel-box .sel-title { font-size: 11px; color: var(--text2); margin-bottom: 5px; }
.sel-nums { display: flex; flex-wrap: wrap; gap: 3px; }
.num-chip { font-size: 10px; font-weight: 700; padding: 2px 5px; border-radius: 4px; color: #fff; }
.chip1 { background: var(--blue); }
.chip2 { background: var(--green); }

.action-btn {
  width: 100%; padding: 13px; border-radius: var(--radius-sm); border: 0.5px solid var(--border2);
  background: var(--surface2); font-size: 14px; font-weight: 500; color: var(--text);
  cursor: pointer; margin-bottom: 8px; -webkit-tap-highlight-color: transparent; transition: all 0.1s;
  font-family: 'Tajawal', sans-serif;
}
.action-btn:active:not(:disabled) { transform: scale(0.98); opacity: 0.85; }
.action-btn.primary { background: var(--blue); color: #fff; border-color: var(--blue); box-shadow: 0 4px 16px var(--blue-glow); }
.action-btn.success { background: var(--green); color: #fff; border-color: var(--green); box-shadow: 0 4px 16px var(--green-glow); }
.action-btn.gold { background: var(--gold); color: #1a1a1a; border-color: var(--gold); box-shadow: 0 4px 16px var(--gold-glow); font-weight: 700; }
.action-btn:disabled { opacity: 0.3; cursor: default; box-shadow: none; }
.divider { height: 0.5px; background: var(--border); margin: 4px 0 12px; }

#filter-section { display: none; margin-top: 8px; }
.section-title { font-size: 13px; font-weight: 700; color: var(--text2); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px; text-align: center; }

.pool-info { background: var(--surface); border: 0.5px solid var(--border); border-radius: var(--radius-sm); padding: 10px 12px; margin-bottom: 12px; display: flex; gap: 8px; justify-content: space-around; }
.pool-stat { text-align: center; }
.pool-stat .ps-val { font-size: 18px; font-weight: 700; color: var(--gold); }
.pool-stat .ps-lbl { font-size: 10px; color: var(--text2); margin-top: 2px; }

#cards-area { display: none; margin-top: 4px; }
.cards-grid { display: flex; flex-direction: column; gap: 10px; }
.card-box { background: var(--surface); border: 0.5px solid var(--border); border-radius: var(--radius); padding: 12px 14px; animation: fadeUp 0.3s ease both; }
.card-box:nth-child(1) { animation-delay: 0.05s; border-right: 3px solid #3b82f6; }
.card-box:nth-child(2) { animation-delay: 0.10s; border-right: 3px solid #10b981; }
.card-box:nth-child(3) { animation-delay: 0.15s; border-right: 3px solid #f59e0b; }
.card-box:nth-child(4) { animation-delay: 0.20s; border-right: 3px solid #8b5cf6; }
.card-box:nth-child(5) { animation-delay: 0.25s; border-right: 3px solid #ef4444; }
.card-box:nth-child(6) { animation-delay: 0.30s; border-right: 3px solid #06b6d4; }
@keyframes fadeUp { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
.card-name { font-size: 11px; color: var(--text2); margin-bottom: 8px; font-weight: 500; }
.card-numbers { display: flex; gap: 6px; flex-wrap: wrap; }
.num-ball { width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: 700; color: #fff; }
.card-box:nth-child(1) .num-ball { background: #1d4ed8; }
.card-box:nth-child(2) .num-ball { background: #047857; }
.card-box:nth-child(3) .num-ball { background: #b45309; }
.card-box:nth-child(4) .num-ball { background: #6d28d9; }
.card-box:nth-child(5) .num-ball { background: #b91c1c; }
.card-box:nth-child(6) .num-ball { background: #0e7490; }

.pool-nums { display: flex; flex-wrap: wrap; gap: 3px; margin-bottom: 12px; }
.pool-chip { font-size: 10px; font-weight: 600; padding: 2px 6px; border-radius: 4px; background: var(--surface3); color: var(--text2); border: 0.5px solid var(--border); }
.pool-chip.common { background: rgba(245,158,11,0.15); color: var(--gold); border-color: rgba(245,158,11,0.3); }
</style>
</head>
<body>

<div class="header">
  <h1>🎱 لوحة الكرات — العبقري ٢</h1>
  <div class="sub">٩٠ كرة — اختيارين — فلترة ذكية</div>
</div>

<div id="app">
  <div class="counter-bar">
    <div class="counter-box" id="cnt-box"><div class="lbl">تم اختيار</div><div class="val" id="cnt-val">0 / 50</div></div>
    <div class="counter-box phase-active" id="phase-box"><div class="lbl">المرحلة</div><div class="val" id="phase-val">الأولى</div></div>
  </div>

  <div class="phase-label" id="phase-hint">اختر 50 كرة للاختيار الأول</div>
  <div class="msg" id="msg-area"></div>

  <div class="grid" id="ball-grid"></div>

  <div class="sel-row">
    <div class="sel-box" id="sel1-box"><div class="sel-title">🔵 الاختيار الأول</div><div class="sel-nums" id="sel1-nums"></div></div>
    <div class="sel-box" id="sel2-box"><div class="sel-title">🟢 الاختيار الثاني</div><div class="sel-nums" id="sel2-nums"></div></div>
  </div>

  <button class="action-btn primary" id="confirm-btn" disabled>تأكيد الاختيار الأول (0/50)</button>
  <button class="action-btn gold" id="filter-btn" style="display:none">⚡ دخول مرحلة الفلترة</button>
  <div class="divider"></div>
  <button class="action-btn" id="reset-btn">↺ إعادة تعيين الكل</button>

  <div id="filter-section">
    <div class="section-title">نتائج الفلترة</div>
    <div class="pool-info">
      <div class="pool-stat"><div class="ps-val" id="stat-pool">—</div><div class="ps-lbl">حجم الوعاء</div></div>
      <div class="pool-stat"><div class="ps-val" id="stat-common">—</div><div class="ps-lbl">مشتركة</div></div>
      <div class="pool-stat"><div class="ps-val" id="stat-net2">—</div><div class="ps-lbl">صافي الثاني</div></div>
      <div class="pool-stat"><div class="ps-val" id="stat-absent">—</div><div class="ps-lbl">غائبة</div></div>
    </div>
    <div class="section-title" style="margin-bottom:8px; font-size:11px;">أرقام الوعاء النشط</div>
    <div class="pool-nums" id="pool-display"></div>
    <div class="section-title" style="margin-top:4px;">البطاقات الست</div>
    <div id="cards-area"><div class="cards-grid" id="cards-container"></div></div>
  </div>
</div>

<script>
const MAX = 50;
let phase = 1, sel1 = [], sel2 = [], current = [];

const grid = document.getElementById('ball-grid');
const cntVal = document.getElementById('cnt-val');
const cntBox = document.getElementById('cnt-box');
const phaseVal = document.getElementById('phase-val');
const phaseBox = document.getElementById('phase-box');
const phaseHint = document.getElementById('phase-hint');
const msgArea = document.getElementById('msg-area');
const confirmBtn = document.getElementById('confirm-btn');
const filterBtn = document.getElementById('filter-btn');
const sel1Nums = document.getElementById('sel1-nums');
const sel2Nums = document.getElementById('sel2-nums');
const sel1Box = document.getElementById('sel1-box');
const sel2Box = document.getElementById('sel2-box');
const filterSection = document.getElementById('filter-section');
const cardsArea = document.getElementById('cards-area');
const cardsContainer = document.getElementById('cards-container');
const poolDisplay = document.getElementById('pool-display');

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
    if (current.length >= MAX) { showMsg('وصلت للحد الأقصى 50 كرة!', 'red'); return; }
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
  confirmBtn.textContent = (phase === 1 ? 'تأكيد الاختيار الأول' : 'تأكيد الاختيار الثاني') + ' (' + cnt + '/50)';
  confirmBtn.disabled = cnt !== MAX;
  if (cnt === 0) showMsg('', 'green');
  else if (cnt < MAX) showMsg('تبقى ' + (MAX - cnt) + ' كرة', 'green');
  else showMsg('ممتاز! اضغط التأكيد ✓', 'green');
  renderChips(sel1Nums, sel1, 'chip1');
  renderChips(sel2Nums, sel2, 'chip2');
}

function renderChips(container, arr, cls) {
  container.innerHTML = '';
  arr.slice().sort((a,b)=>a-b).forEach(n => {
    const c = document.createElement('span');
    c.className = 'num-chip ' + cls;
    c.textContent = n;
    container.appendChild(c);
  });
}

function showMsg(txt, type) { msgArea.textContent = txt; msgArea.className = 'msg ' + (type || ''); }

confirmBtn.addEventListener('click', () => {
  if (current.length !== MAX) return;
  if (phase === 1) {
    sel1 = [...current]; current = []; phase = 2;
    phaseVal.textContent = 'الثانية'; phaseBox.className = 'counter-box phase-active';
    phaseHint.textContent = 'الآن اختر 50 كرة للاختيار الثاني';
    sel1Box.classList.add('active1');
    renderChips(sel1Nums, sel1, 'chip1');
    resetGrid(false);
    showMsg('تم حفظ الاختيار الأول ✓', 'green');
  } else {
    sel2 = [...current]; phase = 3; phaseVal.textContent = 'الفلترة';
    phaseHint.textContent = 'اكتمل الاختياران — جاهز للفلترة';
    confirmBtn.style.display = 'none'; filterBtn.style.display = 'block';
    sel2Box.classList.add('active2');
    renderChips(sel2Nums, sel2, 'chip2');
    lockAll(); showMsg('تم الاختيار الثاني ✓ اضغط دخول الفلترة', 'gold');
  }
});

filterBtn.addEventListener('click', () => {
  filterBtn.disabled = true;
  showMsg('جاري معالجة الـ 100 كرة وتطبيق فلتر العبقري 2...', 'gold');
  setTimeout(() => {
    let set1 = new Set(sel1); let set2 = new Set(sel2);
    let common_numbers = sel1.filter(n => set2.has(n));
    let net_draw2 = sel2.filter(n => !set1.has(n));
    let absent_numbers = [];
    for (let i = 1; i <= 90; i++) { if (!set1.has(i) && !set2.has(i)) absent_numbers.push(i); }
    let boxes = {};
    for (let i = 1; i <= 9; i++) boxes[i] = [];
    common_numbers.forEach(num => {
      let boxId = Math.floor((num - 1) / 10) + 1;
      if (boxId >= 1 && boxId <= 9) boxes[boxId].push(num);
    });
    let sortedBoxes = Object.keys(boxes).map(id => ({ id: Number(id), nums: boxes[id] })).sort((a, b) => b.nums.length - a.nums.length);
    let active_common = [];
    for (let i = 0; i < 5; i++) { if (sortedBoxes[i]) active_common = active_common.concat(sortedBoxes[i].nums); }
    let poolSet = new Set([...active_common, ...net_draw2, ...absent_numbers]);
    let pool = Array.from(poolSet).sort((a, b) => a - b);
    
    document.getElementById('stat-pool').textContent = pool.length;
    document.getElementById('stat-common').textContent = common_numbers.length;
    document.getElementById('stat-net2').textContent = net_draw2.length;
    document.getElementById('stat-absent').textContent = absent_numbers.length;

    poolDisplay.innerHTML = '';
    const commonSet = new Set(active_common);
    pool.forEach(n => {
      const c = document.createElement('span');
      c.className = 'pool-chip' + (commonSet.has(n) ? ' common' : '');
      c.textContent = n;
      poolDisplay.appendChild(c);
    });

    let getRnd = (arr, n) => {
      let a = [...arr];
      for (let i = a.length - 1; i > 0; i--) { let