from typing import Any, List
import aiohttp
import asyncio
import time

class HttpCallerError(Exception):
    pass

class HttpCaller:
    def __init__(self):
        self.urls = [f"https://jsonplaceholder.typicode.com/todos/{i}" for i in range(1, 101)]
        self.client = None

    async def __aenter__(self):
        timeout = aiohttp.ClientTimeout(total=10)
        self.client = aiohttp.ClientSession(timeout=timeout)
        return self

    async def __aexit__(self, exc_type: type, exc: Exception, tb: object):
        if self.client:
            await self.client.close()
            self.client = None

    async def request(self, url: str) -> Any:
        if not self.client:
            raise HttpCallerError("ClientSession is not initialized. Use 'async with HttpCaller()'.")
        try:
            async with self.client.get(url) as response:
                if response.status != 200:
                    raise HttpCallerError(f"Failed to fetch {url}, status: {response.status}")
                return await response.json() 
        except aiohttp.ClientError as e:
            raise HttpCallerError(f"Request to {url} failed: {str(e)}")

    async def get_data(self) -> List[Any]:
        semaphore = asyncio.Semaphore(10)  # Не больше 10 запросов одновременно
        async def limited_request(url: str) -> Any:
            async with semaphore:
                return await self.request(url)
        tasks = [limited_request(url) for url in self.urls]
        return await asyncio.gather(*tasks, return_exceptions=True)  # Возвращает и успехи, и ошибки

async def main():
    start = time.time()
    try:
        async with HttpCaller() as caller:
            data = await caller.get_data()
            successes = [d for d in data if not isinstance(d, Exception)]
            errors = [d for d in data if isinstance(d, Exception)]
            print(f"Fetched {len(successes)} responses, errors: {len(errors)}")
    except HttpCallerError as e:
        print(f"Critical error: {e}")
    finally:
        end = time.time()
        print(f"Total time: {end - start:.2f} seconds.")

asyncio.run(main())