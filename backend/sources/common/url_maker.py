from backend.api.models import CoinInfo

class URLMaker:
    """Parent class for Url makers, specified for each source."""
    def __init__(self, base_url: str):
        self.base_url = base_url

    def make_url_for_coin(self, coin_info: CoinInfo) -> str:
        """Makes a correct URL to source web-page for parse it html code.
        
        Args:
            coin_info (CoinInfo): Information about coin.
        
        Returns:
            str: URL to right coin sales. 
        """