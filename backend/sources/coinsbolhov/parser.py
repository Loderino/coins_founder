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
                    title = card.find("a", {"class": "products__item-info-title"}).text
                    if " "+mint+" " in title or title.endswith(" "+mint):
                        total+=1
                        price = int("".join(card.findAll("div", {"class": "products__item-info-price"})[-1].text.split()[:-1]))
                        prices.append(price)
                else:
                    price = int("".join(card.findAll("div", {"class": "products__item-info-price"})[-1].text.split()[:-1]))
                    prices.append(price)
        if total:
            return {
                "total_variants": total,
                "max_price": max(prices),
                "min_price": min(prices),
                "avg_price": sum(prices) // total
            }
        return {}
