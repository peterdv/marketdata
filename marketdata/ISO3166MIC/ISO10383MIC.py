# -*- coding: utf-8; mode: Python; -*-

import os
import datetime
import csv
import pandas as pd
import inspect

# docstring guide https://numpydoc.readthedocs.io/en/latest/format.html

P_NAME = 'ISO10383MIC'
P_TMP_DIR = '/tmp/' + P_NAME
P_CACHE_DIR = P_TMP_DIR + '/cache'
P_PERSISTENCE_DIR = P_TMP_DIR + '/persistence'

def typename(x): return type(x).__name__
#def classname(x): return x.__class__.__name__
def classname(x): return x.__class__.__qualname__

#
# Set up logging
#
import logging, logging.handlers

LOGFORMAT = '%(asctime)s %(name)s %(levelname)-8s: %(message)s'
LOGDATEFORMAT = '%Y-%m-%d %H:%M:%S'

logFormatter = logging.Formatter(fmt=LOGFORMAT, datefmt=LOGDATEFORMAT)
#
logger = logging.getLogger(P_NAME)
logger.setLevel(logging.DEBUG)

# log to file
logFna = P_TMP_DIR +'/{0}.log'.format(P_NAME)
os.makedirs(P_TMP_DIR, exist_ok=True)
logFileHandler = logging.handlers.RotatingFileHandler(filename=logFna,
                                                      mode='a',
                                                      maxBytes=100*1024, backupCount=5)
logFileHandler.setLevel(logging.DEBUG)
logFileHandler.setFormatter(logFormatter)
logger.addHandler(logFileHandler)

import datetime
import requests
from cachecontrol import CacheControl
from cachecontrol.heuristics import BaseHeuristic
from email.utils import parsedate, formatdate
import calendar


class OneDayHeuristic(BaseHeuristic):
    """The OneWeekHeuristic class implenments a caching strategy 
    where every request should be cached for a day 
    regardless of the upstream cachingstrategy communicated in the response.

    When a response is received and we are testing for whether it is cacheable, 
    the heuristic is applied before checking its headers. 
    We also set a warning header to communicate why the response might be stale. 
    The original response is passed into the warning header in order to use its values. 
    For example, if the response has been expired 
    for more than 24 hours a Warning 113 should be used.

    Parameters
    ----------
    
    Attributes
    ----------
    
    Notes
    -----

    The `CacheControl` package contains
    the httplib2 caching algorithms packaged up for use with requests. 
    The `documentation <https://cachecontrol.readthedocs.io/en/latest/index.html>`_
    and 
    `project repository <https://github.com/ionrock/cachecontrol>`_

    """
    def __init__(self):
        logger.debug('Class "%s" instantiated.',
                     classname(self)) 

    def update_headers(self, response):
        logger.debug('"%s": response header "date" = %s.',
                     classname(self),
                     str(response.headers['date']))
        logger.debug('"%s": response header "expires" = %s.',
                     classname(self),
                     str(response.headers['cache-control']))
        logger.debug('"%s": response header "expires" = %s.',
                     classname(self),
                     str(response.headers['cache-control']))

        date = parsedate(response.headers['date'])
        expires = datetime.datetime(*date[:6]) + datetime.timedelta(days=1)
        logger.debug('"%s": modified header is now "expires" = %s.',
                     classname(self),
                     str(expires))
        return {
            'expires' : formatdate(calendar.timegm(expires.timetuple())),
            'cache-control' : 'public',
        }

    def warning(self, response):
        msg = 'Automatically cached! Response is Stale.'
        return '110 - "%s"' % msg



