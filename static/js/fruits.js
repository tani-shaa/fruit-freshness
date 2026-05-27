const FRUITS = [
    {
        name: "Apple", emoji: "🍎",
        img: "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=400&h=300&fit=crop",
        benefits: "Boosts heart health, aids digestion, and helps manage blood sugar levels.",
        vitamins: "Vitamin C, Vitamin B6",
        minerals: "Potassium, Manganese"
    },
    {
        name: "Banana", emoji: "🍌",
        img: "https://images.unsplash.com/photo-1603833665858-e61d17a86224?w=400&h=300&fit=crop",
        benefits: "Provides quick energy, supports gut health, and reduces muscle cramps.",
        vitamins: "Vitamin B6, Vitamin C",
        minerals: "Potassium, Magnesium"
    },
    {
        name: "Mango", emoji: "🥭",
        img: "https://images.unsplash.com/photo-1601493700631-2b16ec4b4716?w=400&h=300&fit=crop",
        benefits: "Supports eye health, boosts immunity, and aids digestion with enzymes.",
        vitamins: "Vitamin A, Vitamin C, Vitamin E",
        minerals: "Potassium, Copper"
    },
    {
        name: "Orange", emoji: "🍊",
        img: "https://images.unsplash.com/photo-1580052614034-c55d20bfee3b?w=400&h=300&fit=crop",
        benefits: "Strengthens immunity, improves skin health, and lowers cholesterol.",
        vitamins: "Vitamin C, Folate",
        minerals: "Calcium, Potassium"
    },
    {
        name: "Grapes", emoji: "🍇",
        img: "https://images.unsplash.com/photo-1423483641154-5411ec9c0ddf?w=400&h=300&fit=crop",
        benefits: "Rich in antioxidants, supports heart health, and has anti-inflammatory effects.",
        vitamins: "Vitamin C, Vitamin K",
        minerals: "Potassium, Copper"
    },
    {
        name: "Strawberry", emoji: "🍓",
        img: "https://images.unsplash.com/photo-1543528176-61b239494933?w=400&h=300&fit=crop",
        benefits: "Improves blood sugar control, reduces inflammation, and boosts skin glow.",
        vitamins: "Vitamin C, Folate",
        minerals: "Manganese, Potassium"
    },
    {
        name: "Watermelon", emoji: "🍉",
        img: "https://images.unsplash.com/photo-1589984662646-e7b2e4962f18?w=400&h=300&fit=crop",
        benefits: "Keeps you hydrated, reduces muscle soreness, and supports heart health.",
        vitamins: "Vitamin A, Vitamin C",
        minerals: "Potassium, Magnesium"
    },
    {
        name: "Pineapple", emoji: "🍍",
        img: "https://images.unsplash.com/photo-1490885578174-acda8905c2c6?w=400&h=300&fit=crop",
        benefits: "Contains bromelain for digestion, boosts immunity, and reduces inflammation.",
        vitamins: "Vitamin C, Vitamin B6",
        minerals: "Manganese, Copper"
    },
    {
        name: "Papaya", emoji: "🧡",
        img: "https://images.unsplash.com/photo-1526318472351-c75fcf070305?w=400&h=300&fit=crop",
        benefits: "Contains papain enzyme for digestion, reduces inflammation, and boosts immunity.",
        vitamins: "Vitamin A, Vitamin C, Folate",
        minerals: "Potassium, Magnesium"
    },
    {
        name: "Kiwi", emoji: "🥝",
        img: "https://images.unsplash.com/photo-1585059895524-72359e06133a?w=400&h=300&fit=crop",
        benefits: "Improves sleep, supports respiratory health, and is packed with antioxidants.",
        vitamins: "Vitamin C, Vitamin K, Vitamin E",
        minerals: "Potassium, Folate"
    },
    {
        name: "Cherry", emoji: "🍒",
        img: "https://images.unsplash.com/photo-1528821128474-27f963b062bf?w=400&h=300&fit=crop",
        benefits: "Improves sleep quality, reduces gout symptoms, and fights oxidative stress.",
        vitamins: "Vitamin C, Vitamin A",
        minerals: "Potassium, Manganese"
    },
    {
        name: "Pomegranate", emoji: "❤️",
        img: "https://images.unsplash.com/photo-1541344999736-83eca272f6fc?w=400&h=300&fit=crop",
        benefits: "Powerful antioxidants fight free radicals, lowers blood pressure, and improves memory.",
        vitamins: "Vitamin C, Vitamin K, Folate",
        minerals: "Potassium, Copper, Iron"
    },
    {
        name: "Pear", emoji: "🍐",
        img: "https://images.unsplash.com/photo-1568702846914-96b305d2aaeb?w=400&h=300&fit=crop",
        benefits: "High in fiber for gut health, reduces inflammation, and supports heart health.",
        vitamins: "Vitamin C, Vitamin K",
        minerals: "Potassium, Copper"
    },
    {
        name: "Peach", emoji: "🍑",
        img: "https://images.unsplash.com/photo-1595743825637-cdafc8ad4173?w=400&h=300&fit=crop",
        benefits: "Promotes healthy skin, supports digestion, and strengthens the immune system.",
        vitamins: "Vitamin A, Vitamin C",
        minerals: "Potassium, Fluoride"
    },
    {
        name: "Blueberry", emoji: "🫐",
        img: "https://images.unsplash.com/photo-1498557850523-fd3d118b962e?w=400&h=300&fit=crop",
        benefits: "Sharpens memory, protects against aging, and supports urinary tract health.",
        vitamins: "Vitamin C, Vitamin K",
        minerals: "Manganese, Potassium"
    }
];

