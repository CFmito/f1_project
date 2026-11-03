import os
import random
from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI(title="F1 Interactive Blog API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
FRONTEND_DIR = os.path.join(os.path.dirname(BASE_DIR), "frontend")

if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

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
        "image_url": "/static/lh44.jpg"
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

TEAM_HISTORY = [
    {
        "year": "1954",
        "title": "Дебют в Формуле-1",
        "description": "Легендарные 'Серебряные стрелы' (W196) дебютируют в Ф1 и с ходу завоевывают дубль на Гран-при Франции с Хуаном Мануэлем Фанхио."
    },
    {
        "year": "2010",
        "title": "Возвращение заводской команды",
        "description": "Mercedes возвращается в Ф1 как полноценная заводская команда, выкупив Brawn GP. В состав входят Михаэль Шумахер и Нико Росберг."
    },
    {
        "year": "2014",
        "title": "Начало гибридной эры",
        "description": "С переходом на турбогибридные двигатели V6 команда начинает беспрецедентное доминирование в чемпионате."
    },
    {
        "year": "2014–2021",
        "title": "8 Кубков конструкторов подряд",
        "description": "Команда устанавливает абсолютный рекорд Формулы-1, завоевав 8 последовательных Кубков конструкторов."
    },
    {
        "year": "2025–2026",
        "title": "Новая эра и смена поколений",
        "description": "Формирование нового состава с молодыми талантами и подготовка к новому техническому регламенту 2026 года."
    }
]

# База данных видео и эдитов с реальными видео о F1
# База данных видео и эдитов с вашими YouTube Shorts
VIDEOS_DATA = [
    {
        "id": "v1",
        "category": "history",
        "title": "Обзор команды Mercedes F1",
        "desc": "Официальное видео про историю и жизнь команды Mercedes AMG Petronas.",
        "thumbnail": "https://img.youtube.com/vi/o5v8WOh5qPs/hqdefault.jpg",
        "type": "youtube",
        "src": "https://www.youtube.com/embed/o5v8WOh5qPs"
    },
    {
        "id": "v2",
        "category": "edits",
        "title": "Эдит про Джорджа Рассела",
        "desc": "Лучшие моменты, скорость и стиль пилота под номером 63.",
        "thumbnail": "https://img.youtube.com/vi/iIUiChvhAjU/hqdefault.jpg",
        "type": "youtube",
        "src": "https://www.youtube.com/embed/iIUiChvhAjU"
    },
    {
        "id": "v3",
        "category": "edits",
        "title": "Эдит про Кими Антонелли",
        "desc": "Молодой восходящий талант и скорость итальянского пилота.",
        "thumbnail": "https://img.youtube.com/vi/LDy94kVRLzE/hqdefault.jpg",
        "type": "youtube",
        "src": "https://www.youtube.com/embed/LDy94kVRLzE"
    },
    {
        "id": "v4",
        "category": "edits",
        "title": "Эдит про Льюиса Хэмилтона",
        "desc": "Легендарные моменты семикратного чемпиона мира в Mercedes.",
        "thumbnail": "https://img.youtube.com/vi/MtTVtaA9W0I/hqdefault.jpg",
        "type": "youtube",
        "src": "https://www.youtube.com/embed/MtTVtaA9W0I"
    }
]
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

# --- API ENDPOINTS ---

@app.get("/api/drivers")
def get_drivers():
    return DRIVERS

@app.get("/api/team-history")
def get_team_history():
    return TEAM_HISTORY

@app.get("/api/videos")
def get_videos():
    return VIDEOS_DATA

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

@app.get("/api/next-race")
def get_next_race():
    now = datetime.now(timezone.utc)
    for race in F1_SCHEDULE:
        race_dt = datetime.fromisoformat(race["race_time"].replace("Z", "+00:00"))
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

# Мнтирование фронтенда ДОЛЖНО быть строкой НИЖЕ ВСЕХ @app.get роутов
if os.path.exists(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")