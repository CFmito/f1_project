from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import random

app = FastAPI(title="F1 Interactive Blog API")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение папки static для отдачи изображений
app.mount("/static", StaticFiles(directory="static"), name="static")

# Список пилотов
DRIVERS = [
    {
        "id": "1",
        "name": "Lewis Hamilton",
        "number": 44,
        "team": "Scuderia Ferrari / Mercedes",
        "bio": "Семикратный чемпион мира, рекордсмен по количеству побед и поулов в истории Формулы-1. Легенда автоспорта.",
        "podiums": 197,
        "world_titles": 7,
        "image_url": "http://localhost:8080/static/lh44.jpg"
    },
    {
        "id": "2",
        "name": "Kimi Antonelli",
        "number": 12,
        "team": "Mercedes-AMG Petronas",
        "bio": "Молодой восходящий феномен итальянского автоспорта, прошедший стремительный путь через юниорские серии прямо в состав Mercedes.",
        "podiums": 0,
        "world_titles": 0,
        "image_url": "http://localhost:8080/static/ka12.jpg"
    },
    {
        "id": "3",
        "name": "George Russell",
        "number": 63,
        "team": "Mercedes-AMG Petronas",
        "bio": "Победитель Гран-при, известнейший своим аналитическим подходом к гонкам, выдержкой и высокой скоростью в квалификациях.",
        "podiums": 14,
        "world_titles": 0,
        "image_url": "http://localhost:8080/static/gr63.jpg"
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