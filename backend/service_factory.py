from backend.sources.common.service import SourceService
from backend.sources.common.requestor import Requestor
from backend.sources.common import get_url_maker, get_parser

class ServiceFactory:
    """Class containing functions for creating source service objects.
    Every service is specified for each source.
    """
    @staticmethod
    def get_services(sources: list[str]) -> list[SourceService]:
        """Creates a services for each source from sources list.

        Args:
            sources (list[str]): list of sources ids.

        Returns:
            list[SourceService]: list of SourceService objects, specified for every sources from sources list.
        """
        return [ServiceFactory._make_service(source) for source in sources]
    
    @staticmethod
    def _make_service(source_id: str) -> SourceService | None:
        """Creates a SourceService object for a given source id.

        Args:
            source_id (str): id of the source.

        Returns:
            SourceService | None: SourceService object or None if url maker or parser for source is not found.

        Raises:
            ValueError: if url maker or parser for source is not found.
        """
        if (url_maker := get_url_maker(source_id)) is None:
            raise ValueError(f"URL maker for source {source_id} is not found")
        requestor = Requestor(url_maker)
        if (parser := get_parser(source_id)) is None:
            raise ValueError(f"HTML parser for source {source_id} is not found")
        return SourceService(requestor, parser)

