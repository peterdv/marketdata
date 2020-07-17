# -*- coding: utf-8; mode: Python; -*-

import datetime
import csv
import pandas as pd
import inspect

# docstring guide https://numpydoc.readthedocs.io/en/latest/format.html

P_TMP_DIR = '/tmp/'
P_CACHE_DIR = './'
P_PERSISTENCE_DIR = ''

def typename(x): return type(x).__name__
#def classname(x): return x.__class__.__name__
def classname(x): return x.__class__.__qualname__

#
# Set up logging
#
import logging, logging.handlers

LOGFORMAT = '%(asctime)s %(name)s %(levelname)-8s: %(message)s'
LOGDATEFORMAT = '%Y-%m-%d %H:%M:%S'
NAME = 'ISO10383MIC'

logFormatter = logging.Formatter(fmt=LOGFORMAT, datefmt=LOGDATEFORMAT)
#
logger = logging.getLogger(NAME)
logger.setLevel(logging.DEBUG)

# log to file
logFileHandler = logging.handlers.RotatingFileHandler(filename='{0}.log'.format(NAME),
                                                      mode='a',
                                                      maxBytes=100*1024, backupCount=5)
logFileHandler.setLevel(logging.DEBUG)
logFileHandler.setFormatter(logFormatter)
logger.addHandler(logFileHandler)


class ISO10383MIC:
    """The ISO10383MIC class represents a registry of exchanges, trading platforms, markets and trade reporting facilities 

    

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
        self.instantiationDt = datetime.datetime(2011, 11, 4,
                                                 hour=0, minute=0, second=0, microsecond=0,
                                                 tzinfo=datetime.timezone.utc)
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
        import requests
        from lxml import html
        import csv, sys
        from dateutil import parser as dtparser

        logger.debug('Class method "%s" entry.',
                     classname(self) + '.' + inspect.currentframe().f_code.co_name + '()')
        #
        # Coded from the contents of 'https://www.iso20022.org/market-identifier-codes'
        #
        micCachePath = P_CACHE_DIR + classname(self) + '/'
        #fna = micCachePath + 'market-identifier-codes.html'
        #open(fna, 'wb').write(r.content)
    
        #
        # Get the contents of the MIC publication url
        logger.debug('Class method "%s": fetch "%s".',
                     classname(self) + '.' + inspect.currentframe().f_code.co_name + '()',
                     micSite + micRelUrl)
        page = requests.get(micSite + micRelUrl)
        #
        # Parse it using the html module and save the result in tree.
        #
        # We need to use page.content rather than page.text because
        # html.fromstring implicitly expects bytes as input.
        tree = html.fromstring(page.content)
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
        FNA = 'TmpISO10383_MIC.csv'
        csvUrl = micSite + micCsvRelUrl
        logger.debug('Class method "%s": fetch "%s to local file %s".',
                     classname(self) + '.' + inspect.currentframe().f_code.co_name + '()',
                     csvUrl,
                     FNA)
        r = requests.get(csvUrl, allow_redirects=True)
        open(FNA, 'wb').write(r.content)
        #
        #
        # Read and parse the downloaded CSV file to a list of Dict
        micRows = []
        with open( FNA, 'r', encoding=micEncoding) as theFile:
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
        
    
