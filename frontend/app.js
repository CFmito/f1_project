let driversData = [];

// Главная инициализация приложения после полной загрузки DOM
document.addEventListener('DOMContentLoaded', () => {
    fetchDrivers();
    fetchNextRace();
    fetchLeaderboard();
    loadTeamHistory();
    initRandomizer();
    initReactionGame();
    initMiniRaceGame();
    initModalEvents();
});

// 1. Таймер обратного отсчета Гран-при
async function fetchNextRace() {
    try {
        const res = await fetch('/api/next-race');
        if (!res.ok) throw new Error(`HTTP error! Status: ${res.status}`);
        const race = await res.json();

        const titleEl = document.getElementById('race-title');
        const locEl = document.getElementById('race-location');

        if (titleEl) titleEl.innerText = `${race.title} (${race.circuit})`;
        if (locEl) locEl.innerText = `📍 ${race.location}`;

        const raceDate = new Date(race.race_time).getTime();

        setInterval(() => {
            const now = new Date().getTime();
            const diff = raceDate - now;

            if (diff <= 0) return;

            const days = Math.floor(diff / (1000 * 60 * 60 * 24));
            const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((diff % (1000 * 60)) / 1000);

            const dEl = document.getElementById('timer-days');
            const hEl = document.getElementById('timer-hours');
            const mEl = document.getElementById('timer-minutes');
            const sEl = document.getElementById('timer-seconds');

            if (dEl) dEl.innerText = String(days).padStart(2, '0');
            if (hEl) hEl.innerText = String(hours).padStart(2, '0');
            if (mEl) mEl.innerText = String(minutes).padStart(2, '0');
            if (sEl) sEl.innerText = String(seconds).padStart(2, '0');
        }, 1000);
    } catch (e) {
        console.error('Ошибка загрузки гонки:', e);
    }
}

// 2. История команды
async function loadTeamHistory() {
    const container = document.getElementById('history-timeline');
    if (!container) return;

    try {
        const response = await fetch('/api/team-history');
        if (!response.ok) throw new Error(`HTTP status: ${response.status}`);

        const historyData = await response.json();

        container.innerHTML = historyData.map(item => `
            <div class="border-l-4 border-cyanAccent pl-4 py-3 my-4 bg-navyCard/60 rounded-r-xl border border-navyBorder shadow-lg">
                <span class="text-cyanAccent font-bold text-sm block mb-1">${item.year}</span>
                <h3 class="text-white font-bold text-lg mb-1">${item.title}</h3>
                <p class="text-slate-300 text-sm leading-relaxed">${item.description}</p>
            </div>
        `).join('');
    } catch (error) {
        console.error('Ошибка загрузки истории:', error);
    }
}

// 3. Загрузка карточек пилотов
async function fetchDrivers() {
    const container = document.getElementById('drivers-container');
    if (!container) return;

    try {
        const response = await fetch('/api/drivers');
        if (!response.ok) throw new Error('Ошибка сети');
        driversData = await response.json();

        container.innerHTML = driversData.map(d => `
            <div onclick="openDriverModal('${d.id}')" class="bg-navyCard border border-navyBorder rounded-2xl overflow-hidden hover:border-cyanAccent hover:scale-[1.02] transition duration-300 shadow-xl cursor-pointer group flex flex-col justify-between">
                <div>
                    <div class="overflow-hidden h-64">
                        <img src="${d.image_url}" alt="${d.name}" class="w-full h-full object-cover group-hover:scale-105 transition duration-500">
                    </div>
                    <div class="p-6">
                        <div class="flex justify-between items-start mb-2">
                            <h4 class="text-2xl font-bold text-white group-hover:text-cyanAccent transition">${d.name}</h4>
                            <span class="text-3xl font-black text-cyanAccent italic">#${d.number}</span>
                        </div>
                        <p class="text-xs text-blue-400 font-semibold mb-3 uppercase tracking-wider">${d.team}</p>
                        <p class="text-slate-400 text-sm line-clamp-2 mb-4">${d.bio}</p>
                    </div>
                </div>
                
                <div class="px-6 pb-6 pt-2">
                    <div class="flex justify-between text-xs text-slate-300 pt-3 border-t border-navyBorder">
                        <span>🏆 Подиумы: <b>${d.podiums}</b></span>
                        <span>👑 Титулы: <b>${d.world_titles}</b></span>
                    </div>
                    <span class="block text-center text-xs text-cyanAccent font-semibold mt-3 opacity-0 group-hover:opacity-100 transition">
                        Нажмите, чтобы узнать больше →
                    </span>
                </div>
            </div>
        `).join('');
    } catch (err) {
        console.error(err);
        container.innerHTML = `<div class="text-red-400">Не удалось загрузить данные с сервера.</div>`;
    }
}

