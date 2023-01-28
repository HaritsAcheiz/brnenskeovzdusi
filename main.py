import httpx
from selectolax.parser import HTMLParser
import pandas as pd
import time

def make_request(url):
    with httpx.Client() as client:
        response = client.get(url)
    return response

def checker(x):
    if x != None:
        result = x.text()
    else:
        result = None
    return result

def parse_air_quality(response):
    html = HTMLParser(response.text)
    try:
        station = html.css_first('div.box-detail__heading__inner > h1 > strong').text()
    except AttributeError:
        station = html.css_first('div.grid-3:nth-child(2) > h1 > strong').text()
    items = html.css('div.respons-table:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr')
    headers = []
    datas = {'station': station, 'air_quality':list()}
    for index, item in enumerate(items):
        if index == 0:
           header_objects = item.css('th')
           for header in header_objects:
               headers.append(header.text().replace('\t','').replace('\n',''))
        else:
            new_item = dict()
            for i,header in enumerate(headers,1):
                new_item[f'{header}'] = item.css_first(f'td:nth-child({i})').text()
                datas['air_quality'].append(new_item)
    return datas

def get_data(url):
    print(f'getting data from {url}')
    html = make_request(url)
    result = parse_air_quality(html)
    datas = pd.DataFrame(result['air_quality'])
    datas.to_csv(f"{result['station']} {datas.iloc[-1][0].split(':')[0]}.csv")

def main():
    urls = ['https://www.brnenskeovzdusi.cz/brno-detska-nemocnice/',
            'https://www.brnenskeovzdusi.cz/brno-svatoplukova/',
            'https://www.brnenskeovzdusi.cz/brno-lany/',
            'https://www.brnenskeovzdusi.cz/brno-arboretum/',
            'https://www.brnenskeovzdusi.cz/brno-vystaviste/',
            'https://www.brnenskeovzdusi.cz/brno-masna/',
            'https://www.brnenskeovzdusi.cz/brno-lisen/',
            'https://www.brnenskeovzdusi.cz/brno-uvoz/',
            'https://www.brnenskeovzdusi.cz/brno-turany/']
    [get_data(url) for url in urls]

if __name__ == '__main__':
    start = time.perf_counter()
    main()
    print(f'processing_time: {str(time.perf_counter()-start)} second(s)')