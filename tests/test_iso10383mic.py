#!/usr/bin/env python
# -*- coding: utf-8; mode: Python; -*-

from iso10383mic import ISO10383MIC

def test_init():
    mic = ISO10383MIC()
    assert mic.publication_time == None
