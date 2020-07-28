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
from .one_day_heuristic import OneDayHeuristic
from requests_testadapter import Resp

# From . import oneDayHeuristic
# import oneDayHeuristic

#
# Set up module level logging
#
#
module_logger = logging.getLogger(__name__)
module_logger.setLevel(logging.DEBUG)

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
#
# https://stackoverflow.com/questions/10123929/fetch-a-file-from-a-local-url-with-python-requests
#
# As @WooParadog explained requests library doesn't know how to handle
# local files.
# Although, current version allows to define transport adapters.
#
# Therefore you can simply define you own adapter which will be able to handle
# local files, e.g.:
#


class LocalFileAdapter(requests.adapters.HTTPAdapter):
    def build_response_from_file(self, request):
        lna = classname(self) + '.' + inspect.currentframe().f_code.co_name
        logger = logging.getLogger(lna)

        logger.debug('url       = "{}"'.format(request.url))
        file_path = request.url[7:]
        logger.debug('file_path = "{}"'.format(file_path))
        with open(file_path, 'rb') as file:
            buff = bytearray(os.path.getsize(file_path))
            file.readinto(buff)
            resp = Resp(buff)
            r = self.build_response(request, resp)

            return r

    def send(self, request, stream=False, timeout=None,
             verify=True, cert=None, proxies=None):

        return self.build_response_from_file(request)


class ISO10383MIC:
    """Registry of Market Identifier Codes.

    The ISO10383MIC class represents a registry of exchanges,
    trading platforms, regulated or non-regulated markets
    and trade reporting facilities.


    Parameters
    ----------

    mic_site : str, optional
        Protocol and site part of the URL of
        the MIC registry  publication site to download from.
    mic_rel_url : str, optional
        Relative URL to the MIC registry publication site to download from.
    mic_csv_encoding : str, optional
        Character encoding of the csv file referenced to
        on the MIC retistry publication site.
    mic_tmp_dir : str, optional
        Path to a temporary directory.
    mic_cache_dir : str, optional
        Path name to a directory to store cached data.
    mic_persistence_dir : str, optional
        Path name to a directory to store data intended
        to exist, and be shared across class instances.

    Attributes
    ----------
    publication_time : datetime.datetime or None
        The publication time of this version of the MIC registry.
    implementation_time : datetime.datetime or None
        The implementation time of this version of the MIC registry.
    next_publication_time : datetime.datetime or None
        The expected time of the next publication time of
        next version of the MIC registry.
    mic : pandas.DataFrame or None
        This version of the MIC registry.
    from_cache : boleean
        Is data fetched from cached session, rather than
        from `mic_site`.
    from_persisted : boleean
        Is data fetched from persisted data, rather than
        from `mic_site`, or cached session.

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
    def __init__(self,
                 mic_site='https://www.iso20022.org',
                 mic_rel_url='/market-identifier-codes',
                 mic_csv_encoding='windows-1252',
                 mic_tmp_dir='/tmp/ISO10383MIC',
                 mic_cache_dir='/tmp/ISO10383MIC/cache',
                 mic_persistence_dir='/tmp/ISO10383MIC/persistence'):
        #
        lna = classname(self) + '.' + inspect.currentframe().f_code.co_name
        logger = logging.getLogger(lna)

        logger.debug('Class "%s" instantiated.',
                     classname(self))

        self._logger = logger
        self.instantiationDt = datetime.datetime.now(tz=datetime.timezone.utc)

        self.publication_time = None
        self.implementation_time = None
        self.next_publication_time = None
        self.mic = None
        self.from_cache = False
        self.from_persisted = False
        #
        self._mic_site = mic_site
        self._mic_rel_url = mic_rel_url
        self._mic_csv_encoding = mic_csv_encoding
        self._mic_tmp_dir = mic_tmp_dir
        self._mic_cache_dir = mic_cache_dir
        self._mic_persistence_dir = mic_persistence_dir

    def download_mic(self):
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
        os.makedirs(self._mic_persistence_dir, exist_ok=True)
        fna_pub = os.path.join(self._mic_persistence_dir,
                               'market-identifier-codes.html')
        #
        requests_session = requests.session()
        requests_session.mount('file://', LocalFileAdapter())

        use_persisted_mic_pub = False
        if os.path.isfile(fna_pub):
            logger.debug(' Persistence file "%s" exists.',
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
            self.from_cache = False
            self.from_persisted = True
        else:
            logger.debug('Persisted file "%s"'
                         ' is unsuitable, fetch from source.',
                         fna_pub)
            # Get the contents of the MIC publication url
            logger.debug('fetch from "%s".',
                         self._mic_site + self._mic_rel_url)
            #
            cache_override = OneDayHeuristic()

            # cached_sess = CacheControl(requests.Session(),
            os.makedirs(self._mic_cache_dir, exist_ok=True)

            cached_sess = CacheControl(requests_session,
                                       heuristic=cache_override,
                                       cache=FileCache(self._mic_cache_dir))
            resp = cached_sess.get(self._mic_site + self._mic_rel_url)
            binary_page_content = resp.content
            try:
                self.from_cache = resp.from_cache
                logger.debug('from_cache reported by CacheControl:'
                             + ' from_cache = {}'.format(self.from_cache))
            except AttributeError:
                self.from_cache = False
                logger.debug('from_cache missing from CacheControl.'
                             + ' Default from_cache ='
                             + ' {}'.format(self.from_cache))
            #
            # Write new content to persisted file
            fh = open(fna_pub, 'wb')
            fh.write(binary_page_content)
            fh.close()
            self.from_persisted = False
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

        fna_csv = os.path.join(self._mic_persistence_dir, 'ISO10383_MIC.csv')

        use_persisted_mic_csv = False

        # Only consider persisted mic if persisted publication page was used
        use_p = (use_persisted_mic_pub
                 and os.path.isfile(fna_csv)
                 and self.from_persisted)
        if (use_p):
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
            logger.debug('Persisted file "%s" is suitable.',
                         fna_csv)
        else:
            logger.debug('Persisted file "%s"'
                         ' is unsuitable, fetch from source.',
                         fna_csv)
            csv_url = self._mic_site + mic_csv_rel_url
            logger.debug('fetch "%s to local file %s".',
                         csv_url,
                         fna_csv)
            # Get the csv file
            # cached_sess = CacheControl(requests.Session(),
            cached_sess = CacheControl(requests_session,
                                       heuristic=OneDayHeuristic(),
                                       cache=FileCache(self._mic_cache_dir))
            resp = cached_sess.get(csv_url)
            try:
                self.from_cache = resp.from_cache
                logger.debug('from_cache reported by CacheControl:'
                             + ' from_cache = {}'.format(self.from_cache))
            except AttributeError:
                self.from_cache = False
                logger.debug('from_cache missing from CacheControl.'
                             + ' Default from_cache ='
                             + ' {}'.format(self.from_cache))
            self.from_persisted = False
            # Write new (binary) csv file to persisted file
            fh = open(fna_csv, 'wb')
            fh.write(resp.content)
            fh.close()
        #
        #
        # Read and parse the downloaded CSV file to a list of Dict
        mic_rows = []
        with open(fna_csv, 'r', encoding=self._mic_csv_encoding) as the_file:
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
        logger.debug('Return MIC as pandas DataFrame.')
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
    print(' * from_persisted: {}'.format(m.from_persisted))
    print(' * from_cache:     {}'.format(m.from_cache))
