const FRUITS = [
    {
        name: 'Apple', color: '#e8836a',
        img:  'https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=400&h=600&fit=crop',
        desc: 'Crisp, sweet and packed with nutrients. Upload a photo and our AI tells you instantly if it\'s fresh, can be eaten, or rotten.',
        origin: 'Central Asia', originSub: '🌍 Grown in 90+ countries',
        types: ['Fuji', 'Gala', 'Granny Smith', 'Honeycrisp'],
        nutrients: ['Vitamin C', 'Potassium', 'Fiber'],
    },
    {
        name: 'Mango', color: '#e8a838',
        img:  'https://images.unsplash.com/photo-1601493700631-2b16ec4b4716?w=400&h=600&fit=crop',
        desc: 'Tropical, juicy and rich in vitamins. Detect ripeness and freshness with a single photo — no guessing.',
        origin: 'South Asia', originSub: '🌏 India, Thailand, Mexico',
        types: ['Alphonso', 'Ataulfo', 'Kent', 'Tommy Atkins'],
        nutrients: ['Vitamin A', 'Vitamin C', 'Copper'],
    },
    {
        name: 'Strawberry', color: '#c94060',
        img:  'https://images.unsplash.com/photo-1543528176-61b239494933?w=400&h=600&fit=crop',
        desc: 'Delicate and perishable. Strawberries rot fast — our AI gives you a precise freshness window so nothing goes to waste.',
        origin: 'North America', originSub: '🌎 USA, Spain, Mexico',
        types: ['Albion', 'Chandler', 'Seascape', 'Camarosa'],
        nutrients: ['Vitamin C', 'Folate', 'Manganese'],
    },
    {
        name: 'Blueberry', color: '#5b6abf',
        img:  'https://images.unsplash.com/photo-1498557850523-fd3d118b962e?w=400&h=600&fit=crop',
        desc: 'Tiny but powerful. Blueberries are packed with antioxidants. Our model detects freshness from colour and texture patterns.',
        origin: 'North America', originSub: '🌎 USA, Canada, Chile',
        types: ['Highbush', 'Lowbush', 'Rabbiteye', 'Half-high'],
        nutrients: ['Vitamin C', 'Vitamin K', 'Manganese'],
    },
];

const page          = document.getElementById('page');
const navTabs       = document.querySelectorAll('.tab');
const bgWord        = document.getElementById('bgWord');
const heroTitle     = document.getElementById('heroTitle');
const heroDesc      = document.getElementById('heroDesc');
const heroBadges    = document.getElementById('heroBadges');
const canImg        = document.getElementById('canImg');
const canLabelName  = document.getElementById('canLabelName');
const heroCenter    = document.getElementById('heroCenter');
const infoOrigin    = document.getElementById('infoOrigin');
const infoOriginSub = document.getElementById('infoOriginSub');
const infoTypes     = document.getElementById('infoTypes');
const infoNutrients = document.getElementById('infoNutrients');
const dotsWrap      = document.getElementById('dots');

let current = 0, autoTimer;

// Build dots
FRUITS.forEach((_, i) => {
    const d = document.createElement('div');
    d.className = 'dot' + (i === 0 ? ' active' : '');
    d.addEventListener('click', () => { goTo(i); resetAuto(); });
    dotsWrap.appendChild(d);
});

function goTo(idx) {
    current = ((idx % FRUITS.length) + FRUITS.length) % FRUITS.length;
    render();
}

function render() {
    const f = FRUITS[current];

    page.style.background    = f.color;
    bgWord.textContent       = f.name;
    heroTitle.textContent    = f.name;
    heroDesc.textContent     = f.desc;
    canLabelName.textContent = f.name;

    // Can image fade
    canImg.style.opacity = '0';
    setTimeout(() => { canImg.src = f.img; canImg.style.opacity = '1'; }, 250);

    // Right info cards
    if (infoOrigin)    infoOrigin.textContent    = f.origin;
    if (infoOriginSub) infoOriginSub.textContent = f.originSub;
    if (infoTypes)     infoTypes.innerHTML = f.types.map(t => '<span>' + t + '</span>').join('');
    if (infoNutrients) infoNutrients.innerHTML = f.nutrients.map(n => '<span>' + n + '</span>').join('');

    heroBadges.innerHTML = f.nutrients.map(n => '<span class="badge">' + n + '</span>').join('');

    // Remove old slices
    heroCenter.querySelectorAll('.slice').forEach(s => s.remove());

    // Tabs & dots
    navTabs.forEach((t, i) => t.classList.toggle('active', i === current));
    dotsWrap.querySelectorAll('.dot').forEach((d, i) => d.classList.toggle('active', i === current));
}

navTabs.forEach((tab, i) => tab.addEventListener('click', () => { goTo(i); resetAuto(); }));

document.addEventListener('keydown', e => {
    if (e.key === 'ArrowRight') { goTo(current + 1); resetAuto(); }
    if (e.key === 'ArrowLeft')  { goTo(current - 1); resetAuto(); }
});

let tx = 0;
document.addEventListener('touchstart', e => { tx = e.touches[0].clientX; }, { passive: true });
document.addEventListener('touchend',   e => {
    const dx = e.changedTouches[0].clientX - tx;
    if (Math.abs(dx) > 50) { dx < 0 ? goTo(current + 1) : goTo(current - 1); resetAuto(); }
});

function startAuto() { autoTimer = setInterval(() => goTo(current + 1), 3500); }
function resetAuto()  { clearInterval(autoTimer); startAuto(); }

render();
startAuto();