class OneWeekHeuristic(BaseHeuristic):
    """The OneWeekHeuristic class implenments a caching strategy 
    where every request should be cached for a week 
    regardless of the upstream cachingstrategy communicated in the response.

    When a response is received and we are testing for whether it is cacheable, 
    the heuristic is applied before checking its headers. 
    We also set a warning header to communicate why the response might be stale. 
    The original response is passed into the warning header in order to use its values. 
    For example, if the response has been expired 
    for more than 24 hours a Warning 113 should be used.

    Parameters
    ----------
    
    Attributes
    ----------
    
    Notes
    -----

    The `CacheControl` package contains
    the httplib2 caching algorithms packaged up for use with requests. 
    The `documentation <https://cachecontrol.readthedocs.io/en/latest/index.html>`_
    and 
    `project repository <https://github.com/ionrock/cachecontrol>`_

    """
    def __init__(self):
        logger.debug('Class "%s" instantiated.',
                     classname(self)) 
    
    def update_headers(self, response):
        logger.debug('"%s": response header "date" = %s.',
                     classname(self),
                     str(response.headers['date']))
        logger.debug('"%s": response header "expires" = %s.',
                     classname(self),
                     str(response.headers['cache-control']))
        logger.debug('"%s": response header "expires" = %s.',
                     classname(self),
                     str(response.headers['cache-control']))

        date = parsedate(response.headers['date'])
        expires = datetime.datetime(*date[:6]) + datetime.timedelta(weeks=1)
        logger.debug('"%s": modified header is now "expires" = %s.',
                     classname(self),
                     str(expires))
        return {
            'expires' : formatdate(calendar.timegm(expires.timetuple())),
            'cache-control' : 'public',
        }

    def warning(self, response):
        msg = 'Automatically cached! Response is Stale.'
        return '110 - "%s"' % msg


