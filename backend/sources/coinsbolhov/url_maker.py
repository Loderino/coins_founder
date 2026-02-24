from urllib.parse import urljoin

from backend.api.models import CoinInfo
from backend.sources.common.url_maker import URLMaker
from backend.utils import transcript

class CoinsBolhovURLMaker(URLMaker):
    """URL maker for coinsbolhov source"""

    def __get_actual_type(self, coin_info: CoinInfo) -> str:
        """Determines, based on the coin information, in which section of the site you need to look for it.

        Args:
            coin_info (CoinInfo): Information about coin.

        Returns:
            str: url-part (section of the site).
        """
        if coin_info.country in ["Россия", "СССР", "РСФСР"]:
            if coin_info.is_regular:
                return "monety-rsfsr-sssr-rossii"
            return "yubileinye-monety"
        elif coin_info.country in ["Российская империя"]:
            return "monety-rossiiskoi-imperii"
        return "inostrannye-monety"
            

    def __get_actual_country_name(self, country: str) -> str:
        """
        Returns a country name as it is written on the site, based on the coin information.

        Args:
            country (sDetermines, based on the coin information, in which section of the site you need to look for ittr): Country name from the coin information.

        Returns:
            str: URL-part (country name as it is written on the site).
        """
        countries = {

        }
        return countries.get(country, transcript(country).lower())

    def __get_actual_nominal_name(self, nominal: str, currency: str) -> str:
        """
        Returns a nominal name as it is written on the site, based on the coin information.

        Args:
            nominal (str): Nominal from the coin information.
            currency (str): Currency from the coin information.

        Returns:
            str: URL-part (nominal name as it is written on the site).
        """
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

        
    def make_url_for_coin(self, coin_info) -> str:
        """
        Makes a correct URL to source web-page for parse it html code.
        
        Args:
            coin_info (CoinInfo): Information about coin.
        
        Returns:
            str: URL to right coin sales.
        """
        type_filter = self.__get_actual_type(coin_info)
        year_filter = f"year_from-from-{coin_info.year}-to-{coin_info.year}"
        country_filter = f"country-is-{self.__get_actual_country_name(coin_info.country)}"
        nominal_filter = f"nominal-is-{self.__get_actual_nominal_name(coin_info.nominal, coin_info.currency)}"
        url = urljoin(self.base_url, f"{type_filter}/filter/{year_filter}/{country_filter}/{nominal_filter}/")
        print(url)
        return url