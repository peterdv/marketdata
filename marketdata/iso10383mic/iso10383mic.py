# -*- coding: utf-8; mode: Python; -*-

import os
import sys
import datetime
import csv
import inspect
from lxml import html
from dateutil import parser as dtparser
import requests
from cachecontrol import CacheControl
from cachecontrol.caches.file_cache import FileCache
import pandas as pd
import logging
from one_day_heuristic import OneDayHeuristic
# from . import oneDayHeuristic
# import oneDayHeuristic


# docstring guide https://numpydoc.readthedocs.io/en/latest/format.html

P_NAME = 'ISO10383MIC'
P_TMP_DIR = '/tmp/' + P_NAME
P_CACHE_DIR = P_TMP_DIR + '/cache'
P_PERSISTENCE_DIR = P_TMP_DIR + '/persistence'


def typename(x):
    return type(x).__name__


def classname(x):
    return x.__class__.__qualname__


#
# Set up logging
#
#
module_logger = logging.getLogger(__name__)
module_logger.setLevel(logging.DEBUG)


class ISO10383MIC:
    """Registry of Market Identifier Codes.

    The ISO10383MIC class represents a registry of exchanges,
    trading platforms, regulated or non-regulated markets
    and trade reporting facilities.


    Parameters
    ----------


    Attributes
    ----------
    publication_time : datetime.datetime
        The publication time of this version of the MIC registry.
    implementation_time : datetime.datetime
        The implementation time of this version of the MIC registry.
    next_publication_time : datetime.datetime
        The expected time of the next publication time of
        next version of the MIC registry.
    self.mic : pandas.DataFrame
        The currently available copy of this version of the MIC registry

    Notes
    -----

    The
    *ISO 10383:2012(en)
    Securities and related financial instruments
    — Codes for exchanges and market identification (MIC)*
    international standard specifies a universal method of identifying
    exchanges, trading platforms, regulated or non-regulated markets
    and trade reporting facilities
    as sources of prices and related information in order to facilitate
    automated processing.
    It is intended for use in
    any application and communication for identification of places

    * where a financial instrument is listed (place of official listing),
    * where a related trade is executed (place of trade), and
    * where trade details are reported (trade reporting facility).

    Market Identifier Codes (MICs) are to be registered
    at operating/exchange level and at market segment level.
    Market segment MICs and their operating/exchange MIC
    are to be clearly linked in the published lists.

    The Registration Authority (RA) for ISO 10383 (MIC) is:

    S.W.I.F.T. SC
    Avenue Adèle 1
    1310 La Hulpe
    BELGIUM
    Contact: MIC-ISO10383.Generic@swift.com
    """

    import logging

    def __init__(self):
        logger = logging.getLogger(__name__).getChild(self.__class__.__name__)
        # logger = logging.getLogger(__name__)
        logger.debug('Class "%s" instantiated.',
                     classname(self))

        self._logger = logger
        self.instantiationDt = datetime.datetime.now(tz=datetime.timezone.utc)

        self.publication_time = None
        self.implementation_time = None
        self.next_publication_time = None
        self.mic = None

    def download_mic(self,
                     mic_site='https://www.iso20022.org',
                     mic_rel_url='/market-identifier-codes',
                     mic_encoding='windows-1252'):
        """Download MIC registry and convert it to a pandas.DataFrame.

        The default authoritative source is on the web at
        `https://www.iso20022.org/market-identifier-codes
        <https://www.iso20022.org/market-identifier-codes>`_
        containing publication metadata and a reference to a file containing
        the MIC registry stored as comma seperated values.

        Parameters
        ----------
        mic_site : str, optional
            Protocol and site part of the URL of
            the MIC registry  publication site to download from.
            Defaults to 'https://www.iso20022.org'.
        mic_rel_url : str, optional
            Relative URL to the MIC registry publication site to download from.
            Defaults to '/market-identifier-codes'.
        mic_encoding : str, optional
            Character encoding of the csv file referenced to
            on the MIC retistry publication site.
            Defaults to 'windows-1252'.

        Returns
        -------
        pandas.DataFrame
            The MIC registry as downloaded.

        """

        # logger = logging.getLogger(__name__)
        lna = classname(self) + '.' + inspect.currentframe().f_code.co_name
        logger = logging.getLogger(lna)

        logger.debug('Class method "%s" entry.',
                     classname(self) + '.' +
                     inspect.currentframe().f_code.co_name + '()')
        #
        # Coded from the contents of
        # 'https://www.iso20022.org/market-identifier-codes'
        #
        mic_persistence_path = P_PERSISTENCE_DIR + '/' + classname(self)
        os.makedirs(mic_persistence_path, exist_ok=True)
        fna_pub = mic_persistence_path + '/' + 'market-identifier-codes.html'

        use_persisted_mic_pub = False
        if os.path.isfile(fna_pub):
            logger.debug('Class method "%s": Persistence file "%s" exists.',
                         classname(self)
                         + '.'
                         + inspect.currentframe().f_code.co_name + '()',
                         fna_pub)
            now = datetime.datetime.now(tz=datetime.timezone.utc)
            mtime = datetime.datetime.fromtimestamp(os.stat(fna_pub).st_mtime,
                                                    datetime.timezone.utc)
            age = now - mtime
            logger.debug('... mtime = ' + mtime.isoformat())
            logger.debug('... now = ' + now.isoformat())
            logger.debug('... File age = ' + str(age))
            if (age < datetime.timedelta(days=0, hours=23)):
                logger.debug(
                    '... less than 23 hours old - use persisted file.')
                use_persisted_mic_pub = True
        #
        if (use_persisted_mic_pub):
            # read content from persisted file
            fh = open(fna_pub, 'rb')
            binary_page_content = fh.read()
            fh.close()
        else:
            logger.debug('Class method "%s": Persisted file "%s"'
                         ' is unsuitable, fetch from source.',
                         classname(self)
                         + '.'
                         + inspect.currentframe().f_code.co_name
                         + '()',
                         fna_pub)
            # Get the contents of the MIC publication url
            logger.debug('Class method "%s": fetch "%s".',
                         classname(self)
                         + '.'
                         + inspect.currentframe().f_code.co_name
                         + '()',
                         mic_site + mic_rel_url)
            cache_override = OneDayHeuristic()
            cached_sess = CacheControl(requests.Session(),
                                       heuristic=cache_override,
                                       cache=FileCache(P_CACHE_DIR))
            resp = cached_sess.get(mic_site + mic_rel_url)
            binary_page_content = resp.content
            #
            # Write new content to persisted file
            fh = open(fna_pub, 'wb')
            fh.write(binary_page_content)
            fh.close()
        #
        # Parse it using the html module and save the result in tree.
        #
        # We need to use page.content rather than page.text because
        # html.fromstring implicitly expects bytes as input.
        tree = html.fromstring(binary_page_content)
        # A good introduction to XPath is on
        # http://www.w3schools.com/xml/xpath_intro.asp
        #
        XPATH_ROW = '//*[@id="block-iso20022-theme-content"]/article' \
            + '/div[2]/div[3]/div/div/table/tbody/tr'
        XPATH_CSV_URL = XPATH_ROW + '/td[3]/a/@href'
        XPATH_PUB_DATE = XPATH_ROW + '/td[6]/text()'
        XPATH_IMP_DATE = XPATH_ROW + '/td[7]/text()'
        XPATH_NEXT_DATE = XPATH_ROW + '/td[8]/text()'
        #
        mic_csv_rel_url = tree.xpath(XPATH_CSV_URL)[0].replace('\u00A0', ' ')
        logger.debug('Parsed Rel. URL to publication in csv format: "'
                     + mic_csv_rel_url
                     + '"')
        d = tree.xpath(XPATH_PUB_DATE)[0].replace('\u00A0', ' ')
        self.publication_time \
            = dtparser.parse(d).replace(tzinfo=datetime.timezone.utc)
        logger.debug('Parsed Publication date: '
                     + self.publication_time.isoformat())
        d = tree.xpath(XPATH_IMP_DATE)[0].replace('\u00A0', ' ')
        self.implementation_time \
            = dtparser.parse(d).replace(tzinfo=datetime.timezone.utc)
        logger.debug('Parsed Implementation date: '
                     + self.implementation_time.isoformat())
        d = tree.xpath(XPATH_NEXT_DATE)[0].replace('\u00A0', ' ')
        self.next_publication_time \
            = dtparser.parse(d).replace(tzinfo=datetime.timezone.utc)
        logger.debug('Parsed Next Publication date: '
                     + self.next_publication_time.isoformat())
        #
        # Fetch the MIC registry content as a CSV file
        #
        fna_csv = mic_persistence_path + '/' + 'ISO10383_MIC.csv'

        use_persisted_mic_csv = False
        if use_persisted_mic_pub and os.path.isfile(fna_csv):
            logger.debug('Class method "%s": Persisted csv file "%s" exists.',
                         classname(self)
                         + '.'
                         + inspect.currentframe().f_code.co_name
                         + '()',
                         fna_csv)
            now = datetime.datetime.now(tz=datetime.timezone.utc)
            mtime = datetime.datetime.fromtimestamp(os.stat(fna_csv).st_mtime,
                                                    datetime.timezone.utc)
            age = now - mtime
            logger.debug('... mtime = ' + mtime.isoformat())
            logger.debug('... now   = ' + now.isoformat())
            logger.debug('... File age = ' + str(age))
            if (age < datetime.timedelta(days=0, hours=23)):
                logger.debug(
                    '... less than 23 hours old - use persisted file.')
                use_persisted_mic_csv = True
        #
        if (use_persisted_mic_csv):
            # read content from persisted file
            logger.debug('Class method "%s": Persisted file "%s" is suitable.',
                         classname(self)
                         + '.'
                         + inspect.currentframe().f_code.co_name
                         + '()',
                         fna_csv)
        else:
            logger.debug('Class method "%s": Persisted file "%s"'
                         ' is unsuitable, fetch from source.',
                         classname(self)
                         + '.'
                         + inspect.currentframe().f_code.co_name
                         + '()',
                         fna_csv)
            csv_url = mic_site + mic_csv_rel_url
            logger.debug('Class method "%s": fetch "%s to local file %s".',
                         classname(self)
                         + '.'
                         + inspect.currentframe().f_code.co_name
                         + '()',
                         csv_url,
                         fna_csv)
            # Get the csv file
            cached_sess = CacheControl(requests.Session(),
                                       heuristic=OneDayHeuristic(),
                                       cache=FileCache(P_CACHE_DIR))
            resp = cached_sess.get(csv_url)
            # Write new (binary) csv file to persisted file
            fh = open(fna_csv, 'wb')
            fh.write(resp.content)
            fh.close()
        #
        #
        # Read and parse the downloaded CSV file to a list of Dict
        mic_rows = []
        with open(fna_csv, 'r', encoding=mic_encoding) as the_file:
            reader = csv.DictReader(the_file)
            try:
                for line in reader:
                    mic_rows.append(line)
            except csv.Error as e:
                msg = 'file {}, line {}: {}'.format(
                    fna_csv, reader.line_num, e)
                logger.critical(msg)
                sys.exit(msg)
        #
        # Create DataFrame from the list of OrderedDict's
        from collections import Counter
        row = Counter()
        for k in mic_rows:
            row.update(k)
        self.mic = pd.DataFrame([k.values() for k in mic_rows],
                                columns=row.keys())
        #
        # print(self.micDf)
        logger.debug('Class method "%s" return MIC as pandas DataFrame.',
                     classname(self)
                     + '.'
                     + inspect.currentframe().f_code.co_name
                     + '()')
        return(self.mic)


