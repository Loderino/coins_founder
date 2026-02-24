import asyncio

from backend.api.models import CoinInfo
from backend.service_factory import ServiceFactory


class Aggregator:
    async def find_coin_sales(self, coin_info: CoinInfo):
        services = ServiceFactory.get_services(coin_info.sources)
        tasks = [service.get_data(coin_info) for service in services]
        return await asyncio.gather(*tasks)
        

