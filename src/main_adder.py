from logging import getLogger
from src.notion_api import Client
from src.paper_data import getJSONDictFromURL
from typing import Union, Callable, Any


def addOneInfo(
    inURLorPath: str,
    inClientDatabase: Client,
    inKeywords: set,
    *,
    inGetLogger: Callable[[str], Any] = getLogger
):
    lLogger = inGetLogger(__name__)

    # Get data
    lDataJSON = getJSONDictFromURL(
        inURLorPath,
        inKeywords,
        inGetLogger=inGetLogger
    )

    # Check if DOI is already in the database
    if lDataJSON['properties']['doi']['url'] in inClientDatabase.getDOISet():
        lLogger.info(f'Data with DOI {
            lDataJSON['properties']['doi']['url']} is already in database')
        return

    # Add data
    inClientDatabase.addData(lDataJSON)
    lLogger.info(f'Added data with DOI {
        lDataJSON['properties']['doi']['url']}')


def infoAdder(
    inURLorPath: Union[str, list[str]],
    inAPIKey: str,
    inDatabaseID: str,
    inKeywordsID: str = None,
    *,
    inGetLogger: Callable[[str], Any] = getLogger
):
    lLogger = inGetLogger(__name__)

    # Get keywords
    lKeywords = set()
    if (inKeywordsID is not None):
        lClientKeywords = Client(
            inAPIKey, inKeywordsID, inGetLogger=inGetLogger)
        lKeywords = lClientKeywords.getTitleSet('Word')
    lClientDatabase = Client(inAPIKey, inDatabaseID, inGetLogger=inGetLogger)

    # Add info
    if isinstance(inURLorPath, str):
        inURLorPath = [inURLorPath,]
    for lEachURLorPath in inURLorPath:
        lLogger.info('Adding ' + lEachURLorPath + '...')
        try:
            addOneInfo(
                lEachURLorPath,
                lClientDatabase,
                lKeywords,
                inGetLogger=inGetLogger
            )
        except Exception as e:
            lLogger.error(f'{e}')
