// ── DOM refs ─────────────────────────────────────────────────────
const uploadBox       = document.getElementById('uploadBox');
const imageUpload     = document.getElementById('imageUpload');
const previewImg      = document.getElementById('previewImg');
const changeBtn       = document.getElementById('changeBtn');
const uploadBtn       = document.getElementById('uploadBtn');
const uploadStatus    = document.getElementById('uploadStatus');
const fruitSelect     = document.getElementById('fruitSelect');
const resultBox       = document.getElementById('resultBox');
const resultLabel     = document.getElementById('resultLabel');
const resultConf      = document.getElementById('resultConf');
const comparisonPanel = document.getElementById('comparisonPanel');
const uploadedPreview = document.getElementById('uploadedPreview');
const referenceImg    = document.getElementById('referenceImg');
const referenceLabel  = document.getElementById('referenceLabel');
const statAcc         = document.getElementById('statAcc');
const statTraining    = document.getElementById('statTraining');

// Modal
const resultModal      = document.getElementById('resultModal');
const modalClose       = document.getElementById('modalClose');
const modalIcon        = document.getElementById('modalIcon');
const modalTitle       = document.getElementById('modalTitle');
const modalFruit       = document.getElementById('modalFruit');
const barFresh         = document.getElementById('barFresh');
const barRotten        = document.getElementById('barRotten');
const scoreFresh       = document.getElementById('scoreFresh');
const scoreRotten      = document.getElementById('scoreRotten');
const daysSection      = document.getElementById('daysSection');
const daysCount        = document.getElementById('daysCount');
const daysBar          = document.getElementById('daysBar');
const daysMsg          = document.getElementById('daysMsg');
const modalUploadedImg = document.getElementById('modalUploadedImg');
const modalRefImg      = document.getElementById('modalRefImg');
const adviceIcon       = document.getElementById('adviceIcon');
const adviceEdible     = document.getElementById('adviceEdible');
const adviceShelf      = document.getElementById('adviceShelf');
const adviceDays       = document.getElementById('adviceDays');

let lastFilename = null;

// ── Emoji background ──────────────────────────────────────────────
(function () {
    const bgImg  = document.getElementById('heroBgImg');
    const bgWord = document.getElementById('heroBgWord');
    if (!bgImg || typeof FRUITS === 'undefined') return;

    const COLORS = {
        'Apple':'#e8836a','Banana':'#e8c84a','Mango':'#e8a838',
        'Orange':'#e89030','Grapes':'#8878c8','Strawberry':'#c94060',
        'Watermelon':'#48a870','Pineapple':'#d8b830','Papaya':'#e89858',
        'Kiwi':'#78a840','Cherry':'#b83060','Pomegranate':'#c83040',
        'Pear':'#98b840','Peach':'#e8a878','Blueberry':'#5b6abf',
    };

    const POSITIONS = [
        { top:'5%',  left:'3%',   size:'120px', rot:'-20deg', dur:'7s',  delay:'0s'   },
        { top:'25%', left:'1%',   size:'80px',  rot:'15deg',  dur:'5.5s',delay:'1s'   },
        { top:'50%', left:'4%',   size:'100px', rot:'-10deg', dur:'8s',  delay:'2s'   },
        { top:'75%', left:'2%',   size:'70px',  rot:'22deg',  dur:'6s',  delay:'0.5s' },
        { top:'90%', left:'8%',   size:'90px',  rot:'-15deg', dur:'9s',  delay:'1.5s' },
        { top:'10%', left:'25%',  size:'140px', rot:'10deg',  dur:'9s',  delay:'0.5s' },
        { top:'40%', left:'20%',  size:'65px',  rot:'-8deg',  dur:'6s',  delay:'2.5s' },
        { top:'70%', left:'22%',  size:'110px', rot:'18deg',  dur:'7.5s',delay:'1s'   },
        { top:'15%', right:'25%', size:'100px', rot:'12deg',  dur:'8s',  delay:'1.5s' },
        { top:'45%', right:'22%', size:'75px',  rot:'-18deg', dur:'6s',  delay:'0.8s' },
        { top:'80%', right:'20%', size:'120px', rot:'8deg',   dur:'7s',  delay:'3s'   },
        { top:'8%',  right:'4%',  size:'130px', rot:'-5deg',  dur:'10s', delay:'2.5s' },
        { top:'35%', right:'2%',  size:'85px',  rot:'20deg',  dur:'6.5s',delay:'0.3s' },
        { top:'60%', right:'5%',  size:'95px',  rot:'-12deg', dur:'8s',  delay:'1.8s' },
        { top:'88%', right:'3%',  size:'70px',  rot:'16deg',  dur:'5s',  delay:'2s'   },
        { top:'55%', left:'45%',  size:'160px', rot:'-6deg',  dur:'11s', delay:'4s'   },
    ];

    let current = 0, timer;

    function goTo(idx) {
        current = ((idx % FRUITS.length) + FRUITS.length) % FRUITS.length;
        const f = FRUITS[current];
        if (bgWord) bgWord.textContent = f.name;
        document.body.style.background = COLORS[f.name] || '#e8836a';
        bgImg.innerHTML = '';
        POSITIONS.forEach(p => {
            const span = document.createElement('span');
            span.className = 'bg-emoji';
            span.style.cssText = [
                p.top   ? 'top:'   + p.top   : '',
                p.left  ? 'left:'  + p.left  : '',
                p.right ? 'right:' + p.right : '',
                '--size:' + p.size, '--rot:' + p.rot,
                '--dur:'  + p.dur,  '--delay:' + p.delay,
            ].filter(Boolean).join(';');
            span.textContent = f.emoji;
            bgImg.appendChild(span);
        });
    }

    function startTimer() { timer = setInterval(() => goTo(current + 1), 2500); }
    function resetTimer()  { clearInterval(timer); startTimer(); }

    goTo(0);
    startTimer();
})();

