import argparse
import asyncio
import time
from aiohttp import ClientSession
from tqdm.asyncio import tqdm
from statistics import mean, stdev
from urllib.parse import urlparse

async def fetch(session, url):
    """
    Fetch a URL using aiohttp session and return the latency and status code.
    """
    try:
        start_time = time.time()
        async with session.get(url) as response:
            latency = time.time() - start_time
            return latency, response.status
    except Exception as e:
        return 0, str(e)

async def worker(queue, session, stats, pbar):
    """
    A coroutine that gets URLs from a queue and processes them.
    """
    while True:
        url = await queue.get()
        if url is None:
            break

        latency, status = await fetch(session, url)
        stats.append((latency, status))
        
        pbar.update(1)  # Update the progress bar
        
        queue.task_done()

async def main(url, qps, duration):
    queue = asyncio.Queue()
    stats = []
    total_requests = int(qps * duration)

    async with ClientSession() as session:
        with tqdm(total=total_requests, desc="Progress", unit="req") as pbar:
            workers = [asyncio.create_task(worker(queue, session, stats, pbar)) for _ in range(qps)]

            end_time = time.time() + duration
            while time.time() < end_time:
                await queue.put(url)
                await asyncio.sleep(1 / qps)

            for _ in range(qps):
                await queue.put(None)

            await asyncio.gather(*workers)

    latencies = [stat[0] for stat in stats if stat[1] == 200]
    error_count = sum(1 for stat in stats if stat[1] != 200)
    error_rate = error_count / len(stats)

    if latencies:
        print(f"\nAverage Latency: {mean(latencies):.2f}s")
        print(f"Latency Standard Deviation: {stdev(latencies):.2f}s")
    else:
        print("\nNo successful requests.")

    print(f"Total Requests: {len(stats)}")
    print(f"Error rate: {error_rate * 100:.2f}%")


def validate_url(url):
    """
    Function to validate the input URL.
    """
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        raise argparse.ArgumentTypeError(f"Invalid URL: {url}. Ensure it's a full URL like 'http://example.com'.")
    return url

def validate_qps(input_qps):
    """
    Function to validate the URL.
    """
    try:
        qps = int(input_qps)
        if qps <= 0:
            raise ValueError
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid QPS: {input_qps}. Must be a positive integer.")
    return qps

def validate_duration(input_duration):
    """
    Function to validate the input duration.
    """
    try:
        duration = int(input_duration)
        if duration <= 0:
            raise ValueError
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid duration: {input_duration}. Must be a positive integer.")
    return duration

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="HTTP Load-Testing Tool")
    parser.add_argument('url', type=validate_url, help='URL to test. eg: http://example.com')
    parser.add_argument('--qps', type=validate_qps, default=1, help='Queries per second (default: 1, must be a positive integer)')
    parser.add_argument('--duration', type=validate_duration, default=10, help='Duration of the test in seconds (default: 10, must be a positive integer)')
    
    args = parser.parse_args()

    asyncio.run(main(args.url, args.qps, args.duration))
