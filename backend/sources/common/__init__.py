from backend.sources.coinsbolhov.url_maker import CoinsBolhovURLMaker
from backend.sources.coinsbolhov.parser import CoinsBolhovParser

def get_url_maker(source_id: str) -> str:
    match(source_id):
        case "coinsbolhov":
            return CoinsBolhovURLMaker("https://coinsbolhov.ru/catalog/monety/")
        
def get_parser(source_id: str) -> str:
    match(source_id):
        case "coinsbolhov":
            return CoinsBolhovParser()