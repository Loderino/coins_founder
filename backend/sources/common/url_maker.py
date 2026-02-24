from backend.api.models import CoinInfo

class URLMaker:

    def __init__(self, base_url: str):
        self.base_url = base_url

    def make_url_for_coin(self, coin_info: CoinInfo):
        pass