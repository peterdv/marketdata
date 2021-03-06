# -*- coding: utf-8; mode: Python; -*-
import inspect
import datetime
from cachecontrol.heuristics import BaseHeuristic
from email.utils import parsedate, formatdate
import calendar
import logging


def typename(x):
    return type(x).__name__


def classname(x):
    return x.__class__.__qualname__


class OneDayHeuristic(BaseHeuristic):
    """One day caching stratigy for `CacheControl`.

    This class implenments a caching strategy
    where every request should be cached for a day
    regardless of the upstream cachingstrategy communicated in the response.

    Parameters
    ----------

    Attributes
    ----------

    Notes
    -----

    When a response is received and we are testing for whether it is cacheable,
    the heuristic is applied before checking its headers.
    We also set a warning header
    to communicate why the response might be stale.
    The original response is passed into the warning header
    in order to use its values.
    For example, if the response has been expired
    for more than 24 hours a Warning 113 should be used.

    The `CacheControl` package contains
    the httplib2 caching algorithms packaged up for use with requests.
    The
    `documentation <https://cachecontrol.readthedocs.io/en/latest/index.html>`_
    and
    `project repository <https://github.com/ionrock/cachecontrol>`_

    """

    def __init__(self):
        lna = classname(self) + '.' + inspect.currentframe().f_code.co_name
        logger = logging.getLogger(lna)
        logger.debug('Class "%s" instantiated.',
                     classname(self))

    def update_headers(self, response):
        lna = classname(self) + '.' + inspect.currentframe().f_code.co_name
        logger = logging.getLogger(lna)
        logger.debug('"%s": response header "date" = %s.',
                     classname(self),
                     str(response.headers['date']))
        logger.debug('"%s": response header "expires" = %s.',
                     classname(self),
                     str(response.headers['expires']))
        logger.debug('"%s": response header "cache-control" = %s.',
                     classname(self),
                     str(response.headers['cache-control']))

        date = parsedate(response.headers['date'])
        expires = datetime.datetime(*date[:6]) + datetime.timedelta(days=1)
        logger.debug('"%s": modified header is now "expires" = %s.',
                     classname(self),
                     str(expires))
        return {
            'expires': formatdate(calendar.timegm(expires.timetuple())),
            'cache-control': 'public',
        }

    def warning(self, response):
        lna = classname(self) + '.' + inspect.currentframe().f_code.co_name
        logger = logging.getLogger(lna)
        logger.debug('Add warning (110) headder')
        msg = 'Automatically cached! Response is Stale.'
        return '110 - "%s"' % msg
