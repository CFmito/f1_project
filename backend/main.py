from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random

app = FastAPI(title="F1 Interactive Blog API")

# Настройка CORS для взаимодействия с фронтендом
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Данные о ваших любимых пилотах
DRIVERS = [
    {
        "id": "1",
        "name": "Lewis Hamilton",
        "number": 44,
        "team": "Scuderia Ferrari / Mercedes",
        "bio": "Семикратный чемпион мира, рекордсмен по количеству побед и поулов в истории Формулы-1. Легенда автоспорта.",
        "podiums": 197,
        "world_titles": 7,
        "image_url": "https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?w=500&auto=format&fit=crop&q=60"
    },
    {
        "id": "2",
        "name": "Kimi Antonelli",
        "number": 12,
        "team": "Mercedes-AMG Petronas",
        "bio": "Молодой восходящий феномен итальянского автоспорта, прошедший стремительный путь через юниорские серии прямо в состав Mercedes.",
        "podiums": 0,
        "world_titles": 0,
        "image_url": "https://images.unsplash.com/photo-1541348263662-e082662d82da?w=500&auto=format&fit=crop&q=60"
    },
    {
        "id": "3",
        "name": "George Russell",
        "number": 63,
        "team": "Mercedes-AMG Petronas",
        "bio": "Победитель Гран-при, известнейший своим аналитическим подходом к гонкам, выдержкой и высокой скоростью в квалификациях.",
        "podiums": 14,
        "world_titles": 0,
        "image_url": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=500&auto=format&fit=crop&q=60"
    }
]

@app.get("/api/drivers")
def get_drivers():
    """Возвращает список любимых пилотов"""
    return DRIVERS

@app.get("/api/random-car")
def get_random_car():
    """Рандомайзер сборки болида F1"""
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

# Запуск сервера: uvicorn main:app --reload --port 8080