// 4. Таблица лидеров (Leaderboard)
async function fetchLeaderboard() {
    const listEl = document.getElementById('leaderboard-list');
    if (!listEl) return;

    try {
        const res = await fetch('/api/leaderboard');
        if (!res.ok) throw new Error(`HTTP status: ${res.status}`);
        const leaderboard = await res.json();

        listEl.innerHTML = leaderboard.map((item, idx) => `
            <li class="flex justify-between items-center bg-navyBg/60 px-3 py-1.5 rounded-lg border border-navyBorder">
                <span><b>${idx + 1}.</b> ${item.player}</span>
                <span class="font-mono text-cyanAccent font-bold">${item.time_ms} ms</span>
            </li>
        `).join('');
    } catch (e) {
        console.error('Ошибка загрузки лидерборда', e);
    }
}

async function saveScoreToApi(playerName, timeMs) {
    try {
        await fetch('/api/leaderboard', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ player: playerName, time_ms: timeMs })
        });
        fetchLeaderboard();
    } catch (e) {
        console.error('Ошибка сохранения счета', e);
    }
}

// 5. Модальное окно пилота
function openDriverModal(id) {
    const driver = driversData.find(d => d.id === id);
    if (!driver) return;

    document.getElementById('modal-img').src = driver.image_url;
    document.getElementById('modal-name').innerText = driver.name;
    document.getElementById('modal-number').innerText = `#${driver.number}`;
    document.getElementById('modal-team').innerText = driver.team;
    document.getElementById('modal-bio').innerText = driver.bio;
    document.getElementById('modal-podiums').innerText = driver.podiums;
    document.getElementById('modal-titles').innerText = driver.world_titles;

    document.getElementById('driver-modal').classList.remove('hidden');
}

function initModalEvents() {
    const modal = document.getElementById('driver-modal');
    const closeBtn = document.getElementById('close-modal-btn');
    if (!modal || !closeBtn) return;

    closeBtn.addEventListener('click', () => modal.classList.add('hidden'));
    modal.addEventListener('click', (e) => { if (e.target === modal) modal.classList.add('hidden'); });
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') modal.classList.add('hidden'); });
}

// 6. Рандомайзер болида
function initRandomizer() {
    const btn = document.getElementById('randomize-btn');
    const resultBox = document.getElementById('car-result');
    if (!btn || !resultBox) return;

    btn.addEventListener('click', async () => {
        try {
            btn.innerText = '⚙️ Генерация...';
            const response = await fetch('/api/random-car');
            const car = await response.json();

            document.getElementById('res-chassis').innerText = car.chassis;
            document.getElementById('res-engine').innerText = car.engine;
            document.getElementById('res-tyres').innerText = car.tyres;
            document.getElementById('res-strategy').innerText = car.strategy;
            document.getElementById('res-score').innerText = `${car.score} / 100`;

            resultBox.classList.remove('hidden');
        } catch (err) {
            alert('Ошибка обращения к Python API');
        } finally {
            btn.innerText = '🏎️ Собрать болид';
        }
    });
}

// 7. Игра: Тест Реакции
function initReactionGame() {
    const startBtn = document.getElementById('start-reaction-btn');
    const statusText = document.getElementById('reaction-status');
    const lights = document.querySelectorAll('.light-circle');
    const lightsContainer = document.getElementById('lights-container');
    if (!startBtn || !statusText || !lightsContainer) return;

    let startTime, timerId, intervalId;
    let gameState = 'idle'; 

    function resetLights() {
        lights.forEach(l => l.className = 'w-8 h-8 rounded-full bg-slate-800 light-circle');
    }

    startBtn.addEventListener('click', () => {
        startBtn.blur();

        clearTimeout(timerId);
        clearInterval(intervalId);

        gameState = 'waiting';
        resetLights();
        statusText.innerText = 'Внимание... Приготовьтесь!';
        statusText.className = 'text-lg font-bold mb-4 text-amber-400';

        let currentLight = 0;
        intervalId = setInterval(() => {
            if (currentLight < 5) {
                lights[currentLight].className = 'w-8 h-8 rounded-full bg-red-600 shadow-lg shadow-red-500 light-circle';
                currentLight++;
            } else {
                clearInterval(intervalId);
                const delay = Math.random() * 2500 + 1000;
                timerId = setTimeout(() => {
                    resetLights();
                    startTime = Date.now();
                    gameState = 'ready';
                    statusText.innerText = 'ЖМИ!';
                    statusText.className = 'text-2xl font-black mb-4 text-emerald-400 animate-bounce';
                }, delay);
            }
        }, 800);
    });

    async function handleInteraction() {
        if (gameState === 'waiting') {
            clearTimeout(timerId);
            clearInterval(intervalId);
            gameState = 'idle';
            statusText.innerText = '❌ Фальстарт! Попробуйте снова.';
            statusText.className = 'text-lg font-bold mb-4 text-red-400';
            resetLights();
        } else if (gameState === 'ready') {
            const reactionTime = Date.now() - startTime;
            gameState = 'idle';

            statusText.innerText = `🏁 Ваша реакция: ${reactionTime} ms!`;
            statusText.className = 'text-xl font-extrabold mb-4 text-cyanAccent';

            setTimeout(async () => {
                const playerName = prompt(`Ваш результат: ${reactionTime} ms!\nВведите ваше имя для таблицы лидеров:`);
                if (playerName && playerName.trim()) {
                    await saveScoreToApi(playerName.trim(), reactionTime);
                }
            }, 100);
        }
    }

    lightsContainer.addEventListener('click', handleInteraction);

    document.addEventListener('keydown', (e) => {
        if (e.code === 'Space') {
            if (gameState === 'waiting' || gameState === 'ready') {
                e.preventDefault(); 
                handleInteraction();
            }
        }
    });
}

