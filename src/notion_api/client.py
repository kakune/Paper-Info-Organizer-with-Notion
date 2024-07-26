from typing import Dict
from src.notion_api.query import gNotionURL, _makeHeader
from src.notion_api.default_logger import _defaultGetLogger
import requests
from typing import Callable, Any


class Client:
    def __init__(
        self,
        inNotionAPIKey: str,
        inDatabaseID: str,
        *,
        inGetLogger: Callable[[str], Any] = _defaultGetLogger
    ) -> None:
        self.__header = _makeHeader(inNotionAPIKey=inNotionAPIKey)
        self.__databaseID = inDatabaseID
        self.__logger = inGetLogger(__name__)

    def addData(
        self,
        inData: Dict
    ):
        lData = inData.copy()
        lData.update(
            {'parent': {'database_id': self.__databaseID}}
        )
        lResponse = requests.post(
            gNotionURL,
            headers=self.__header,
            json=lData
        )
        if lResponse.status_code == 200:
            self.__logger.info("Succeeded in adding data.")
        else:
            self.__logger.warning(f"Error: {lResponse.status_code}")
            self.__logger.warning(lResponse.text)

    def getData(self):
        lResponse = requests.post(
            f"https://api.notion.com/v1/databases/{self.__databaseID}/query",
            headers=self.__header
        )
        if lResponse.status_code == 200:
            self.__logger.info("Succeeded in getting data.")
            return lResponse.json()
        else:
            self.__logger.warning(f"Error: {lResponse.status_code}")
            self.__logger.warning(lResponse.text)
            return None

    def getTitleSet(
        self,
        inColumnName: str
    ):
        lData = self.getData()
        if lData is None:
            return None

        lResult = set()
        for lPart in lData['results']:
            if (len(lPart['properties'][inColumnName]['title']) == 0):
                continue
            lResult.add(
                lPart['properties'][inColumnName]['title'][0]['text']['content']
            )

        return lResult

    def getDOISet(self):
        lData = self.getData()
        if lData is None:
            return None

        lResult = set()
        for lPart in lData['results']:
            lResult.add(
                lPart['properties']['doi']['url']
            )

        return lResult
