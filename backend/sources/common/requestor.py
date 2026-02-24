from httpx import AsyncClient

from backend.api.models import CoinInfo
from backend.sources.common.url_maker import URLMaker

class Requestor:
    """HTTP requestor for getting html code from web-page."""
    def __init__(self, url_maker: URLMaker):
        self.client = AsyncClient()
        self.url_maker = url_maker

    async def get_html(self, data:CoinInfo) -> dict:
        """Asyncronously sends a GET request to the URL constructed by the URL maker for the given coin info.

            Args:
                data (CoinInfo): Information about the coin to search for.

            Raises:
                Exception: If the request fails or the response status code is not 200.

            Returns:
                dict: Dictionary containing the URL and the HTML code of the web-page.
        """
        try:
            url = self.url_maker.make_url_for_coin(data)
            response = await self.client.get(url)
            response.raise_for_status()
            return {"url" : url, "html" : response.text}
        except Exception as e:
            print(e)
            raise e from e
