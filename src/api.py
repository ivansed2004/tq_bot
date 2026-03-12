import aiohttp


async def api_remote_call(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()