if __name__ == '__main__':
    import logging
    import logging.handlers

    LOGFORMAT = '%(asctime)s %(name)s %(levelname)-8s %(message)s'
    LOGDATEFORMAT = '%Y-%m-%d %H:%M:%S'
    log_formatter = logging.Formatter(fmt=LOGFORMAT, datefmt=LOGDATEFORMAT)
    #
    logging.getLogger().setLevel(logging.DEBUG)
    logger = logging.getLogger()
    #
    # log to file
    log_fna = P_TMP_DIR + '/{0}.log'.format(P_NAME)
    os.makedirs(P_TMP_DIR, exist_ok=True)
    log_file_handler = logging.handlers.RotatingFileHandler(
        filename=log_fna,
        mode='a',
        maxBytes=100 * 1024,
        backupCount=5)
    log_file_handler.setLevel(logging.DEBUG)
    log_file_handler.setFormatter(log_formatter)
    logger.addHandler(log_file_handler)
    #

    def show_loggers():
        loggers = [('root', logging.getLogger())]
        for name in sorted(logging.Logger.manager.loggerDict.keys()):
            logger = logging.getLogger(name)
            loggers.append((name, logger))
        for name, logger in loggers:
            indent = ""
            if name != 'root':
                indent = "   " * (name.count('.') + 1)
            if logger.propagate:
                prop = "+ "
            else:
                prop = "  "
            handlers = ""
            if len(logger.handlers) > 0:
                handlers = ": " + str(logger.handlers)
            level = logging.getLevelName(logger.level)
            eff_level = logging.getLevelName(logger.getEffectiveLevel())
            if level == eff_level:
                level_str = ' [%s]' % level
            else:
                level_str = ' [%s -> %s]' % (level, eff_level)
            print(indent + prop + name + level_str + handlers)

    show_loggers()

    m = ISO10383MIC()
    df = m.download_mic()
    print('Returned MIC DataFrame:')
    print(df)
