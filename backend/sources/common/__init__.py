from backend.sources.common.url_maker import URLMaker
from backend.sources.common.parser import HTMLParser
from backend.sources.coinsbolhov.url_maker import CoinsBolhovURLMaker
from backend.sources.coinsbolhov.parser import CoinsBolhovParser

def get_url_maker(source_id: str) -> URLMaker:
    """
    Returns an instance of URLMaker for a given source id.

    Args:
        source_id (str): id of the source.

    Returns:
        URLMaker: an instance of URLMaker for the given source id.
    """
    match(source_id):
        case "coinsbolhov":
            return CoinsBolhovURLMaker("https://coinsbolhov.ru/catalog/monety/")
        
def get_parser(source_id: str) -> HTMLParser:
    """
    Returns an instance of HTMLParser for a given source id.

    Args:
        source_id (str): id of the source.

    Returns:
        HTMLParser: an instance of HTMLParser for the given source id.
    """
    match(source_id):
        case "coinsbolhov":
            return CoinsBolhovParser()