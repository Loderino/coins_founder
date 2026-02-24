from urllib.parse import urljoin

from backend.sources.common.url_maker import URLMaker
from backend.utils import transcript

class CoinsBolhovURLMaker(URLMaker):

    def __get_actual_type(self, coin_info):
        if coin_info.country in ["Россия", "СССР", "РСФСР"]:
            if coin_info.is_regular:
                return "monety-rsfsr-sssr-rossii"
            return "yubileinye-monety"
        elif coin_info.country in ["Российская империя"]:
            return "monety-rossiiskoi-imperii"
        return "inostrannye-monety"
            

    def __get_actual_country_name(self, country: str):
        countries = {

        }
        return countries.get(country, transcript(country).lower())

    def __get_actual_nominal_name(self, nominal: str, currency: str):
        identical_nominals = {
            "50 центов": "1_2 доллара",
            "25 центов": "1_4 доллара"
        }

        full_nominal = f"{nominal} {currency}"
        same_nominal = identical_nominals.get(full_nominal, None)

        nominals = {
            "2.5 доллара": "84d85b87758815f2d2faa20bac5dcc58",
            "1_4 доллара": "1f57bf3a1f758ee48fe1b009a04f2a25",

        }
        if same_nominal:
            return nominals.get(full_nominal, transcript(full_nominal).lower())+"-or-"+nominals.get(same_nominal, transcript(full_nominal).lower())    
        return nominals.get(full_nominal, transcript(full_nominal).lower())

        
    def make_url_for_coin(self, coin_info):
        type_filter = self.__get_actual_type(coin_info)
        year_filter = f"year_from-from-{coin_info.year}-to-{coin_info.year}"
        country_filter = f"country-is-{self.__get_actual_country_name(coin_info.country)}"
        nominal_filter = f"nominal-is-{self.__get_actual_nominal_name(coin_info.nominal, coin_info.currency)}"
        url = urljoin(self.base_url, f"{type_filter}/filter/{year_filter}/{country_filter}/{nominal_filter}/")
        print(url)
        return url