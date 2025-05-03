import asyncio
import logging
from langchain_openai import AzureChatOpenAI
from pydantic import BaseModel, SecretStr
from browser_use import ActionResult, Agent, Controller
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext, BrowserContextConfig

from src.constants.config import DirConfig, BasicConfig, ApiKeyConfig
from src.utils.safe_utils import generate_password

logger = logging.getLogger(__name__)
controller = Controller()


browser = Browser(
    config=BrowserConfig(
        # chrome_instance_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        disable_security=False,
    )
)
config = BrowserContextConfig(
    cookies_file= DirConfig.cookies_dir.joinpath("x.com_cookies.json").as_posix(),
    wait_for_network_idle_page_load_time=3.0,
    browser_window_size={"width": 1280, "height": 1100},
    locale="en-US",
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
)
context = BrowserContext(browser=browser, config=config)


async def main():
    password =generate_password()
    tasks = [
        f"""
        Visit https://vimeo.com/ and register an account with the following information if not already registered:
        - username candidates: {BasicConfig.social_media_usernames}
        - email: {BasicConfig.gmail_account}
        - password: {password}
        - phone number: {BasicConfig.mobile_number}
        - date of birth: {BasicConfig.date_of_birth}
        Go to gmail.com and verify the email address if needed.
    """
    ]
    model = AzureChatOpenAI(
        model="gpt-4o",
        api_version="2024-10-21",
        azure_endpoint=ApiKeyConfig.llm_base_url,
        api_key=SecretStr(ApiKeyConfig.llm_api_key),
        temperature=0.0,
    )

    agents = []
    for task in tasks:
        agent = Agent(
            task=task,
            llm=model,
            controller=controller,
            browser_context=context,
            save_conversation_path="works/logs",
            use_vision=True,
        )
        agents.append(agent)

    await asyncio.gather(*[agent.run() for agent in agents])

