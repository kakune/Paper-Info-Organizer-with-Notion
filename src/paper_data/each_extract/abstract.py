from abc import ABCMeta, abstractmethod
import requests
from bs4 import BeautifulSoup


class _ExtractorAbstract(metaclass=ABCMeta):
    def getPageText(self, inURL: str):
        lResponse = requests.get(inURL)
        lResponse.raise_for_status()
        return BeautifulSoup(lResponse.text, 'html.parser')

    def getAllDataDict(self) -> dict:
        return {
            'Title': self.getTitle(),
            'Authors': self.getAuthors(),
            'Abstract': self.getAbstract(),
            'Year': self.getYear(),
            'DOI': self.getDOI(),
            'PDF URL': self.getPDFLink()
        }

    @abstractmethod
    def __init__(self, inURL: str):
        raise NotImplementedError

    @abstractmethod
    def getTitle(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def getAuthors(self) -> list:
        raise NotImplementedError

    @abstractmethod
    def getAbstract(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def getYear(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def getDOI(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def getPDFLink(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def getJournal(self) -> str:
        raise NotImplementedError
