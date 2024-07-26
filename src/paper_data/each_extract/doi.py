from src.paper_data.each_extract.abstract import _ExtractorAbstract
from src.paper_data.each_extract.utils import _isPDF
import requests
from typing import Callable, Any
from src.paper_data.default_logger import _defaultGetLogger


class _DOIExtractor(_ExtractorAbstract):
    def __init__(
        self,
        inDOI: str,
        inPDFLink: str = None,
        *,
        inGetLogger: Callable[[str], Any] = _defaultGetLogger
    ):
        self.__logger = inGetLogger(__name__)
        self.__logger.debug(f'DOIExtractor: inDOI={
                            inDOI}, inPDFLink={inPDFLink}')

        self.__doi = inDOI
        self.__pdflink = inPDFLink if (
            (inPDFLink is not None)
            and (_isPDF(inPDFLink, inGetLogger=inGetLogger))
        ) else None
        lResponse = requests.get(f'https://api.crossref.org/works/{inDOI}')
        if lResponse.status_code != 200:
            raise ValueError(f'Error: {lResponse.status_code}')
        self.__item = lResponse.json()['message']

    def getTitle(self) -> str:
        return self.__item['title'][0] if 'title' in self.__item and self.__item['title'] else None

    def getAuthors(self) -> list:
        return [author['given'] + ' ' + author['family'] for author in self.__item['author']] if 'author' in self.__item else None

    def getAbstract(self) -> str:
        return self.__item['abstract'] if 'abstract' in self.__item else None

    def getYear(self) -> int:
        return self.__item['published-print']['date-parts'][0][0] if 'published-print' in self.__item else self.__item['published-online']['date-parts'][0][0] if 'published-online' in self.__item else None

    def getDOI(self) -> str:
        return self.__doi

    def getPDFLink(self) -> str:
        return self.__pdflink

    def getJournal(self) -> str:
        return self.__item['container-title'][0] if 'container-title' in self.__item and self.__item['container-title'] else None