class ISO10383MIC:
    """The ISO10383MIC class represents a registry of exchanges, 
    trading platforms, markets and trade reporting facilities 

    

    Parameters
    ----------
    
    Attributes
    ----------
    implementationDt : pd.Timestamp
        The implementation time of this version of the MIC registry.
    self.micDf : pandas.DataFrame
        The currently available copy of this version of the MIC registry
    nextPublicationDt : pd.Timestamp
        The expected time of the next publication time of 
        next version of the MIC registry.
    publicationDt : pd.Timestamp
        The publication time of this version of the MIC registry.

    Notes
    -----

    The
    *ISO 10383:2012(en)
    Securities and related financial instruments — Codes for exchanges and market identification (MIC)*
    international standard specifies a universal method of identifying 
    exchanges, trading platforms, regulated or non-regulated markets 
    and trade reporting facilities 
    as sources of prices and related information in order to facilitate automated processing.
    It is intended for use in any application and communication for identification of places

    * where a financial instrument is listed (place of official listing),
    * where a related trade is executed (place of trade), and
    * where trade details are reported (trade reporting facility).

    Market Identifier Codes (MICs) are to be registered 
    at operating/exchange level and at market segment level. 
    Market segment MICs and their operating/exchange MIC are to be clearly linked 
    in the published lists.

    The Registration Authority (RA) for ISO 10383 (MIC) is:
    
    S.W.I.F.T. SC
    Avenue Adèle 1
    1310 La Hulpe
    BELGIUM
    Contact: MIC-ISO10383.Generic@swift.com
    """

    def __init__(self):
        logger.debug('Class "%s" instantiated.',
                     classname(self)) 
        self.instantiationDt = datetime.datetime.now(tz=datetime.timezone.utc)
        
        self.publicationDt = None
        self.implementationDt = None
        self.nextPublicationDt = None
        self.micDf = None

    def downloadMic(self,
                    micSite='https://www.iso20022.org',
                    micRelUrl='/market-identifier-codes',
                    micEncoding='windows-1252'):
        """Download MIC registry and convert it to a pandas DataFrame.

        The default authoritative source is on the web at
        `https://www.iso20022.org/market-identifier-codes <https://www.iso20022.org/market-identifier-codes>`_
        containing publication metadata and a reference to a file containing
        the MIC registry stored as comma seperated values.

        Parameters
        ----------
        micSite : str, optional
            Protocol and site part of the URL of the MIC registry  publication site to download from.
            Defaults to 'https://www.iso20022.org'.
        micRelUrl : str, optional
            Relative URL to the MIC registry publication site to download from.
            Defaults to '/market-identifier-codes'.
        micEncoding : str, optional
            Character encoding of the csv file referenced onto the MIC retistry publication site.
            Defaults to 'windows-1252'.

        Returns
        -------
        pandas.DataFrame
            The MIC registry as downloaded.

        """
        import os
        import requests
        from lxml import html
        import csv, sys
        from dateutil import parser as dtparser
        from cachecontrol.caches.file_cache import FileCache

        logger.debug('Class method "%s" entry.',
                     classname(self) + '.' + inspect.currentframe().f_code.co_name + '()')
        #
        # Coded from the contents of 'https://www.iso20022.org/market-identifier-codes'
        #
        micPersistencePath = P_PERSISTENCE_DIR + classname(self)
        os.makedirs(micPersistencePath, exist_ok=True)
        fnaPub = micPersistencePath + '/market-identifier-codes.html'

        usePersistedMicPub = False
        if os.path.isfile(fnaPub):
            logger.debug('Class method "%s": Persistence file "%s" exists.',
                         classname(self) + '.' + inspect.currentframe().f_code.co_name + '()',
                         fnaPub)
            mtimeDt = datetime.datetime.fromtimestamp(os.stat(fnaPub).st_mtime, datetime.timezone.utc)
            logger.debug('... mtime = ' + mtimeDt.isoformat())
            nowDt = datetime.datetime.now(tz= datetime.timezone.utc)
            logger.debug('... nowDt = ' + nowDt.isoformat())
            ageTd = nowDt - mtimeDt
            logger.debug('... File age = ' + str(ageTd))
            if ( ageTd < datetime.timedelta(days=0, hours=23)):
                logger.debug('... less than 23 hours old - use persisted file.')
                usePersistedMicPub = True
        #
        if (usePersistedMicPub):
            # read content from persisted file
            fh = open(fnaPub, 'rb')
            binaryPageContent = fh.read()
            fh.close()
        else:
            logger.debug('Class method "%s": Persisted file "%s" is unsuitable, fetch from source.',
                         classname(self) + '.' + inspect.currentframe().f_code.co_name + '()',
                         fnaPub)
            # Get the contents of the MIC publication url
            logger.debug('Class method "%s": fetch "%s".',
                         classname(self) + '.' + inspect.currentframe().f_code.co_name + '()',
                         micSite + micRelUrl)
            cachedSess = CacheControl(requests.Session(), 
                                      heuristic=OneDayHeuristic(),
                                      cache=FileCache(P_CACHE_DIR))
            resp = cachedSess.get(micSite + micRelUrl)
            binaryPageContent = resp.content
            #
            # Write new content to persisted file
            fh = open(fnaPub, 'wb')
            fh.write(binaryPageContent)
            fh.close()
        #
        # Parse it using the html module and save the result in tree.
        #
        # We need to use page.content rather than page.text because
        # html.fromstring implicitly expects bytes as input.
        tree = html.fromstring(binaryPageContent)
        # A good introduction to XPath is on http://www.w3schools.com/xml/xpath_intro.asp
        XpathtoRow = '//*[@id="block-iso20022-theme-content"]/article/div[2]/div[3]/div/div/table/tbody/tr'
        XPathToCsvUrl  = XpathtoRow + '/td[3]/a/@href'
        XPathToPubDate = XpathtoRow + '/td[6]/text()'
        XPathToImpDate = XpathtoRow + '/td[7]/text()'
        XPathToNxtDate = XpathtoRow + '/td[8]/text()'
        #
        micCsvRelUrl = tree.xpath(XPathToCsvUrl)[0].replace('\u00A0',' ')
        logger.debug('Parsed Rel. URL to publication in csv format: "' + micCsvRelUrl + '"')
        d = tree.xpath(XPathToPubDate)[0].replace('\u00A0',' ')
        self.publicationDt = dtparser.parse(d).replace(tzinfo=datetime.timezone.utc)
        logger.debug('Parsed Publication date: ' + self.publicationDt.isoformat())
        d = tree.xpath(XPathToImpDate)[0].replace('\u00A0',' ')
        self.implementationDt = dtparser.parse(d).replace(tzinfo=datetime.timezone.utc)
        logger.debug('Parsed Implementation date: ' + self.implementationDt.isoformat())
        d = tree.xpath(XPathToNxtDate)[0].replace('\u00A0',' ')
        self.nextPublicationDt = dtparser.parse(d).replace(tzinfo=datetime.timezone.utc)
        logger.debug('Parsed Next Publication date: ' + self.nextPublicationDt.isoformat())
        #
        # Fetch the MIC registry content as a CSV file
        #
        fnaCsv = P_PERSISTENCE_DIR + '/TmpISO10383_MIC.csv'
        os.makedirs(P_PERSISTENCE_DIR, exist_ok=True)

        usePersistedMicCsv = False
        if usePersistedMicPub and os.path.isfile(fnaCsv):
            logger.debug('Class method "%s": Persisted csv file "%s" exists.',
                         classname(self) + '.' + inspect.currentframe().f_code.co_name + '()',
                         fnaCsv)
            mtimeDt = datetime.datetime.fromtimestamp(os.stat(fnaCsv).st_mtime, datetime.timezone.utc)
            logger.debug('... mtime = ' + mtimeDt.isoformat())
            nowDt = datetime.datetime.now(tz= datetime.timezone.utc)
            logger.debug('... nowDt = ' + nowDt.isoformat())
            ageTd = nowDt - mtimeDt
            logger.debug('... File age = ' + str(ageTd))
            if ( ageTd < datetime.timedelta(days=0, hours=23)):
                logger.debug('... less than 23 hours old - use persisted file.')
                usePersistedMicCsv = True
        #
        if (usePersistedMicCsv):
            # read content from persisted file
            logger.debug('Class method "%s": Persisted file "%s" is suitable.',
                         classname(self) + '.' + inspect.currentframe().f_code.co_name + '()',
                         fnaCsv)
        else:
            logger.debug('Class method "%s": Persisted file "%s" is unsuitable, fetch from source.',
                         classname(self) + '.' + inspect.currentframe().f_code.co_name + '()',
                         fnaCsv)
            csvUrl = micSite + micCsvRelUrl
            logger.debug('Class method "%s": fetch "%s to local file %s".',
                         classname(self) + '.' + inspect.currentframe().f_code.co_name + '()',
                         csvUrl,
                         fnaCsv)
            # Get the csv file
            cachedSess = CacheControl(requests.Session(), 
                                      heuristic=OneDayHeuristic(),
                                      cache=FileCache(P_CACHE_DIR))
            resp = cachedSess.get(csvUrl)
            # Write new (binary) csv file to persisted file
            fh = open(fnaCsv, 'wb')
            fh.write(resp.content)
            fh.close()
        #
        #
        # Read and parse the downloaded CSV file to a list of Dict
        micRows = []
        with open(fnaCsv, 'r', encoding=micEncoding) as theFile:
            reader = csv.DictReader(theFile)
            try:
                for line in reader:
                    micRows.append(line)
            except csv.Error as e:
                msg = 'file {}, line {}: {}'.format(filename, reader.line_num, e)
                logger.critical(msg)
                sys.exit(msg)
        #
        # Create DataFrame from the list of OrderedDict's
        from collections import Counter
        row = Counter()
        for k in micRows:
            row.update(k)
        self.micDf = pd.DataFrame([k.values() for k in micRows], columns = row.keys())
        #
        # print(self.micDf)
        logger.debug('Class method "%s" return MIC as pandas DataFrame.',
                     classname(self) + '.' + inspect.currentframe().f_code.co_name + '()')
        return(self.micDf)


if __name__ == '__main__':
    
    m = ISO10383MIC()
    mDf = m.downloadMic()
    print('Returned MIC DataFrame:')
    print(mDf)
        
    
