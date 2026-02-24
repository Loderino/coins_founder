from backend.sources.common.requestor import Requestor
from backend.sources.common.parser import HTMLParser

class SourceService:
    def __init__(self, requestor: Requestor, parser: HTMLParser):
        self.requestor = requestor
        self.parser = parser

    async def get_data(self, coin_info):
        result = await self.requestor.get_html(coin_info)
        price_data = self.parser.parse(result["html"], coin_info.mintmark)
        price_data["url"] = result["url"]
        return price_data