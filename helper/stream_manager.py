import aiohttp
from urllib.parse import urljoin
import asyncio
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
from functools import partial, wraps


class StreamManager:
    def __init__(self, host):
        self.host = host
        self.client = aiohttp.ClientSession() 

    @staticmethod
    def run_async(function):
        @wraps(function)
        async def wrapper(*args, **kwargs):
            return await asyncio.get_event_loop().run_in_executor(
                ThreadPoolExecutor(max_workers=multiprocessing.cpu_count() * 5),
                partial(function, *args, **kwargs),
            )

        return wrapper

    async def get_filesize_from_link(self, link):
        try:
            async with self.client() as client:
                res = await client.get(link)
                size = res.headers.get("Content-Length") or 0
                return int(size)
        except:
            return 0
    
    @run_async
    def generate_stream_link(self, msg):
        file_id = msg.id
        chat_id = msg.chat_id
        return urljoin(self.host, f"file/{chat_id}/{file_id}")
    

    
