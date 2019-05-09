from parse_doi import doi_parser
import pandas as pd
import re

df = pd.read_csv('/home/kevin/Documents/uni/EPFL/master_thesis/dimensionality/metal_channels_in_ccsd.csv')

doi_list = df['doi_paper'].dropna().to_list()

uv_regex_list = ['uv', 'uv-vis', 'vis']
uv_regex = re.compile('|'.join(uv_regex_list), re.IGNORECASE)

photo_regex_list = ['photo', 'absorp', 'light', 'lumin']
photo_regex = re.compile('|'.join(photo_regex_list), re.IGNORECASE)

electronic_regex_list = ['electronic', 'conduc']
electronic_regex = re.compile('|'.join(electronic_regex_list), re.IGNORECASE)

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
df_parsed = dp.parse()

df_parsed.to_csv('parsed_full_text.csv', index=False)
