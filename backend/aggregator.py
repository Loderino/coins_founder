import asyncio

from backend.api.models import CoinInfo
from backend.service_factory import ServiceFactory


class Aggregator:
    """Class for handling API queries. Begins founding operations for many sources and aggregates it`s results."""
    async def find_coin_sales(self, coin_info: CoinInfo) -> list[dict]:
        """
        Asyncronously finds all available sales for given coin in specified sources.

        Args:
            coin_info (CoinInfo): Information about coin.

        Returns:
            list[dict]: List of dictionaries, where each dictionary contains information about sales from one source.
        """
        services = ServiceFactory.get_services(coin_info.sources)
        tasks = [service.get_data(coin_info) for service in services]
        return await asyncio.gather(*tasks)
        

