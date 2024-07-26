import re
from src.paper_data.default_logger import _defaultGetLogger
from src.paper_data.each_extract.abstract import _ExtractorAbstract
from src.paper_data.each_extract.utils import _getDOIFromURL
from typing import Callable, Any


class _ArxivExtractor(_ExtractorAbstract):
    def __init__(
        self,
        inURL: str,
        *,
        inGetLogger: Callable[[str], Any] = _defaultGetLogger
    ):
        self.__getLogger = inGetLogger
        self.__logger = inGetLogger(__name__)
        self.__logger.debug(f'ArxivExtractor: inURL={inURL}')

        self.__url = inURL.replace('/pdf/', '/abs/')
        self.__pageText = self.getPageText(self.__url)

    def getTitle(self) -> str:
        return self.__pageText.find('h1', {'class': 'title'}).text.strip().replace('Title:', '')

    def getAuthors(self) -> list:
        lAuthors = []
        lAuthorsTag = self.__pageText.find_all('div', {'class': 'authors'})
        for tag in lAuthorsTag:
            for a in tag.find_all('a'):
                lAuthors.append(a.text.strip())
        return lAuthors

    def getAbstract(self) -> str:
        lAbstract = None
        lAbstractTag = self.__pageText.find(
            'blockquote', {'class': 'abstract'})
        if lAbstractTag:
            lAbstract = lAbstractTag.text.strip().replace('Abstract: ', '')
        return lAbstract

    def getYear(self) -> int:
        lDateTag = self.__pageText.find_all('meta', {'name': 'citation_date'})
        if not lDateTag:
            return None
        return int(lDateTag[0].get('content').split('/')[0])

    def getDOI(self) -> str:
        return _getDOIFromURL(self.getPDFLink(), inGetLogger=self.__getLogger)

    def getPDFLink(self) -> str:
        lPDFLink = None
        lPDFLinkTag = self.__pageText.find('a', {'href': re.compile(r'/pdf/')})
        if lPDFLinkTag:
            lPDFLink = 'https://arxiv.org' + lPDFLinkTag['href']
        return lPDFLink

    def getJournal(self) -> str:
        return 'arXiv'
