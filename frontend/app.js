const API_URL = 'http://localhost:8080/api';

document.addEventListener('DOMContentLoaded', () => {
    fetchDrivers();
    initRandomizer();
    initReactionGame();
    initMiniRaceGame();
});

// 1. Загрузка пилотов с Python бэкенда
async function fetchDrivers() {
    const container = document.getElementById('drivers-container');
    try {
        const response = await fetch(`${API_URL}/drivers`);
        if (!response.ok) throw new Error('Ошибка сети');
        const drivers = await response.json();

        container.innerHTML = drivers.map(d => `
            <div class="bg-navyCard border border-navyBorder rounded-2xl overflow-hidden hover:border-cyanAccent transition duration-300 shadow-lg">
                <img src="${d.image_url}" alt="${d.name}" class="w-full h-48 object-cover">
                <div class="p-5">
                    <div class="flex justify-between items-start mb-2">
                        <h4 class="text-xl font-bold text-white">${d.name}</h4>
                        <span class="text-2xl font-black text-cyanAccent italic">#${d.number}</span>
                    </div>
                    <p class="text-xs text-blue-400 font-semibold mb-3 uppercase tracking-wider">${d.team}</p>
                    <p class="text-slate-400 text-sm mb-4 line-clamp-3">${d.bio}</p>
                    <div class="flex justify-between text-xs text-slate-300 pt-3 border-t border-navyBorder">
                        <span>🏆 Подиумы: <b>${d.podiums}</b></span>
                        <span>👑 Титулы: <b>${d.world_titles}</b></span>
                    </div>
                </div>
            </div>
        `).join('');
    } catch (err) {
        console.error(err);
        container.innerHTML = `<div class="text-red-400">Не удалось загрузить данные с Python-сервера. Проверьте запуск на :8080.</div>`;
    }
}

// 2. Рандомайзер болида
function initRandomizer() {
    const btn = document.getElementById('randomize-btn');
    const resultBox = document.getElementById('car-result');

    btn.addEventListener('click', async () => {
        try {
            btn.innerText = '⚙️ Генерация...';
            const response = await fetch(`${API_URL}/random-car`);
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

// 3. Игра: Тест Реакции
function initReactionGame() {
    const startBtn = document.getElementById('start-reaction-btn');
    const statusText = document.getElementById('reaction-status');
    const lights = document.querySelectorAll('.light-circle');
    let startTime, timerId, gameState = 'idle';

    function resetLights() {
        lights.forEach(l => l.className = 'w-8 h-8 rounded-full bg-slate-800 light-circle');
    }

    startBtn.addEventListener('click', () => {
        if (gameState === 'waiting' || gameState === 'ready') return;
        
        gameState = 'waiting';
        resetLights();
        statusText.innerText = 'Внимание... Приготовьтесь!';
        statusText.className = 'text-lg font-bold mb-4 text-amber-400';

        let currentLight = 0;
        const interval = setInterval(() => {
            if (currentLight < 5) {
                lights[currentLight].className = 'w-8 h-8 rounded-full bg-red-600 shadow-lg shadow-red-500 light-circle';
                currentLight++;
            } else {
                clearInterval(interval);
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

    function handleInteraction() {
        if (gameState === 'waiting') {
            clearTimeout(timerId);
            gameState = 'idle';
            statusText.innerText = '❌ Фальстарт! Попробуйте снова.';
            statusText.className = 'text-lg font-bold mb-4 text-red-400';
            resetLights();
        } else if (gameState === 'ready') {
            const reactionTime = Date.now() - startTime;
            gameState = 'idle';
            statusText.innerText = `🏁 Ваша реакция: ${reactionTime} ms!`;
            statusText.className = 'text-xl font-extrabold mb-4 text-cyanAccent';
        }
    }

    document.getElementById('lights-container').addEventListener('click', handleInteraction);
    document.addEventListener('keydown', (e) => {
        if (e.code === 'Space' && (gameState === 'waiting' || gameState === 'ready')) {
            e.preventDefault();
            handleInteraction();
        }
    });
}

// 4. Мини-гонка на Canvas
function initMiniRaceGame() {
    const canvas = document.getElementById('raceCanvas');
    const ctx = canvas.getContext('2d');
    const startBtn = document.getElementById('start-race-btn');
    const scoreText = document.getElementById('race-score');

    let player = { x: 120, y: 250, width: 35, height: 55 };
    let obstacles = [];
    let score = 0;
    let gameLoopId = null;
    let isRunning = false;

    function drawPlayer() {
        ctx.fillStyle = '#00d2ff'; // Неоново-голубой болид
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
        startBtn.innerText = 'Играть снова';
    }

    startBtn.addEventListener('click', () => {
        if (isRunning) return;
        isRunning = true;
        score = 0;
        player.x = 120;
        obstacles = [];
        scoreText.innerText = 'Счет: 0';
        update();
    });

    document.addEventListener('keydown', (e) => {
        if (!isRunning) return;
        if ((e.key === 'ArrowLeft' || e.key === 'a') && player.x > 15) {
            player.x -= 25;
        }
        if ((e.key === 'ArrowRight' || e.key === 'd') && player.x < canvas.width - 50) {
            player.x += 25;
        }
    });
}