// 8. Мини-гонка на Canvas
function initMiniRaceGame() {
    const canvas = document.getElementById('raceCanvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const startBtn = document.getElementById('start-race-btn');
    const scoreText = document.getElementById('race-score');

    let player = { x: 120, y: 250, width: 35, height: 55 };
    let obstacles = [];
    let score = 0;
    let gameLoopId = null;
    let isRunning = false;

    function drawPlayer() {
        ctx.fillStyle = '#00d2ff';
        ctx.fillRect(player.x, player.y, player.width, player.height);
        ctx.fillStyle = '#000';
        ctx.fillRect(player.x - 4, player.y + 5, 5, 12);
        ctx.fillRect(player.x + player.width - 1, player.y + 5, 5, 12);
        ctx.fillRect(player.x - 4, player.y + 35, 5, 12);
        ctx.fillRect(player.x + player.width - 1, player.y + 35, 5, 12);
    }

    function spawnObstacle() {
        if (Math.random() < 0.03) {
            const laneX = [25, 120, 215][Math.floor(Math.random() * 3)];
            obstacles.push({ x: laneX, y: -60, width: 35, height: 55 });
        }
    }

    function update() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        ctx.strokeStyle = '#1e293b';
        ctx.setLineDash([15, 10]);
        ctx.beginPath();
        ctx.moveTo(93, 0); ctx.lineTo(93, canvas.height);
        ctx.moveTo(186, 0); ctx.lineTo(186, canvas.height);
        ctx.stroke();

        drawPlayer();
        spawnObstacle();

        for (let i = 0; i < obstacles.length; i++) {
            let obs = obstacles[i];
            obs.y += 4;

            ctx.fillStyle = '#3b82f6';
            ctx.fillRect(obs.x, obs.y, obs.width, obs.height);

            if (
                player.x < obs.x + obs.width &&
                player.x + player.width > obs.x &&
                player.y < obs.y + obs.height &&
                player.y + player.height > obs.y
            ) {
                gameOver();
                return;
            }

            if (obs.y > canvas.height) {
                obstacles.splice(i, 1);
                score += 10;
                scoreText.innerText = `Счет: ${score}`;
            }
        }

        gameLoopId = requestAnimationFrame(update);
    }

    function gameOver() {
        cancelAnimationFrame(gameLoopId);
        isRunning = false;
        alert(`💥 Столкновение! Ваш счет: ${score}`);
        if (startBtn) startBtn.innerText = 'Играть снова';
    }

    if (startBtn) {
        startBtn.addEventListener('click', () => {
            if (isRunning) return;
            isRunning = true;
            score = 0;
            player.x = 120;
            obstacles = [];
            scoreText.innerText = 'Счет: 0';
            update();
        });
    }

    document.addEventListener('keydown', (e) => {
        if (!isRunning) return;
        if ((e.key === 'ArrowLeft' || e.key === 'a' || e.key === 'A' || e.key === 'ф' || e.key === 'Ф') && player.x > 15) {
            player.x -= 25;
        }
        if ((e.key === 'ArrowRight' || e.key === 'd' || e.key === 'D' || e.key === 'в' || e.key === 'В') && player.x < canvas.width - 50) {
            player.x += 25;
        }
    });
}