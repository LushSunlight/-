import requests
import re
from bs4 import BeautifulSoup
from bs4 import NavigableString
import datetime
import pandas as pd
import platform
import locale
import os

# This dataframe contains 3 columns. The first column is 'date',
# the second column is the news headline of that date and the third column
# is the full content.
dataframe = pd.DataFrame(columns = ['date','headline','content'])
dataframe.head()
filename = '2020news.csv'
locale.setlocale(locale.LC_CTYPE,'chinese')

# Traverse the dates.
# year = input('year:')
# begin = datetime.date(int(year), 1, 1)
# end = datetime.date(int(year), 12, 31)
begin = datetime.date(2017, 1, 7)
end = datetime.date(2017, 12, 31)

d = begin
delta = datetime.timedelta(days=1)


def tag_filter_headline(tag):
    flag_1 = (tag.name == 'li') and not tag.has_attr('class')
    flag_2 = isinstance(tag.next_element, NavigableString)
    return flag_1 and flag_2


def tag_filter_content(tag):
    flag_1 = (tag.name == 'p') and not tag.has_attr('class')
    flag_2 = isinstance(tag.next_element, NavigableString)
    return flag_1 and flag_2


while d <= end:
    # Get the source code of that day.
    sysstr = platform.system()
    if (sysstr == 'Linux'):
        url_d = d.strftime('http://mrxwlb.com/%Y年%-m月%-d日新闻联播文字版')  # This only works on Unix!
    elif (sysstr == 'Windows'):
        url_d = d.strftime('http://mrxwlb.com/%Y年%#m月%#d日新闻联播文字版')  # Windows users use this line instead.
    r = requests.get(url_d)

    # Making the source code text into soup!
    soup = BeautifulSoup(r.text, features="lxml")
    outlines_raw = soup.find_all(tag_filter_headline)
    full_texts_raw = soup.find_all(tag_filter_content)

    outlines = ""
    full_texts = ""

    for outline in list(outlines_raw):
        try:
            outlines = ",".join((outlines, outline.string))
        except Exception as e:
            pass
        continue

    outlines = outlines.strip(',')

    for full_text in list(full_texts_raw):
        try:
            full_texts = "\n".join((full_texts, full_text.string))
        except Exception as e:
            pass
        continue

    full_texts = full_texts.strip('\n')
    # new_full_texts = ''
    # for i in range(len(list(outlines_raw))):
    #     new_full_texts += list(full_texts_raw)[i].string
    #     new_full_texts += '\n'

    df_new = pd.DataFrame([[d, outlines, full_texts]], columns=['date', 'headline', 'content'])
    dataframe = pd.concat([dataframe, df_new], ignore_index=True)
    # dataframe = dataframe.append(df_new, ignore_index=True)
    if not os.path.isdir('./XWLB_txts'):
        os.mkdir('./XWLB_txts')
    f = open('./XWLB_txts/' + str(d).replace('-', '') + '.txt', mode='w', encoding='utf8')
    f.write(full_texts)
    f.close()
    # dataframe.to_csv(filename, encoding='utf_8_sig')
    dataframe.head()

    d += delta

