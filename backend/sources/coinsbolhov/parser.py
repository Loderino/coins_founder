from bs4 import BeautifulSoup as bs4

from backend.sources.common.parser import HTMLParser

class CoinsBolhovParser(HTMLParser):
    """HTML Parser for coinsbolhov source."""
    def parse(self, html: str, mint: str) -> dict:
        soup = bs4(html, features="html.parser")
        cards = soup.find_all("div", {"class": "products__item products__item--horizontal"})
        total = len(cards)
        if total:
            prices = []
            if mint:
                total=0
            for card in cards:
                if mint:
                    if card.find("a", {"class": "products__item-info-title"}).text.endswith(mint):
                        total+=1
                        price = int(card.find("div", {"class": "products__item-info-price"}).text.split()[0])
                        prices.append(price)
                else:
                    price = int(card.find("div", {"class": "products__item-info-price"}).text.split()[0])
                    prices.append(price)
            return {
                "total_variants": total,
                "max_price": max(prices),
                "min_price": min(prices),
                "avg_price": sum(prices) // total
            }
        return {}
