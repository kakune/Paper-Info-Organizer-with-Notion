from src.paper_data.data_container import _Container
from src.paper_data.extract_webdata import _extractPaperData
from src.paper_data.default_logger import _defaultGetLogger
from typing import Callable, Any


def getJSONDictFromPropertiesDict(
    inProperties: dict,
    inKeywords: set,
    *,
    inGetLogger: Callable[[str], Any] = _defaultGetLogger
) -> dict:
    lContainer = _Container(inGetLogger=inGetLogger)
    return lContainer.setPropertiesFromDict(inProperties, inKeywords).getDict()


def getJSONDictFromURL(
    inURL: str,
    inKeywords: set,
    *,
    inGetLogger: Callable[[str], Any] = _defaultGetLogger
) -> dict:
    return getJSONDictFromPropertiesDict(
        _extractPaperData(inURL, inGetLogger=inGetLogger),
        inKeywords,
        inGetLogger=inGetLogger
    )
