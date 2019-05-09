#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Kevin M. Jablonka'
__copyright__ = 'MIT License'
__maintainer__ = 'Kevin M. Jablonka'
__email__ = 'kevin.jablonka@epfl.ch'
__version__ = '0.1.0'
__status__ = 'First Draft, Testing'

from crossref.restful import Works
works = Works()
import pandas as pd
from requests_html import HTMLSession
from collections import defaultdict
from tqdm.autonotebook import tqdm
import concurrent.futures
import logging
import re
from .utils import isnotebook
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class DoiParser():
    """
    Class is initialized with a list of DOIs (strings) and a dictionary
    of regexes. The idea of this approach is that the output of this parser
    will be a list of dictionary (one dictionary with the regex_dict keys as key
    for each structure).

    Biggest problem before parsing a full-text website is that JavaScript needs to be
    rendered.
    """

    def __init__(self, doi_list: list, regex_dict: dict, njobs: int = 1):
        """

        Args:
            doi_list (list): list of DOI strings
            regex_dict (dict): dictionary with compiled python regular expressions
            njobs (int): maximal number of workers (default 1)

        """
        self.doi_list = doi_list
        self.regex_dict = regex_dict
        self.njobs = njobs
        self.result_list = []
        self.error_dict = defaultdict(list)
        self._empty_results_dict = dict([(k, False) for k, __ in regex_dict.items()])

        if isnotebook():
            logger.error('Requests HTML will not work in a notebook! Hence our parsing also will not work in a notebook!')

    @staticmethod
    def _parse_string(string: str, regex_dict: dict) -> dict:
        """
        Parses a string for the regular expression provided in regex_dict
        and returns a dictionary with the results.

        Args:
            string (str):
            regex_dict (dict):

        Returns:
            dictionary with booleans as values and regex_dict keys as keys

        """
        results_dict = {}
        for k, v in regex_dict.items():
            regex_result = re.findall(v, string)
            if len(regex_result) > 0:
                results_dict[k] = True
            else:
                results_dict[k] = False

        return results_dict

    def _parse_doi(self, doi: str) -> dict:
        """

        ToDo:
            - The step when we simply take the URL key is the biggest approximation
            - The error catching needs to be improved

        Args:
            doi (str): a valid DOI string

        Returns:
            dictionary with booleans as values and regex_dict keys as keys

        """
        try:
            url = works.doi(doi)['URL']
        except KeyError:
            logger.error('Could not find a URL for this DOI')
            self.error_dict['url_not_found'].append(doi)
            results_dict = self._empty_results_dict
            results_dict['doi'] = doi
            return results_dict
        else:
            try:
                session = HTMLSession()
                r = session.get(url)
                _ = r.html.render(timeout=0, sleep=10)
                text = r.html.full_text
                results_dict = DoiParser._parse_string(text, self.regex_dict)
                r.close()
                session.close()

            except Exception:
                self.error_dict['parsing_error'].append(doi)
                results_dict = self._empty_results_dict
                results_dict['doi'] = doi
                return results_dict
            else:
                return results_dict

    def parse(self) -> pd.DataFrame:
        """
        Run parsing for this DOI parser object.

        Returns:
            pd.DataFrame with parsing results.

        """
        with concurrent.futures.ProcessPoolExecutor(
                max_workers=self.njobs) as executor:
            for result_dict in tqdm(
                    executor.map(self._parse_doi,
                                 self.doi_list),
                total=len(self.doi_list)):
                self.result_list.append(result_dict)

        return pd.DataFrame(self.result_list)