// ── Status poll ───────────────────────────────────────────────────
async function pollStatus() {
    try {
        const d = await (await fetch('/status')).json();
        if (statAcc) statAcc.textContent = d.accuracy != null ? (typeof d.accuracy === 'number' ? d.accuracy + '%' : d.accuracy) : 'Not trained';
        if (statTraining) statTraining.classList.toggle('hidden', !d.training);
    } catch {}
}
pollStatus();
setInterval(pollStatus, 6000);

// ── File handling ─────────────────────────────────────────────────
uploadBox.addEventListener('click', () => imageUpload.click());
uploadBox.addEventListener('dragover', e => { e.preventDefault(); uploadBox.classList.add('drag-over'); });
uploadBox.addEventListener('dragleave', () => uploadBox.classList.remove('drag-over'));
uploadBox.addEventListener('drop', e => { e.preventDefault(); uploadBox.classList.remove('drag-over'); if (e.dataTransfer.files[0]) handleFile(e.dataTransfer.files[0]); });
imageUpload.addEventListener('change', () => { if (imageUpload.files[0]) handleFile(imageUpload.files[0]); });

function handleFile(file) {
    if (!['image/jpeg','image/jpg','image/png'].includes(file.type)) {
        showStatus('Only JPG and PNG accepted.', false); return;
    }
    const reader = new FileReader();
    reader.onload = e => {
        previewImg.src = e.target.result;
        previewImg.classList.remove('hidden');
        uploadBox.style.display = 'none';
        changeBtn.classList.remove('hidden');
        resultBox.classList.add('hidden');
        if (comparisonPanel) comparisonPanel.classList.add('hidden');
        showStatus('Ready.', true);
    };
    reader.readAsDataURL(file);
}

changeBtn.addEventListener('click', () => {
    imageUpload.value = '';
    previewImg.src = '';
    previewImg.classList.add('hidden');
    uploadBox.style.display = '';
    changeBtn.classList.add('hidden');
    resultBox.classList.add('hidden');
    if (comparisonPanel) comparisonPanel.classList.add('hidden');
    showStatus('', true);
    lastFilename = null;
});

// ── Analyse ───────────────────────────────────────────────────────
uploadBtn.addEventListener('click', async () => {
    if (!fruitSelect.value) { showStatus('Select a fruit first.', false); return; }
    if (!imageUpload.files[0]) { showStatus('Upload an image first.', false); return; }

    uploadBtn.disabled = true;
    uploadBtn.textContent = '⏳ Analysing…';
    showStatus('', true);
    resultBox.classList.add('hidden');
    if (comparisonPanel) comparisonPanel.classList.add('hidden');

    const fd = new FormData();
    fd.append('image', imageUpload.files[0]);
    fd.append('fruit', fruitSelect.value);

    try {
        const res  = await fetch('/predict', { method: 'POST', body: fd });
        const data = await res.json();

        if (data.error) {
            showStatus(data.error, false);
        } else if (data.label === 'Unknown') {
            showStatus(data.message || 'Model not trained yet.', false);
        } else {
            lastFilename = data.filename;
            showSidebarResult(data.verdict, data.fresh_pct, data.fruit);
            showComparison(data.fruit, data.verdict, data.fresh_pct);
            openModal(data.verdict, data.fruit, data.fresh_pct, data.rotten_pct, data.days_left);
        }
    } catch {
        showStatus('Server unreachable. Is Flask running?', false);
    } finally {
        uploadBtn.disabled = false;
        uploadBtn.textContent = '🔍 Analyse';
    }
});

// ── Sidebar result ────────────────────────────────────────────────
function showSidebarResult(verdict, freshPct, fruit) {
    const cls = verdict === 'Fresh' ? 'result-fresh' : verdict === 'Can be Eaten' ? 'result-unknown' : 'result-rotten';
    resultLabel.textContent = cap(fruit) + ' — ' + verdict;
    resultLabel.className   = cls;
    resultConf.textContent  = 'Freshness: ' + freshPct + '%';
    resultBox.classList.remove('hidden');
}

