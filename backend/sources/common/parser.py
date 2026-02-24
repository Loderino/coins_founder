class HTMLParser:
    """Parent class for parsers, specified for each source."""
    def parse(self, html: str, mint: str) -> dict:
        """
        Parses the given HTML and extracts information about sales from source.

        Args:
            html (str): HTML code of the source web-page.
            mint (str): Mintmark of the coin.

        Returns:
            dict: Dictionary, containing information about sales from source.
        """