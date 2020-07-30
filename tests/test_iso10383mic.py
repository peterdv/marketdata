#!/usr/bin/env python
# -*- coding: utf-8; mode: Python; -*-
import os
import logging
import inspect
import datetime
import pytest
import pandas

from marketdata.referencedata.iso10383mic import ISO10383MIC

FIXTURE_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'data',
)

ISO20022ORG_SAMPLES_DIR = pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, 'iso10383mic', 'www.iso20022.org'),
    keep_top_dir=True,
)


def test_iso10383mic_init_nodata(caplog):
    """Verify ISO10383MIC attributes.

    Veryfy the existence and default values of
    ISO10383MIC
    attributes.
    """

    print(inspect.currentframe().f_code.co_name)
    # caplog.set_level(logging.DEBUG)
    mic = ISO10383MIC()
    assert mic.mic is None
    assert mic.publication_time is None
    assert mic.implementation_time is None
    assert mic.next_publication_time is None
    assert mic.from_cache is False
    assert mic.from_persisted is False


@ISO20022ORG_SAMPLES_DIR
def test_iso10383mic_init(datafiles, caplog):
    """Verify ISO10383MIC with sample data.

    Instantiate an use
    ISO10383MIC
    based on sample data.
    """

    print('Function: "{}"'.format(inspect.currentframe().f_code.co_name))
    # caplog.set_level(logging.DEBUG)
    tmp_path = str(datafiles)
    d_path = os.path.join(tmp_path, 'www.iso20022.org')
    print('"{0}" contains {1} files'.format(d_path, len(os.listdir(d_path))))
    for f in os.listdir(d_path):
        print(' * file "{}"'.format(f))
    assert len(os.listdir(d_path)) >= 11
    assert os.path.isfile(os.path.join(d_path, 'market-identifier-codes.html'))
    assert os.path.isfile(os.path.join(d_path, 'ISO10383_MIC.csv'))

    test_data_site = 'file://' + d_path + '/'
    rel_url = 'market-identifier-codes.html'
    cache_dir = os.path.join(tmp_path, 'cache_init')
    persist_dir = os.path.join(tmp_path, 'persistence_init')
    #
    print('mic_site            = "{}"'.format(test_data_site))
    print('mic_rel_url         = "{}"'.format(rel_url))
    print('mic_cache_dir       = "{}"'.format(cache_dir))
    print('mic_persistence_dir = "{}"'.format(persist_dir))
    mic = ISO10383MIC(mic_site=test_data_site,
                      mic_rel_url=rel_url,
                      mic_csv_encoding='windows-1252',
                      mic_cache_dir=cache_dir,
                      mic_persistence_dir=persist_dir)
    assert mic.mic is None
    assert mic.publication_time is None
    assert mic.implementation_time is None
    assert mic.next_publication_time is None
    assert mic.from_cache is False
    assert mic.from_persisted is False
    #
    df = mic.download_mic()
    assert isinstance(df, pandas.DataFrame)
    assert isinstance(mic.mic, pandas.DataFrame)
    assert mic.publication_time is not None
    assert isinstance(mic.publication_time, datetime.datetime)
    assert mic.implementation_time is not None
    assert isinstance(mic.implementation_time, datetime.datetime)
    assert mic.next_publication_time is not None
    assert isinstance(mic.next_publication_time, datetime.datetime)
    assert mic.from_cache is False
    assert mic.from_persisted is False
    #
    print('mic.download_mic() returned MIC DataFrame:')
    print(df)


