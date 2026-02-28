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

        normalize_nominals = {
            "½ доллара": "1_2 доллара",
            "¼ доллара": "1_4 доллара",
            "1 дайм": "10 центов",
            "2½ доллара": "2.5 доллара",
            "½ копейки": "1 деньга",
            "1 денежка": "1 деньга",
            "¼ копейки": "1 полушка",
            "1 гривенник": "10 копеек"
        }
        identical_nominals = {
            "50 центов": ["1_2 доллара"],
            "1_2 доллара": ["50 центов"],
            "1_4 доллара": ["25 центов"],
            "25 центов": ["1_4 доллара"],
            "1 деньга": ["деньга_v1", "деньга_v2", "деньга_v3", "деньга_v4"],
            "1 полушка": ["полушка_v1", "полушка_v2"],
            "1 полуполтинник": ["25 копеек"],
            "2 копейки": ["2 копейки1"],
            "1 червонец": ["10 рублей"],
        }

        full_nominal = normalize_nominals.get(f"{nominal} {currency}", f"{nominal} {currency}")
        same_nominals = identical_nominals.get(full_nominal, None)

        nominals = {
            "2.5 доллара": "84d85b87758815f2d2faa20bac5dcc58",
            "1_4 доллара": "1f57bf3a1f758ee48fe1b009a04f2a25",
            "деньга_v1": "0a47df593597a769a086f0b43f9b99a8",
            "деньга_v2": "83f8a47d24a32ad544fad5406b292cdb",
            "деньга_v3": "6b4e63412f488b720c69810d1525947d",
            "деньга_v4": "73af2e93defebf7e332d3a66aa1823c8",
            "полушка_v1": "d98dc793e794e8d21faad23690cb46a2",
            "полушка_v2": "ddaadf7115358e0a24363c9fb97783f4",
            "1 полуполтинник": "a453fa90d1f3f90952706272f5020a93",
            "1 полтина": "f871a320cf0a75362b78966a648b8617",
            "1 полтинник": "b426b8844e60796450287e12546d5176",
            "¼ копейки": "d98dc793e794e8d21faad23690cb46a2",
            "1 червонец": "64cadb796a0ac9236ffc749332ec39f6",
            "2 евроцента": "444138c570576ab767fc7a7c91282051",
            "5 евроцентов": "01f47ed18120ec1c91be860fe0cea7f7",
            "10 евроцентов": "8fb22893b43ef0a0fe4c483a8ed8094f",
            "20 евроцентов": "7c4b57f48663eeeb6c64470140b78f14"
        }
        if same_nominals:
            same_nominals.insert(0, full_nominal)
            return "-or-".join([nominals.get(nominal, transcript(nominal).lower()) for nominal in same_nominals])    
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