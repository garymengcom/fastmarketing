import asyncio
from browser_use import Agent
from browser_use.controller.service import Controller

from src.constants.config import DirConfig, BasicConfig
from src.utils.browswer_utils import get_browser_context
from src.utils.llm_utils import get_llm

controller = Controller()


async def main():
    task = f"""
        This is a Google login task.
        1. Visit https://accounts.google.com/ and login with the following information:
        - email: {BasicConfig.gmail_account}
        - password: {BasicConfig.gmail_password}
        2. If the login fails, please wait until manually login to the account.
        3. After login, close the browser.
    """

    browser = get_browser_context("google-login")
    agent = Agent(
        task=task,
        llm=get_llm(),
        controller=controller,
        browser_context=browser,
        save_conversation_path=DirConfig.logs_dir.as_posix(),
        use_vision=True,
    )
    await agent.run()
    await browser.close()


if __name__ == '__main__':
    asyncio.run(main())
