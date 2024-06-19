import asyncio
import aiohttp
import time
import argparse
from statistics import mean, stdev

async def fetch(session, url):
    """
    Asynchronously fetches a URL and records latency.
    """
    try:
        async with session.get(url) as response:
            latency = response.headers.get('X-Response-Time', 0)
            return latency, response.status
    except Exception as e:
        return 0, 500

async def worker(queue, session, stats):
    """
    A coroutine that gets URLs from a queue and processes them.
    """
    while True:
        url = await queue.get()
        if url is None:
            break

        start_time = time.time()
        latency, status = await fetch(session, url)
        end_time = time.time()

        duration = end_time - start_time
        stats.append((duration, status))

        queue.task_done()

async def main(url, qps, duration):
    queue = asyncio.Queue()
    stats = []

    async with aiohttp.ClientSession() as session:
        workers = [asyncio.create_task(worker(queue, session, stats)) for _ in range(qps)]

        end_time = time.time() + duration
        while time.time() < end_time:
            await queue.put(url)
            await asyncio.sleep(1 / qps)

        for _ in range(qps):
            await queue.put(None)

        await asyncio.gather(*workers)

    latencies = [stat[0] for stat in stats if stat[1] == 200]
    error_count = sum(1 for stat in stats if stat[1] != 200)

    if latencies:
        print(f"Average Latency: {mean(latencies):.2f}s")
        print(f"Latency Standard Deviation: {stdev(latencies):.2f}s")
    else:
        print("No successful requests.")

    print(f"Total Requests: {len(stats)}")
    print(f"Errors: {error_count}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="HTTP Load-Testing Tool")
    parser.add_argument('url', type=str, help='URL to test. eg: http://example.com')
    parser.add_argument('--qps', type=int, default=1, help='Queries per second')
    parser.add_argument('--duration', type=int, default=10, help='Duration of the test in seconds')

    args = parser.parse_args()

    asyncio.run(main(args.url, args.qps, args.duration))
