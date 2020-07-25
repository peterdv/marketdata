#!/usr/bin/env python
# -*- coding: utf-8; mode: Python; -*-

from ISO10383MIC import ISO10383MIC

def test_init():
    mic = ISO10383MIC()
    assert mic.publicationDt == None
