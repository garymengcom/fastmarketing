import asyncio
from urllib.parse import urlparse

from src.crud.wordpress_website_crud import WordpressWebsiteCrud
from src.schemas import GoogleSearchRequest
from src.utils.google_server_utils import google_search

async def search():
    for i in range(1, 10):
        r = GoogleSearchRequest(
            q="inurl:/wp-content/ OR inurl:/wp-includes/ OR inurl:/wp-admin/",
            page=i,
            num=100,
        )
        data = await google_search(r)
        links = [res["link"] for res in data["organic"]]
        domains = [urlparse(url).netloc for url in links]
        WordpressWebsiteCrud.batch_add_domains(domains)
        print(f"Page {i} done, {len(domains)} domains added.")


if __name__ == '__main__':
    asyncio.run(search())
    print("All Done")