function buildCards() {
    const grid = document.getElementById('fruitGrid');
    if (!grid) return;
    grid.innerHTML = '';
    FRUITS.forEach(f => {
        const card = document.createElement('div');
        card.className = 'flip-card';
        card.innerHTML = `
        <div class="flip-inner">
            <div class="flip-front">
                <img src="${f.img}" alt="${f.name}"
                     onerror="this.src='https://placehold.co/400x300/FFD6E0/FF8BA7?text=${encodeURIComponent(f.name)}'">
                <div class="card-name">${f.emoji} ${f.name}</div>
            </div>
            <div class="flip-back">
                <div class="back-emoji">${f.emoji}</div>
                <h4>${f.name}</h4>
                <p class="benefit">${f.benefits}</p>
                <div class="nutrient-row">
                    <span class="tag vitamin">💊 ${f.vitamins}</span>
                    <span class="tag mineral">⚙️ ${f.minerals}</span>
                </div>
            </div>
        </div>`;
        grid.appendChild(card);
    });
}

buildCards();

// ── 3D Circular Carousel ─────────────────────────────────────────
(function () {
    const ring    = document.getElementById('carouselRing');
    const label   = document.getElementById('carouselLabel');
    const btnPrev = document.getElementById('carPrev');
    const btnNext = document.getElementById('carNext');

    if (!ring) return;

    const COUNT   = FRUITS.length;          // 15
    const RADIUS  = 260;                    // px — ring radius
    let   current = 0;
    let   autoTimer;

    // Build cards
    FRUITS.forEach((f, i) => {
        const card = document.createElement('div');
        card.className = 'car-card';
        card.dataset.index = i;
        card.innerHTML = `
            <img src="${f.img}" alt="${f.name}"
                 onerror="this.src='https://placehold.co/220x280/111/555?text=${encodeURIComponent(f.name)}'">
            <div class="car-card-name">${f.emoji} ${f.name}</div>`;
        card.addEventListener('click', () => rotateTo(i));
        ring.appendChild(card);
    });

    function rotateTo(idx) {
        current = ((idx % COUNT) + COUNT) % COUNT;
        render();
        resetAuto();
    }

    function render() {
        const cards = ring.querySelectorAll('.car-card');
        const angleStep = 360 / COUNT;

        cards.forEach((card, i) => {
            const offset = i - current;
            // Shortest path around the circle
            const norm   = ((offset % COUNT) + COUNT) % COUNT;
            const angle  = norm <= COUNT / 2 ? norm * angleStep : (norm - COUNT) * angleStep;
            const rad    = angle * Math.PI / 180;

            const x      = Math.sin(rad) * RADIUS;
            const z      = Math.cos(rad) * RADIUS - RADIUS;
            const scale  = 0.55 + 0.45 * ((z + RADIUS) / RADIUS);
            const opacity= 0.3 + 0.7  * ((z + RADIUS) / RADIUS);
            const zIndex = Math.round(scale * 100);

            card.style.transform  = `translateX(${x}px) translateZ(${z}px) scale(${scale})`;
            card.style.opacity    = opacity;
            card.style.zIndex     = zIndex;
            card.classList.toggle('car-active', i === current);
        });

        // Update centre label
        label.textContent = FRUITS[current].name;
    }

    function next() { rotateTo(current + 1); }
    function prev() { rotateTo(current - 1); }

    btnNext.addEventListener('click', next);
    btnPrev.addEventListener('click', prev);

    // Auto-rotate every 2.5s
    function startAuto() { autoTimer = setInterval(next, 2500); }
    function resetAuto()  { clearInterval(autoTimer); startAuto(); }

    // Touch / drag support
    let touchStartX = 0;
    ring.addEventListener('touchstart', e => { touchStartX = e.touches[0].clientX; }, { passive: true });
    ring.addEventListener('touchend',   e => {
        const dx = e.changedTouches[0].clientX - touchStartX;
        if (Math.abs(dx) > 40) dx < 0 ? next() : prev();
    });

    render();
    startAuto();
})();
