import httpx
import asyncio
from selectolax.parser import HTMLParser
from dataclasses import dataclass, asdict

urls = ['https://www.brnenskeovzdusi.cz/brno-detska-nemocnice/',
        'https://www.brnenskeovzdusi.cz/brno-arboretum/',
        'https://www.brnenskeovzdusi.cz/brno-lany/',
        'https://www.brnenskeovzdusi.cz/brno-svatoplukova/',
        'https://www.brnenskeovzdusi.cz/brno-vystaviste/',
        'https://www.brnenskeovzdusi.cz/brno-masna/',
        'https://www.brnenskeovzdusi.cz/brno-lisen/',
        'https://www.brnenskeovzdusi.cz/brno-uvoz/',
        'https://www.brnenskeovzdusi.cz/brno-turany/']

# @dataclass
# class AirQuality:
#     station: str
#     datetime: str
#     SO2_1h: float
#     SO2_24h: float
#     NO2_1h: float
#     O3_1h: float
#     O3_8h: float
#     PM10_1h: float
#     PM10_24h: float
#     PM25_1h: float
#     CO_8h: float

def make_request(url):
    with httpx.Client() as client:
        response = client.get(url)
        html = HTMLParser(response.text)
    return html

def checker(x):
    if x != None:
        result = x.text()
    else:
        result = None
    return result

def parse_air_quality(html):
    station = html.css_first('div.box-detail__heading__inner > h1:nth-child(2) > strong:nth-child(1)').text()
    items = html.css('div.respons-table:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr')
    headers = []
    datas = []
    for index, item in enumerate(items):
        if index == 0:
           header_objects = item.css('th')
           for header in header_objects:
               headers.append(header.text().replace('\t','').replace('\n',''))
        else:
            new_item = dict()
            for i,header in enumerate(headers,1):
                new_item[f'{header}'] = item.css_first(f'td:nth-child({i})').text()
                datas.append(new_item)
    return datas

if __name__ == '__main__':
    html = make_request(urls[0])
    result = parse_air_quality(html)
    print(result)