from backend.service import SourceService
from backend.parser import HTMLParser
from backend.requestor import Requestor

class ServiceFactory:
    @staticmethod
    def get_services(services: str) -> list[SourceService]:
        pass
    
    @staticmethod
    def make_service(service_id: str):
        url = ...
        requestor = Requestor(url)
        parser = HTMLParser()
        service = SourceService(requestor, parser)

