import aiohttp
import asyncio
from bs4 import BeautifulSoup
from logging import getLogger, basicConfig, DEBUG

FORMAT = '%(asctime)s : %(levelname)s : %(name)s : %(message)s'
logger = getLogger()
basicConfig(level=DEBUG, format=FORMAT)
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 YaBrowser/24.7.0.0 Safari/537.36',
}
purchases = []


async def open_reg_number_elements(session, element) -> None:
    element_link = element.find_next('a')
    link = f"https://zakupki.gov.ru{element_link.attrs['href']}"
    response = await session.get(link)
    if response.ok:
        text = await response.text()
        soup = BeautifulSoup(text, 'html.parser')
        print([title.text for title in soup.find_all('h2', attrs={'class': 'blockInfo__title'})])
    else:
        logger.debug('Страница недоступна!!!')


async def main():
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        response = await session.get(
            'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString=0101500000324000488')
        if response.ok:
            text = await response.text()
            soup = BeautifulSoup(text, 'html.parser')
            elements = soup.find_all('div', attrs={'class': 'registry-entry__header-mid__number'})
            for element in elements:
                await open_reg_number_elements(session, element)
        else:
            logger.debug('Сайт недоступен!!!')


if __name__ == '__main__':
    logger.debug("Start project")
    asyncio.run(main())
