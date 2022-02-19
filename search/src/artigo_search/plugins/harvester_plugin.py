import asyncio
import logging
import traceback

from .plugin import Plugin
from aiohttp import ClientSession

logger = logging.getLogger(__name__)


class HarvesterPlugin(Plugin):
    def __init__(self, config=None, name=None):
        super().__init__(config, name)

        self.semaphore = asyncio.Semaphore(5)

    def harvest(self, urls: list) -> list:
        self.urls = set(urls); results = self.init()
        results.sort(key=lambda x: urls.index(x[0]))

        return results

    def init(self):
        try:
            self.loop = asyncio.get_event_loop()
        except:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            self.loop = asyncio.get_event_loop()

        future = asyncio.ensure_future(self.run())

        return self.loop.run_until_complete(future)

    async def run(self):
        tasks = []

        async with ClientSession() as session:
            for url in self.urls:
                task = self.bound_fetch(url, session)
                tasks.append(asyncio.ensure_future(task))

            return [await task for task in tasks]

    async def bound_fetch(self, url, session):
        async with self.semaphore:
           return await self.fetch(url, session)

    async def fetch(self, url, session):
        logger.info(f'[Server] Harvest: {url}')
        
        try:
            async with session.get(url) as response:
                html = await response.read()

                return self.extract(url, html)
        except Exception as error:
            logger.error(f'[Server] Harvest: {repr(error)}')
            logger.error(traceback.format_exc())

            return url, []

    def extract(self, url, response):
        return url, []
