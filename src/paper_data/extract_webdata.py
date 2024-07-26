from src.paper_data.default_logger import _defaultGetLogger
from src.paper_data.each_extract.arxiv import _ArxivExtractor
from src.paper_data.each_extract.utils import _getDOIFromURL, _getDOIFromPDFPath, _extractArxivNumber
from src.paper_data.each_extract.doi import _DOIExtractor
from typing import Callable, Any


def _getExtractorFromDOI(
    inDOI: str,
    inPDFLink: str = None,
    *,
    inGetLogger: Callable[[str], Any] = _defaultGetLogger
) -> dict:
    lLogger = inGetLogger(__name__)

    if 'arxiv' in inDOI:
        lSplittedDOI = inDOI.split('.')
        lURL = 'https://arxiv.org/abs/' + \
            lSplittedDOI[-2] + '.' + lSplittedDOI[-1]
        lLogger.debug(f'getExtractorFromDOI: Detected arXiv link: {lURL}')
        return _ArxivExtractor(
            lURL,
            inGetLogger=inGetLogger
        )
    return _DOIExtractor(
        inDOI,
        inPDFLink=inPDFLink,
        inGetLogger=inGetLogger
    )


def _getExtractorFromURL(
    inURL: str,
    *,
    inGetLogger: Callable[[str], Any] = _defaultGetLogger
):
    if (lNumber := _extractArxivNumber(inURL, inGetLogger=inGetLogger)) is not None:
        return _ArxivExtractor('https://arxiv.org/abs/' + lNumber, inGetLogger=inGetLogger)
    elif inURL.startswith('file://'):
        if (not inURL.endswith('.pdf')):
            raise ValueError('Not a PDF file')
        lDOI = _getDOIFromPDFPath(inURL[7:], inGetLogger=inGetLogger)
        return _getExtractorFromDOI(lDOI, inGetLogger=inGetLogger)
    else:
        lDOI = _getDOIFromURL(inURL, inGetLogger=inGetLogger)
        return _getExtractorFromDOI(lDOI, inPDFLink=inURL, inGetLogger=inGetLogger)


def _extractPaperData(
    inURL: str,
    *,
    inGetLogger: Callable[[str], Any] = _defaultGetLogger
) -> dict:
    lExtractor = _getExtractorFromURL(inURL, inGetLogger=inGetLogger)
    return {
        'Title': lExtractor.getTitle(),
        'Authors': lExtractor.getAuthors(),
        'Abstract': lExtractor.getAbstract(),
        'Year': lExtractor.getYear(),
        'DOI': lExtractor.getDOI(),
        'PDF URL': lExtractor.getPDFLink(),
        'Journal': lExtractor.getJournal()
    }
