import asyncio
import httpx

async def fetch(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

        print(f"{url} -> {response.status_code}")

async def main():
    await asyncio.gather(
        fetch("https://google.com"),
        fetch("https://github.com"),
        fetch("https://python.org")
    )

asyncio.run(main())