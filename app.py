import aiohttp
import asyncio
from bs4 import BeautifulSoup as bs
from logging import getLogger, basicConfig, DEBUG


FORMAT = '%(asctime)s : %(levelname)s : %(name)s : %(message)s'
logger = getLogger()
basicConfig(level=DEBUG, format=FORMAT)


async def main():
    async with aiohttp.ClientSession() as session:
        responce = await session.get('https://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString=0101500000324000488')
        if responce.ok:
            text = await responce.text()
            soup = bs(text, 'html.parser')
            links = soup.find_all('a')
            print(links)


if __name__ == '__main__':
    logger.debug("Start project")
    asyncio.run(main())