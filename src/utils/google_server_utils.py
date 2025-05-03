import ssl
from typing import Dict, Any

import aiohttp
import certifi

from src.constants.config import ApiKeyConfig
from src.schemas import GoogleSearchRequest


async def google_search(request: GoogleSearchRequest) -> Dict[str, Any]:
    url = "https://google.serper.dev/search"

    payload = request.model_dump(exclude_none=True)
    headers = {
        'X-API-KEY': ApiKeyConfig.serper_api_key,
        'Content-Type': 'application/json'
    }

    ssl_context = ssl.create_default_context(cafile=certifi.where())
    connector = aiohttp.TCPConnector(ssl=ssl_context)

    async with aiohttp.ClientSession(connector=connector) as session:
        async with session.post(url, headers=headers, json=payload) as response:
            response.raise_for_status()
            return await response.json()