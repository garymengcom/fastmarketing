"""
Goal: Searches for job listings, evaluates relevance based on a CV, and applies

@dev You need to add OPENAI_API_KEY to your environment variables.
Also you have to install PyPDF2 to read pdf files: pip install PyPDF2
"""

import asyncio
import csv
import logging
import os
import sys
from pathlib import Path
from typing import Optional

from src.constants.config import DirConfig, BasicConfig, LlmConfig
from src.utils.safe_utils import generate_password

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from pydantic import BaseModel, SecretStr

from browser_use import ActionResult, Agent, Controller
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext, BrowserContextConfig



logger = logging.getLogger(__name__)
controller = Controller()


class SocialMediaAccount(BaseModel):
    username: str
    email: str
    password: str


@controller.action("Save social media account to local", param_model=SocialMediaAccount)
def save_account(account: SocialMediaAccount):
    with open(DirConfig.accounts_dir / "accounts.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([account.username, account.email, account.password])

    return "Saved career to file"


browser = Browser(
    config=BrowserConfig(
        # chrome_instance_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        disable_security=False,
    )
)
config = BrowserContextConfig(
    # cookies_file="path/to/cookies.json",
    wait_for_network_idle_page_load_time=3.0,
    browser_window_size={"width": 1280, "height": 1100},
    locale="en-US",
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
    # allowed_domains=['google.com', 'wikipedia.org'],
)
context = BrowserContext(browser=browser, config=config)


async def main():
    password =generate_password()
    tasks = [
        f"""
        Visit https://x.com/ and register an account with the following information if not already registered:
        - username candidates: {BasicConfig.social_media_usernames}
        - email: {BasicConfig.gmail_account}
        - password: {password}
        - phone number: {BasicConfig.mobile_number}
        Go to gmail.com and verify the email address if needed.
    """
    ]
    model = AzureChatOpenAI(
        model="gpt-4o",
        api_version="2024-10-21",
        azure_endpoint=LlmConfig.base_url,
        api_key=SecretStr(LlmConfig.api_key),
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

