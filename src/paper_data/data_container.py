from typing import Self, Callable, Any
import ahocorasick
from src.paper_data.default_logger import _defaultGetLogger


def _getKeywordsFromAbstract(
    inAbstract: str,
    inKeywords: set = set(),
    *,
    inGetLogger: Callable[[str], Any] = _defaultGetLogger
) -> set:
    lLogger = inGetLogger(__name__)

    if ((inAbstract is None) or (len(inKeywords) == 0)):
        lLogger.debug('getKeywordsFromAbstract: No abstract or keywords')
        return set()

    lLowerKeywords = {inWord.lower() for inWord in inKeywords}
    lDictOriginalKeywords = {inWord.lower(): inWord for inWord in inKeywords}
    lLowerAbstract = inAbstract.lower()

    lAuto = ahocorasick.Automaton()
    for idx, lKeyword in enumerate(lLowerKeywords):
        lAuto.add_word(lKeyword, (idx, lKeyword))
    lAuto.make_automaton()

    lKeywords = set()
    for _, (_, lOriginalValue) in lAuto.iter(lLowerAbstract):
        lKeywords.add(lDictOriginalKeywords[lOriginalValue])

    lLogger.debug(f'getKeywordsFromAbstract: Keywords found: {lKeywords}')
    return lKeywords


class _Container:
    def __init__(
        self,
        *,
        inGetLogger: Callable[[str], Any] = _defaultGetLogger
    ) -> None:
        self.__logger = inGetLogger(__name__)
        self.__getLogger = inGetLogger

        self.__properties = {}

    def setPropertiesFromDict(
        self,
        inProperties: dict,
        inKeywords: set = set()
    ) -> Self:
        self.__logger.debug('Container::setPropertiesFromDict() run')
        self.setTitle(inProperties['Title'])
        self.setAuthors(inProperties['Authors'])
        self.setYear(inProperties['Year'])
        self.setDOI(inProperties['DOI'])
        self.setPDF(inProperties['PDF URL'])
        self.setJournal(inProperties['Journal'])
        self.setKeywords(_getKeywordsFromAbstract(
            inProperties['Abstract'],
            inKeywords,
            inGetLogger=self.__getLogger
        ))
        return self

    def setTitle(
        self,
        inTitle: str
    ) -> Self:
        if inTitle is None:
            return self
        self.__properties['Title'] = {
            'title': [
                {
                    'text': {
                        'content': inTitle
                    }
                }
            ]
        }
        return self

    def setAuthors(
        self,
        inAuthors: list
    ) -> Self:
        if inAuthors is None:
            return self
        self.__properties['Author'] = {
            'rich_text': [
                {
                    'text': {
                        'content': ', '.join(inAuthors)
                    }
                }
            ]
        }
        return self

    def setYear(
        self,
        inYear: int
    ) -> Self:
        if inYear is None:
            return self
        self.__properties['Year'] = {
            'number': inYear
        }
        return self

    def setDOI(
        self,
        inDOI: str
    ) -> Self:
        if inDOI is None:
            return self
        self.__properties['doi'] = {
            'url': 'https://doi.org/' + inDOI
        }
        return self

    def setPDF(
        self,
        inPDFURL: str
    ) -> Self:
        if inPDFURL is None:
            return self
        self.__properties['PDF'] = {
            'files': [
                {
                    'name': inPDFURL,
                    'external': {
                        'url': inPDFURL
                    }
                }
            ]

        }
        return self

    def setJournal(
        self,
        inJournal: str
    ) -> Self:
        if inJournal is None:
            return self
        self.__properties['Journal'] = {
            'rich_text': [
                {
                    'text': {
                        'content': inJournal
                    }
                }
            ]
        }
        return self

    def setKeywords(
        self,
        inKeywords: list
    ) -> Self:
        if inKeywords is None:
            return self
        self.__properties['Keywords'] = {
            'multi_select': [
                {'name': lKey} for lKey in inKeywords
            ]
        }
        return self

    def getDict(self) -> dict:
        self.__logger.debug('Container::getDict() run')
        return {'properties': self.__properties}
