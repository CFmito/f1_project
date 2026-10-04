from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import random
from datetime import datetime

app = FastAPI(title="F1 Interactive Blog API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Раздача статических файлов (картинок)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Временное хранилище рекордов (Leaderboard)
LEADERBOARD = [
    {"player": "Max_V", "time_ms": 195},
    {"player": "Charles_16", "time_ms": 210},
    {"player": "Speedy", "time_ms": 235}
]

class ScoreRequest(BaseModel):
    player: str
    time_ms: int

DRIVERS = [
    {
        "id": "1",
        "name": "Lewis Hamilton",
        "number": 44,
        "team": "Scuderia Ferrari / Mercedes",
        "bio": "Семикратный чемпион мира, рекордсмен по количеству побед и поулов в истории Формулы-1. Легенда автоспорта.",
        "podiums": 207,
        "world_titles": 7,
        "image_url": "/static/lh44.jpg"  # Используем относительный путь вместо жесткой привязки к порту
    },
    {
        "id": "2",
        "name": "Kimi Antonelli",
        "number": 12,
        "team": "Mercedes-AMG Petronas",
        "bio": "Молодой восходящий феномен итальянского автоспорта, прошедший стремительный путь через юниорские серии прямо в состав Mercedes.",
        "podiums": 15,
        "world_titles": 0,
        "image_url": "/static/ka12.jpg"
    },
    {
        "id": "3",
        "name": "George Russell",
        "number": 63,
        "team": "Mercedes-AMG Petronas",
        "bio": "Победитель Гран-при, известнейший своим аналитическим подходом к гонкам, выдержкой и высокой скоростью в квалификациях.",
        "podiums": 31,
        "world_titles": 0,
        "image_url": "/static/gr63.jpg"
    }
]

@app.get("/api/drivers")
def get_drivers():
    return DRIVERS

@app.get("/api/random-car")
def get_random_car():
    chassis_list = ["Mercedes W16", "Ferrari SF-25", "McLaren MCL39", "Red Bull RB21"]
    engine_list = ["Mercedes-AMG V6", "Ferrari V6 Turbo", "Honda RBPT", "Renault E-Tech"]
    tyres_list = ["Soft (C5 - Красные)", "Medium (C3 - Жёлтые)", "Hard (C1 - Белые)", "Intermediate (Зелёные)"]
    strategy_list = ["Plan A: Undercut", "Plan B: Soft-Medium-Soft", "Hammer Time / Attack", "Box, Box for Fastest Lap"]

    return {
        "chassis": random.choice(chassis_list),
        "engine": random.choice(engine_list),
        "tyres": random.choice(tyres_list),
        "strategy": random.choice(strategy_list),
        "score": random.randint(75, 99)
    }

# Календарь предстоящих Гран-при (в формате ISO с UTC временем Z)
F1_SCHEDULE = [
    {
        "title": "Гран-при Сингапура",
        "circuit": "Marina Bay Street Circuit",
        "location": "Марина-Бэй, Сингапур",
        "race_time": "2026-10-11T12:00:00Z"
    },
    {
        "title": "Гран-при США",
        "circuit": "Circuit of the Americas",
        "location": "Остин, США",
        "race_time": "2026-10-25T20:00:00Z"
    },
    {
        "title": "Гран-при Мехико",
        "circuit": "Autódromo Hermanos Rodríguez",
        "location": "Мехико, Мексика",
        "race_time": "2026-11-01T20:00:00Z"
    },
    {
        "title": "Гран-при Сан-Паулу",
        "circuit": "Autódromo José Carlos Pace",
        "location": "Сан-Паулу, Бразилия",
        "race_time": "2026-11-08T17:00:00Z"
    },
    {
        "title": "Гран-при Лас-Вегаса",
        "circuit": "Las Vegas Strip Circuit",
        "location": "Лас-Вегас, США",
        "race_time": "2026-11-22T04:00:00Z"
    },
    {
        "title": "Гран-при Катара",
        "circuit": "Lusail International Circuit",
        "location": "Лусаил, Катар",
        "race_time": "2026-11-29T16:00:00Z"
    },
    {
        "title": "Гран-при Абу-Даби",
        "circuit": "Yas Marina Circuit",
        "location": "Абу-Даби, ОАЭ",
        "race_time": "2026-12-06T13:00:00Z"
    }
]

@app.get("/api/next-race")
def get_next_race():
    now = datetime.utcnow()
    
    for race in F1_SCHEDULE:
        race_dt = datetime.fromisoformat(race["race_time"].replace("Z", "+00:00")).replace(tzinfo=None)
        if race_dt > now:
            return race

    return {
        "title": "Сезон завершен",
        "circuit": "Ожидаем новый календарь",
        "location": "F1 2027",
        "race_time": now.isoformat()
    }

@app.get("/api/leaderboard")
def get_leaderboard():
    return sorted(LEADERBOARD, key=lambda x: x["time_ms"])[:5]

@app.post("/api/leaderboard")
def save_score(score: ScoreRequest):
    LEADERBOARD.append({"player": score.player, "time_ms": score.time_ms})
    return {"status": "success"}

# Раздача фронтенда из папки frontend
app.mount("/", StaticFiles(directory="/frontend", html=True), name="frontend")