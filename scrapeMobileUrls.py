import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

df = pd.read_excel('crawlPages.xlsx', index_col=0)
# print(df)

root_url = "https://phonedb.net"

mobileUrlList = []

for i in df.itertuples():
    url = root_url+str(i[1])
    response = requests.get(url=url)
    html = BeautifulSoup(response.text, 'html.parser')
    url_list = html.css.select('.content_block_title > a')
    print(url_list)
    for url in url_list:
        mobileUrlList.append(url['href'])

mobileUrlDF = pd.DataFrame(mobileUrlList)

mobileUrlDF.to_excel('mobileUrlsList.xlsx')
