import requests
from src.paper_data.default_logger import _defaultGetLogger
from logging import getLogger
from bs4 import BeautifulSoup
import pdf2doi
import logging
import tempfile
import os
import timeout_decorator
import re
from typing import Callable, Any


def _extractArxivNumber(
    inStr: str,
    *,
    inGetLogger: Callable[[str], Any] = _defaultGetLogger
) -> str:
    lLogger = inGetLogger(__name__)

    lArxivPattern = r'\b\d{4}\.\d{4,5}\b'
    lMatches = re.findall(lArxivPattern, inStr)
    if len(lMatches) == 0:
        lLogger.debug(f'extractArxivNumber: No arXiv number found in {inStr}')
        return None
    lLogger.debug(f'extractArxivNumber: Found arXiv number {
        lMatches[-1]} in {inStr}')
    return str(lMatches[-1])


def _isPDF(
    inURL: str,
    *,
    inGetLogger: Callable[[str], Any] = _defaultGetLogger
) -> bool:
    lLogger = inGetLogger(__name__)
    try:
        lResponse = requests.head(inURL, allow_redirects=True)
        lContentType = lResponse.headers.get('Content-Type', '').lower()
        lLogger.debug(f'isPDF: Content-Type: {lContentType}')
        return 'pdf' in lContentType
    except Exception as _:
        lLogger.warning(f'isPDF: Error while checking {inURL}')
        return False


@timeout_decorator.timeout(10, use_signals=False)
def _pdf2doiWithTimeout(inPDFPath: str):
    return pdf2doi.pdf2doi(inPDFPath)


def _getDOIFromPDFPath(
    inPDFPath: str,
    *,
    inGetLogger: Callable[[str], Any] = _defaultGetLogger
) -> str:
    if os.path.getsize(inPDFPath) > 5 * 1024 * 1024:
        raise ValueError(f'File size exceeds 5MB: {inPDFPath}')

    try:
        pdf2doi.logger.setLevel(logging.WARNING)
        getLogger('pdfminer').setLevel(logging.WARNING)
        lDOI = _pdf2doiWithTimeout(inPDFPath)
    except timeout_decorator.timeout_decorator.TimeoutError:
        raise ValueError(
            f'getDOIFromPDFPath: Timeout of pdf2doi in {inPDFPath}')
    except Exception as e:
        raise ValueError(f'getDOIFromPDFPath: {e} with pdf2doi in {inPDFPath}')

    if lDOI is None:
        raise ValueError(f'getDOIFromPDFPath: DOI not found in {inPDFPath}')

    return lDOI['identifier']


def _getDOIFromPDFURL(
    inPDFURL: str,
    *,
    inGetLogger: Callable[[str], Any] = _defaultGetLogger
) -> str:
    lLogger = inGetLogger(__name__)
    lResponse = requests.get(inPDFURL)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as lTempPDF:
        lLogger.debug(f'getDOIFromPDFURL: Writing PDF to {lTempPDF.name}')
        lTempPDF.write(lResponse.content)
        lPathTempPDF = lTempPDF.name

    try:
        return _getDOIFromPDFPath(lPathTempPDF, inGetLogger=inGetLogger)
    finally:
        lLogger.debug(f'getDOIFromPDFURL: Removing {lPathTempPDF}')
        os.remove(lPathTempPDF)


def _getDOIFromWebpage(
    inURL: str,
    *,
    inGetLogger: Callable[[str], Any] = _defaultGetLogger
) -> str:
    lLogger = inGetLogger(__name__)

    lResponse = requests.get(inURL)
    lSoup = BeautifulSoup(lResponse.content, 'html.parser')

    # Check all anchor tags
    for lLink in lSoup.find_all('a', href=True):
        lHRef = lLink['href']
        if 'doi.org' in lHRef:
            lDOI = lHRef.split('doi.org/')[-1]
            lLogger.debug(f'getDOIFromWebpage: Found DOI: {lDOI}')
            return lDOI

    # If DOI not found in anchor tags, check meta tags
    for lMeta in lSoup.find_all('meta'):
        if lMeta.get('name', '').lower() == 'citation_doi':
            lDOI = lMeta.get('content', '').strip()
            lLogger.debug(f'getDOIFromWebpage: Found DOI in meta tag: {lDOI}')
            return lDOI

    # If DOI still not found, check spans and other elements containing DOI
    for lTag in lSoup.find_all():
        if lTag.string and '10.' in lTag.string:
            lCandidateDOI = lTag.string.strip()
            if lCandidateDOI.startswith('10.'):
                lLogger.debug(
                    f'getDOIFromWebpage: Found DOI in tag: {lCandidateDOI}')
                return lCandidateDOI

    raise ValueError('getDOIFromWebpage: DOI not found')


def _getDOIFromURL(
    inURL: str,
    *,
    inGetLogger: Callable[[str], Any] = _defaultGetLogger
) -> str:
    if _isPDF(inURL, inGetLogger=inGetLogger):
        return _getDOIFromPDFURL(inURL, inGetLogger=inGetLogger)
    return _getDOIFromWebpage(inURL, inGetLogger=inGetLogger)
