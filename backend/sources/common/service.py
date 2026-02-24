from backend.api.models import CoinInfo
from backend.sources.common.requestor import Requestor
from backend.sources.common.parser import HTMLParser

class SourceService:
    """Class that encapsulates the logic for obtaining sales information from a specific source."""
    def __init__(self, requestor: Requestor, parser: HTMLParser):
        self.requestor = requestor
        self.parser = parser

    async def get_data(self, coin_info: CoinInfo) -> dict:
        """
        Asyncronously finds all available sales for given coin in specified source.

        Args:
            coin_info (CoinInfo): Information about coin.

        Returns:
            dict: Dictionary, containing information about sales from source.
        """
        result = await self.requestor.get_html(coin_info)
        price_data = self.parser.parse(result["html"], coin_info.mintmark)
        price_data["url"] = result["url"]
        return price_data