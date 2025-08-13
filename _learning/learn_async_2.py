import asyncio
import random

class AsyncFetcher:
    def __init__(self, num_urls: int, workers: int):
        self.start_set = {f"http://example.com/page{i}" for i in range(num_urls)}
        self.semaphore = asyncio.Semaphore(workers)
        self.seen: set[str] = set()
        self.discovered: set[str] = set()

    async def fetch_url(self, url: str) -> tuple[str, list[str]]:
        """Fetch URL and maybe discover new URLs."""
        async with self.semaphore:
            await asyncio.sleep(random.uniform(0.1, 1.0))
            print(f"Fetched {url}")
            new_urls: list[str] = []
            if random.random() < 0.5:
                new = url + "/found"
                print(f"Discovered new URL: {new}")
                new_urls.append(new)
            return url, new_urls

    async def crawler(self) -> list[str]:
        """Crawl starting set, processing tasks as they complete."""
        pending = {asyncio.create_task(self.fetch_url(url)) for url in self.start_set}

        while pending:
            done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)
            for task in done:
                url, new_urls = task.result()

                if url not in self.start_set:
                    self.discovered.add(url)
                self.seen.add(url)

                for new_url in new_urls:
                    if new_url not in self.seen:
                        pending.add(asyncio.create_task(self.fetch_url(new_url)))

        return sorted(self.discovered)

async def main():
    num_urls = 10
    workers = 10
    fetcher = AsyncFetcher(num_urls, workers)
    discovered_urls = await fetcher.crawler()
    print("\nDiscovered URLs:")
    for url in discovered_urls:
        print(url)

if __name__ == "__main__":
    asyncio.run(main())