@ISO20022ORG_SAMPLES_DIR
def test_iso10383mic_from_persisted(datafiles, caplog):
    """Verify ISO10383MIC with persisted data.

    Instantiate an use
    ISO10383MIC
    based on persisted data.
    """

    print('Function: "{}"'.format(inspect.currentframe().f_code.co_name))
    caplog.set_level(logging.DEBUG)
    tmp_path = str(datafiles)
    d_path = os.path.join(tmp_path, 'www.iso20022.org')
    print('"{0}" contains {1} files'.format(d_path, len(os.listdir(d_path))))
    for f in os.listdir(d_path):
        print(' * file "{}"'.format(f))
    assert os.path.isfile(os.path.join(d_path, 'market-identifier-codes.html'))
    assert os.path.isfile(os.path.join(d_path, 'ISO10383_MIC.csv'))
    #
    test_data_site = 'file://' + d_path + '/'
    rel_url = 'market-identifier-codes.html'
    cache_dir = os.path.join(tmp_path, 'cache_from_persisted')
    persist_dir = os.path.join(tmp_path, 'persistence_from_persisted')
    #
    if os.path.isdir(persist_dir):
        print('"{0}" contains {1} files'.format(persist_dir,
                                                len(os.listdir(persist_dir))))
        for f in os.listdir(persist_dir):
            print(' * file "{}"'.format(f))
    else:
        print('"{}" does not exist yet.'.format(persist_dir))
    #
    print('mic_site            = "{}"'.format(test_data_site))
    print('mic_rel_url         = "{}"'.format(rel_url))
    print('mic_cache_dir       = "{}"'.format(cache_dir))
    print('mic_persistence_dir = "{}"'.format(persist_dir))
    mic = ISO10383MIC(mic_site=test_data_site,
                      mic_rel_url=rel_url,
                      mic_csv_encoding='windows-1252',
                      mic_cache_dir=cache_dir,
                      mic_persistence_dir=persist_dir)
    assert mic.mic is None
    assert mic.publication_time is None
    assert mic.from_cache is False
    assert mic.from_persisted is False
    #
    print('Before first download_mic() call, expect no persisted data')
    assert os.path.isdir(persist_dir) is False
    #
    df = mic.download_mic()
    #
    print('After first download_mic() call, '
          + 'expect persisted data to have been created, but not yet used.')
    if os.path.isdir(persist_dir):
        print('"{0}" contains {1} files'.format(persist_dir,
                                                len(os.listdir(persist_dir))))
        for f in os.listdir(persist_dir):
            print(' * file "{}"'.format(f))
    else:
        print('"{}" does not exist yet.'.format(persist_dir))
    #
    assert os.path.isdir(persist_dir) is True
    assert isinstance(df, pandas.DataFrame)
    assert isinstance(mic.mic, pandas.DataFrame)
    assert mic.publication_time is not None
    assert mic.from_cache is False
    assert mic.from_persisted is False  # Just created, not used
    #
    df2 = mic.download_mic()
    #
    print('After second download_mic() call, '
          + 'expect persisted data to have been used.')
    print('   ... mic.from_persisted = {}'.format(mic.from_persisted))
    #
    assert os.path.isdir(persist_dir) is True
    assert mic.from_cache is False
    assert mic.from_persisted is True  # Used
    #

    mic3 = ISO10383MIC(mic_site=test_data_site,
                       mic_rel_url=rel_url,
                       mic_csv_encoding='windows-1252',
                       mic_cache_dir=cache_dir,
                       mic_persistence_dir=persist_dir)
    assert mic3.mic is None
    df3 = mic3.download_mic()
    print('Expect persisted data to be shared across instances')
    print('   ... mic.from_persisted = {}'.format(mic.from_persisted))

    assert isinstance(df3, pandas.DataFrame)
    assert isinstance(mic3.mic, pandas.DataFrame)
    assert isinstance(mic3.publication_time, datetime.datetime)
    assert mic3.from_cache is False
    assert mic3.from_persisted is True  # Used. Shared across instances
    #
    #


@ISO20022ORG_SAMPLES_DIR
def test_iso10383mic_from_iso_site(datafiles, caplog):
    """Verify ISO10383MIC with real data.

    Instantiate an use
    ISO10383MIC
    based on real on-line  data.
    """

    print('Function: "{}"'.format(inspect.currentframe().f_code.co_name))
    caplog.set_level(logging.DEBUG)
    tmp_path = str(datafiles)
    cache_dir = os.path.join(tmp_path, 'cache_from_iso_site')
    persist_dir = os.path.join(tmp_path, 'persistence_from_iso_site')
    #
    mic = ISO10383MIC(mic_cache_dir=cache_dir,
                      mic_persistence_dir=persist_dir)
    df = mic.download_mic()
    assert mic.from_cache is False
    assert mic.from_persisted is False
    #
    df = mic.download_mic()
    assert mic.from_cache is False
    assert mic.from_persisted is True
    #
    # Remove persisted files - to force use of cache
    #
    if os.path.isdir(persist_dir):
        print('Remove persisted files, to trigger use of http cache:')
        for f in os.listdir(persist_dir):
            ff = os.path.join(persist_dir, f)
            print(' * file "{}"'.format(ff))
            try:
                os.remove(ff)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (ff, e))
    df = mic.download_mic()
    assert mic.from_cache is True
    assert mic.from_persisted is False
    #
