import asyncio
from asyncio import sleep
from urllib.parse import urlparse

from src.crud.career_website_crud import CareerWebsiteCrud
from src.schemas import GoogleSearchRequest, UrlIn
from src.utils.google_server_utils import google_search

async def search(pages):
    for i in range(1, pages + 1):
        r = GoogleSearchRequest(
            q="inurl:career. inurl:careers. OR inurl:/career/ OR inurl:/careers/",
            page=i,
            num=100,
            location="United States",
            gl="us",
            hl="en",
        )
        data = await google_search(r)
        if not data or "organic" not in data or len(data["organic"]) == 0:
            print(f"Page {i} is empty, break.")
            break

        links = [res["link"] for res in data["organic"]]
        urls = [UrlIn(url=url, domain=urlparse(url).netloc) for url in links]
        CareerWebsiteCrud.batch_add(urls)
        print(f"Page {i} done, {len(urls)} domains/urls added.")
        await sleep(1.0)


if __name__ == '__main__':
    asyncio.run(search(10))
    print("All Done")