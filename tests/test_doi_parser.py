#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Kevin M. Jablonka'
__copyright__ = 'MIT License'
__maintainer__ = 'Kevin M. Jablonka'
__email__ = 'kevin.jablonka@epfl.ch'
__version__ = '0.1.0'
__status__ = 'First Draft, Testing'

import re
from parse_doi import doi_parser

def test_doi_parser():
    doi_list = ['10.1039/b822934c', '10.1002/ejic.201700457', '10.1021/cg800248b']

    uv_regex_list = ['uv', 'uv-vis', 'vis']
    uv_regex = re.compile('|'.join(uv_regex_list), re.IGNORECASE)

    photo_regex_list = ['photo', 'absorp', 'light', 'lumin']
    photo_regex = re.compile('|'.join(photo_regex_list), re.IGNORECASE)

    electronic_regex_list = ['electronic', 'conduc']
    electronic_regex = re.compile('|'.join(electronic_regex_list),
                                  re.IGNORECASE)

    spectroscopy_regex_list = ['spectroscopy']
    spectroscopy_regex = re.compile('|'.join(spectroscopy_regex_list),
                                  re.IGNORECASE)

    regex_dict = {
        'uv': uv_regex,
        'photo': photo_regex,
        'electronic': electronic_regex,
        'spectroscopy': spectroscopy_regex
    }

    dp = doi_parser.DoiParser(doi_list, regex_dict)
    df = dp.parse()

    assert len(df) == len(doi_list)