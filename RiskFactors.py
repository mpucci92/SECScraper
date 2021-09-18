import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
from lxml import etree
import codecs
import datetime

files = []
text = []
date = []


def riskFactors(full_file_path):

    for filepath in full_file_path:

        file = codecs.open(filepath, 'r', "utf-8")
        raw = file.read()

        try:
            dt_string = BeautifulSoup(raw[0:1000], 'lxml').find('acceptance-datetime').text.split('\n')[0][0:8]
            format_ = "%Y%m%d"
            dt_object = datetime.datetime.strptime(dt_string, format_)
            date.append(dt_object)
        except Exception as e:
            date.append(None)

        doc_start_pattern = re.compile(r'<DOCUMENT>')
        doc_end_pattern = re.compile(r'</DOCUMENT>')

        # Regex to find <TYPE> tag prceeding any characters, terminating at new line
        type_pattern = re.compile(r'<TYPE>[^\n]+')

        doc_start_is = [x.end() for x in doc_start_pattern.finditer(raw)]
        doc_end_is = [x.start() for x in doc_end_pattern.finditer(raw)]

        ### Type filter is interesting, it looks for <TYPE> with Not flag as new line, ie terminare there, with + sign
        ### to look for any char afterwards until new line \n. This will give us <TYPE> followed Section Name like '10-K' or '10-Q'
        ### Once we have have this, it returns String Array, below line will with find content after <TYPE> ie, '10-K' or '10-Q'
        ### as section names
        doc_types = [x[len('<TYPE>'):] for x in type_pattern.findall(raw)]

        document = {}

        # Create a loop to go through each section type and save only the 10-K section in the dictionary
        for doc_type, doc_start, doc_end in zip(doc_types, doc_start_is, doc_end_is):
            if doc_type == '10-Q':
                document[doc_type] = raw[doc_start:doc_end]
                doc_type = doc_type

            elif doc_type == '10-K':
                document[doc_type] = raw[doc_start:doc_end]
                doc_type = doc_type

        # Write the regex

        if '10-Q' in doc_types:
            regex = re.compile(r'((>Item|ITEM)(\s|&#160;|&nbsp;)(1A|1B|2)\.{0,1})|(ITEM\s(1A|1B|2))')

            # Use finditer to math the regex
            matches = regex.finditer(document['10-Q'])

            regIndex = 'Item 2.'

            # Write a for loop to print the matches
            for match in matches:
                if match.group() == '>Item 1B.':
                    regIndex = 'Item 1B.'

            if regIndex == 'Item 1B.':
                regex = re.compile(r'((>Item|ITEM)(\s|&#160;|&nbsp;)(1A|1B)\.{0,1})|(ITEM\s(1A|1B))')
                matches = regex.finditer(document['10-Q'])
            else:
                regex = re.compile(r'((>Item|ITEM)(\s|&#160;|&nbsp;)(1A|2)\.{0,1})|(ITEM\s(1A|2))')
                matches = regex.finditer(document['10-Q'])

            matches = regex.finditer(document['10-Q'])

            # Create the dataframe
            try:
                df = pd.DataFrame([(x.group(), x.start(), x.end()) for x in matches])

                df.columns = ['item', 'start', 'end']
                df['item'] = df.item.str.lower()
            except Exception as e:
                print(filepath)
                continue

            # Get rid of unnesesary charcters from the dataframe
            df.replace('&#160;', ' ', regex=True, inplace=True)
            df.replace('&nbsp;', ' ', regex=True, inplace=True)
            df.replace(' ', '', regex=True, inplace=True)
            df.replace('\.', '', regex=True, inplace=True)
            df.replace('>', '', regex=True, inplace=True)

            # Drop duplicates
            pos_dat = df.sort_values('start', ascending=True).drop_duplicates(subset=['item'], keep='last')
            pos_dat.set_index('item', inplace=True)

            if regIndex == 'Item 2.':
                try:
                    item_1a_raw = document['10-Q'][pos_dat['start'].loc['item1a']:pos_dat['start'].loc['item2']]
                except Exception as e:
                    print(filepath)
                    item_1a_raw = ''

            else:
                try:
                    item_1a_raw = document['10-Q'][pos_dat['start'].loc['item1a']:pos_dat['start'].loc['item1b']]
                except Exception as e:
                    print(filepath)
                    item_1a_raw = ''

            item_1a_content = BeautifulSoup(item_1a_raw, 'lxml')
            item_1a_content = item_1a_content.text.replace('\xa0', " ")

        else:
            regex = re.compile(r'((>Item|ITEM)(\s|&#160;|&nbsp;)(1A|1B|2)\.{0,1})|(ITEM\s(1A|1B|2))')

            # Use finditer to math the regex
            matches = regex.finditer(document['10-K'])

            regIndex = 'Item 2.'

            # Write a for loop to print the matches
            for match in matches:
                if match.group() == '>Item 1B.':
                    regIndex = 'Item 1B.'

            if regIndex == 'Item 1B.':
                regex = re.compile(r'((>Item|ITEM)(\s|&#160;|&nbsp;)(1A|1B)\.{0,1})|(ITEM\s(1A|1B))')
                matches = regex.finditer(document['10-K'])
            else:
                regex = re.compile(r'((>Item|ITEM)(\s|&#160;|&nbsp;)(1A|2)\.{0,1})|(ITEM\s(1A|2))')
                matches = regex.finditer(document['10-K'])

            matches = regex.finditer(document['10-K'])

            # Create the dataframe
            try:
                df = pd.DataFrame([(x.group(), x.start(), x.end()) for x in matches])

                df.columns = ['item', 'start', 'end']
                df['item'] = df.item.str.lower()
            except Exception as e:
                print(filepath)
                continue

            # Get rid of unnesesary charcters from the dataframe
            df.replace('&#160;', ' ', regex=True, inplace=True)
            df.replace('&nbsp;', ' ', regex=True, inplace=True)
            df.replace(' ', '', regex=True, inplace=True)
            df.replace('\.', '', regex=True, inplace=True)
            df.replace('>', '', regex=True, inplace=True)

            # Drop duplicates
            pos_dat = df.sort_values('start', ascending=True).drop_duplicates(subset=['item'], keep='last')
            pos_dat.set_index('item', inplace=True)

            if regIndex == 'Item 2.':
                try:
                    item_1a_raw = document['10-K'][pos_dat['start'].loc['item1a']:pos_dat['start'].loc['item2']]
                except Exception as e:
                    print(filepath)
                    item_1a_raw = ''
            else:
                try:
                    item_1a_raw = document['10-K'][pos_dat['start'].loc['item1a']:pos_dat['start'].loc['item1b']]
                except Exception as e:
                    print(filepath)
                    item_1a_raw = ''

            item_1a_content = BeautifulSoup(item_1a_raw, 'lxml')
            item_1a_content = item_1a_content.text.replace('\xa0', " ")

        if len(item_1a_content) < 1:
            text.append(None)
            files.append(filepath)
        else:
            text.append(item_1a_content)
            files.append(filepath)


def riskFactorDataframe(files,text,date):

    df = pd.DataFrame()
    df['timestamp'] = date
    df['file'] = files
    df['text'] = text

    ticker_article = {'tickers': [], 'article_type': []}

    for i in range(len(df)):
        ticker_of_choice = df.file.iloc[i].split('\\')[-4]
        type_of_article = df.file.iloc[i].split('\\')[-3]
        ticker_article['tickers'].append(ticker_of_choice)
        ticker_article['article_type'].append(type_of_article)

    df['tickers'] = (ticker_article['tickers'])
    df['article_type'] = (ticker_article['article_type'])

    return df