// ── Comparison panel ──────────────────────────────────────────────
function showComparison(fruit, verdict, freshPct) {
    if (!comparisonPanel) return;
    uploadedPreview.src = previewImg.src;
    const fd = FRUITS.find(f => f.name.toLowerCase() === fruit.toLowerCase());
    if (fd) { referenceImg.src = fd.img; referenceLabel.textContent = 'Fresh ' + fd.name; }
    const compBadge = document.getElementById('compBadge');
    const compConf  = document.getElementById('compConf');
    if (compBadge) {
        compBadge.textContent = verdict === 'Fresh' ? '✅ Fresh' : verdict === 'Can be Eaten' ? '⚠️ Can be Eaten' : '❌ Rotten';
        compBadge.className   = 'comp-badge ' + (verdict === 'Fresh' ? 'badge-fresh' : verdict === 'Can be Eaten' ? 'badge-unknown' : 'badge-rotten');
    }
    if (compConf) compConf.textContent = 'Freshness: ' + freshPct + '%';
    comparisonPanel.classList.remove('hidden');
    comparisonPanel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// ── Modal ─────────────────────────────────────────────────────────
function openModal(verdict, fruit, freshPct, rottenPct, daysLeft) {
    const fd = FRUITS.find(f => f.name.toLowerCase() === fruit.toLowerCase());
    const icons = { 'Fresh': '✅', 'Can be Eaten': '⚠️', 'Rotten': '❌' };
    const cls   = { 'Fresh': 'fresh-title', 'Can be Eaten': 'warn-title', 'Rotten': 'rotten-title' };

    modalIcon.textContent  = icons[verdict] || '🔍';
    modalTitle.textContent = verdict;
    modalTitle.className   = 'modal-title ' + (cls[verdict] || '');
    modalFruit.textContent = cap(fruit);

    // Reset bars
    barFresh.style.width    = '0%';
    barRotten.style.width   = '0%';
    scoreFresh.textContent  = '0%';
    scoreRotten.textContent = '0%';

    modalUploadedImg.src = previewImg.src;
    modalRefImg.src      = fd ? fd.img : '';

    // Days remaining
    const maxDays = { apple:14, banana:5, mango:6, orange:14, grapes:7,
        strawberry:3, watermelon:10, pineapple:5, papaya:5,
        kiwi:7, cherry:5, pomegranate:14, pear:7, peach:5, blueberry:7 };
    const max   = maxDays[fruit.toLowerCase()] || 7;
    const pct   = daysLeft != null ? Math.min(100, Math.round((daysLeft / max) * 100)) : 0;
    const color = daysLeft > 5 ? '#4ade80' : daysLeft > 2 ? '#fbbf24' : '#f87171';

    daysCount.textContent    = daysLeft != null ? daysLeft + ' day' + (daysLeft !== 1 ? 's' : '') + ' remaining' : '—';
    daysBar.style.width      = '0%';
    daysBar.style.background = color;

    if (verdict === 'Fresh') {
        daysMsg.textContent = 'Safe to eat. Best consumed within ' + daysLeft + ' day' + (daysLeft !== 1 ? 's' : '');
        daysMsg.style.color = '#4ade80';
    } else if (verdict === 'Can be Eaten') {
        daysMsg.textContent = 'Consume soon — only ' + daysLeft + ' day' + (daysLeft !== 1 ? 's' : '') + ' left';
        daysMsg.style.color = '#fbbf24';
    } else {
        daysMsg.textContent = 'Do not eat — discard immediately';
        daysMsg.style.color = '#f87171';
    }

    // Advice
    adviceIcon.textContent    = icons[verdict] || '';
    adviceEdible.textContent  = verdict;
    adviceShelf.style.display = 'none';
    adviceDays.innerHTML      = '';

    resultModal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';

    requestAnimationFrame(() => requestAnimationFrame(() => {
        barFresh.style.width   = freshPct + '%';
        barRotten.style.width  = rottenPct + '%';
        animateNum(scoreFresh,  freshPct);
        animateNum(scoreRotten, rottenPct);
        daysBar.style.width = pct + '%';
    }));
}

function animateNum(el, target) {
    let n = 0;
    const step = () => { n = Math.min(n + 2, target); el.textContent = n + '%'; if (n < target) requestAnimationFrame(step); };
    requestAnimationFrame(step);
}

modalClose.addEventListener('click', closeModal);
resultModal.addEventListener('click', e => { if (e.target === resultModal) closeModal(); });
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });

function closeModal() {
    resultModal.classList.remove('hidden');
    resultModal.classList.add('hidden');
    document.body.style.overflow = '';
    resetSidebar();
}

// ── Reset ─────────────────────────────────────────────────────────
function resetSidebar() {
    imageUpload.value = '';
    previewImg.src = '';
    previewImg.classList.add('hidden');
    uploadBox.style.display = '';
    changeBtn.classList.add('hidden');
    resultBox.classList.add('hidden');
    showStatus('', true);
    lastFilename = null;
}

function showStatus(msg, ok) {
    uploadStatus.textContent = msg;
    uploadStatus.className   = ok ? 'upload-status success' : 'upload-status error';
}

function cap(s) { return s.charAt(0).toUpperCase() + s.slice(1); }
