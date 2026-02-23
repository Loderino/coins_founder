from backend.requestor import Requestor
from backend.parser import HTMLParser
class SourceService:
    def __init__(self, requestor: Requestor, parser: HTMLParser):
        self.requestor = requestor
        self.parser = parser

    async def get_data(self):
        html = await self.requestor.get_html()
        return self.parser.parse(html)