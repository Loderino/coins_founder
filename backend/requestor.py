from httpx import AsyncClient

class Requestor:
    def __init__(self, url):
        self.client = AsyncClient(base_url=url)

    def _make_correct_url_postfix(self, data):
        pass

    async def get_html(self, data):
        return await self.client.get(self._make_correct_url_postfix(data))

