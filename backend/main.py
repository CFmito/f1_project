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
    {"player": "Speedy", "time_ms": 235},
    {"player": "Lando_4", "time_ms": 250},
    {"player": "Oscar_81", "time_ms": 270}
]

class ScoreRequest(BaseModel):
    player: str
    time_ms: int

class ChatRequest(BaseModel):
    message: str

DRIVERS = [
    {
        "id": "1",
        "name": "Lewis Hamilton",
        "number": 44,
        "team": "Scuderia Ferrari / Mercedes",
        "bio": "Семикратный чемпион мира, легенда автоспорта, рекордсмен по победам и поулам.",
        "podiums": 207,
        "world_titles": 7,
        "wins": 105,
        "poles": 104,
        "image_url": "/static/lh44.jpg"
    },
    {
        "id": "2",
        "name": "Kimi Antonelli",
        "number": 12,
        "team": "Mercedes-AMG Petronas",
        "bio": "Молодой восходящий феномен итальянского автоспорта, стремительно ворвавшийся в основной состав Mercedes.",
        "podiums": 2,
        "world_titles": 0,
        "wins": 0,
        "poles": 1,
        "image_url": "/static/ka12.jpg"
    },
    {
        "id": "3",
        "name": "George Russell",
        "number": 63,
        "team": "Mercedes-AMG Petronas",
        "bio": "Победитель Гран-при, мастер квалификаций и лидер команды с аналитическим подходом к гонкам.",
        "podiums": 16,
        "world_titles": 0,
        "wins": 3,
        "poles": 4,
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

VIDEOS_DATA = [
    {
        "id": "v1",
        "category": "history",
        "title": "Обзор команды Mercedes F1",
        "desc": "Официальное видео про историю и жизнь команды Mercedes AMG Petronas.",
        "thumbnail": "https://img.youtube.com/vi/RhqB-wLfVwQ/hqdefault.jpg",
        "type": "youtube",
        "src": "https://www.youtube.com/embed/RhqB-wLfVwQ"
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
    chassis_list = ["Mercedes W17", "Ferrari SF-26", "McLaren MCL40", "Red Bull RB22"]
    engine_list = ["Mercedes-AMG V6 Turbo", "Ferrari V6 Turbo", "Honda RBPT", "Ford Powertrains"]
    tyres_list = ["Soft (C5 - Красные)", "Medium (C3 - Жёлтые)", "Hard (C1 - Белые)", "Intermediate (Зелёные)"]
    strategy_list = ["Plan A: Undercut", "Plan B: Soft-Medium-Soft", "Hammer Time / Attack", "Box, Box for Fastest Lap"]

    return {
        "chassis": random.choice(chassis_list),
        "engine": random.choice(engine_list),
        "tyres": random.choice(tyres_list),
        "strategy": random.choice(strategy_list),
        "score": random.randint(80, 99)
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
    # Строго топ-5
    return sorted(LEADERBOARD, key=lambda x: x["time_ms"])[:5]

@app.post("/api/leaderboard")
def save_score(score: ScoreRequest):
    global LEADERBOARD
    LEADERBOARD.append({"player": score.player, "time_ms": score.time_ms})
    # Сортируем и оставляем ровно топ-5
    LEADERBOARD = sorted(LEADERBOARD, key=lambda x: x["time_ms"])[:5]
    return {"status": "success", "leaderboard": LEADERBOARD}

@app.post("/api/ai-chat")
def ai_chat(req: ChatRequest):
    msg = req.message.lower()
    
    if "зачем" in msg or "сайт" in msg or "цель" in msg:
        reply = "Этот сайт — фан-хаб, созданный для любителей Формулы-1 и команды Mercedes. Здесь вы можете следить за расписанием гран-при, изучать историю команды, смотреть эксклюзивные эдиты, собирать конфигурации болидов и соревноваться в мини-играх!"
    elif "mercedes" in msg or "команд" in msg or "петронас" in msg:
        reply = "Mercedes-AMG Petronas F1 Team — легендарная заводская команда, удерживающая рекорд по количеству Кубков конструкторов подряд (8 титулов с 2014 по 2021 год) и славящаяся своими 'Серебряными стрелами'."
    elif "хэмилтон" in msg or "hamilton" in msg:
        reply = "Льюис Хэмилтон (#44) — семикратный чемпион мира, легенда автоспорта, обладатель рекордов по победам (105) и поулам (104)."
    elif "рассел" in msg or "russell" in msg:
        reply = "Джордж Рассел (#63) — британский топ-пилот Mercedes, отличающийся невероятной стабильностью, мастерством в квалификациях и победным темпом."
    elif "антонелли" in msg or "kimi" in msg or "кими" in msg:
        reply = "Кими Антонелли (#12) — молодой итальянский суперталант и восходящая звезда команды Mercedes в новом поколении Формулы-1."
    else:
        reply = "Я виртуальный ИИ-ассистент этого фан-хаба. Спросите меня о назначении сайта, истории Mercedes F1 или о трех любимых пилотах: Льюисе Хэмилтоне, Джордже Расселе и Кими Антонелли!"
        
    return {"reply": reply}

# Монтирование фронтенда в самом конце
if os.path.exists(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")