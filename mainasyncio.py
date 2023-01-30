import asyncio
import httpx
import pandas as pd
from selectolax.parser import HTMLParser

async def fetch(url):
    async with httpx.AsyncClient(timeout=None) as client:
        return await client.get(url)

def parse_air_quality(page):
    html = HTMLParser(page)
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
    result = pd.DataFrame(datas['air_quality'])
    result.to_csv(f"{datas['station']} {result.iloc[-1][0].split(':')[0]}.csv")

async def main(urls):
    responses = await asyncio.gather(*map(fetch, urls))
    htmls = [response.text for response in responses]
    [parse_air_quality(html) for html in htmls]

if __name__ == '__main__':
    urls = ['https://www.brnenskeovzdusi.cz/brno-detska-nemocnice/',
            'https://www.brnenskeovzdusi.cz/brno-svatoplukova/',
            'https://www.brnenskeovzdusi.cz/brno-lany/',
            'https://www.brnenskeovzdusi.cz/brno-arboretum/',
            'https://www.brnenskeovzdusi.cz/brno-vystaviste/',
            'https://www.brnenskeovzdusi.cz/brno-masna/',
            'https://www.brnenskeovzdusi.cz/brno-lisen/',
            'https://www.brnenskeovzdusi.cz/brno-uvoz/',
            'https://www.brnenskeovzdusi.cz/brno-turany/']
    asyncio.run(main(urls))
