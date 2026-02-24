from backend.sources.common.service import SourceService
from backend.sources.common.requestor import Requestor
from backend.sources.common import get_url_maker, get_parser

class ServiceFactory:
    @staticmethod
    def get_services(sources: str) -> list[SourceService]:
        return [ServiceFactory._make_service(source) for source in sources]
    
    @staticmethod
    def _make_service(source_id: str) -> SourceService:
        url_maker = get_url_maker(source_id)
        requestor = Requestor(url_maker)
        parser = get_parser(source_id)
        return SourceService(requestor, parser)

