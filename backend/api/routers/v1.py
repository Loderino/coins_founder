from fastapi import APIRouter

from backend.aggregator import Aggregator
from backend.api.models import CoinInfo

v1_router = APIRouter(prefix="/api/v1")
agg = Aggregator()

@v1_router.post("/sales")
async def check_for_sales(coin_info: CoinInfo):
    print(coin_info)
    return await agg.find_coin_sales(coin_info)
    # return {"message": "Hello World"}

@v1_router.get("/sources")
async def get_sources():
    return {
        "sources": [
            {"id": "coinsbolhov", "link": "https://coinsbolhov.ru/", "icon": "https://coinsbolhov.ru/favicons/favicon-32x32.png", "badge": "API v1"},
        ]
    }