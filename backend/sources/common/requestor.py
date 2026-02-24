from httpx import AsyncClient

from backend.sources.common.url_maker import URLMaker

class Requestor:
    def __init__(self, url_maker: URLMaker):
        self.client = AsyncClient()
        self.url_maker = url_maker

    async def get_html(self, data) -> dict:
        try:
            url = self.url_maker.make_url_for_coin(data)
            response = await self.client.get(url)
            response.raise_for_status()
            return {"url" : url, "html" : response.text}
        except Exception as e:
            print(e)
            raise e from e
