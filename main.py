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

@dataclass
class AirQuality:
    station: str
    datetime: str
    SO2_1h: float
    SO2_24h: float
    NO2_1h: float
    O3_1h: float
    O3_8h: float
    PM10_24h: float
    PM25_1h: float
    CO_8h: float

def make_request(url):
    with httpx.Client() as client:
        response = client.get(url)
        html = HTMLParser(response.text)
    return html

def parse_air_quality(html):
    station = html.css_first('div.box-detail__heading__inner > h1:nth-child(2) > strong:nth-child(1)').text()
    items = html.css('div.respons-table:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr')
    for index, item in enumerate(items):
        if index == 0:
            continue
        else:
            new_item = AirQuality(
                datetime = item.css_first('.text-left.pl40').text(),
                NO2_1h = item.css_first('.z2').text(),

            )



if __name__ == '__main__':
    html = make_request(urls[0])
    parse_air_quality(html)