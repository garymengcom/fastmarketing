import asyncio
import csv
import logging
from browser_use import Agent, Controller
from pydantic import BaseModel, Field

from src.constants.config import BasicConfig, DirConfig
from src.utils.browswer_utils import get_browser_context
from src.utils.llm_utils import get_llm

logger = logging.getLogger(__name__)
controller = Controller()

class SubmissionResult(BaseModel):
    url: str
    success: str = Field(default="Success", description="Submission status")
    failure_reason: str = Field(default="", description="Reason for failure, if any")


@controller.action('Read directory websites from file')
def read_directory_websites():
    with open(DirConfig.basic_info_dir / 'directory_websites.csv', 'r') as f:
        return f.read()


@controller.action('Save submission result to file', param_model=SubmissionResult)
def save_submission_result(result: SubmissionResult):
    with open(DirConfig.basic_info_dir / 'directory_websites_results.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([result.url, result.success, result.failure_reason])

    return 'Saved career to file'


async def main():
    tasks = [
        f"""
        1. Read the website url one by one from directory_websites.csv.
        2. Visit the website and register an account with the following information if not already registered:
        - email: {BasicConfig.gmail_account}
        - password: {BasicConfig.signup_password}
        - phone number: {BasicConfig.mobile_number}
        - date of birth: {BasicConfig.date_of_birth}
        - gender: {BasicConfig.gender}
        3. Submit the following information to the website:
        - website url: {BasicConfig.website_homepage} 
        - website title: {BasicConfig.website_title}
        - website description: {BasicConfig.website_description}
        Don't retry if the submission fails.
        4. Save the submission result to local file directory_websites_results.csv.
    """
    ]
    agents = []
    for task in tasks:
        agent = Agent(
            task=task,
            llm=get_llm(),
            controller=controller,
            browser_context=get_browser_context("google-login"),
            save_conversation_path="build/logs",
            use_vision=True,
        )
        agents.append(agent)

    await asyncio.gather(*[agent.run() for agent in agents])


if __name__ == '__main__':
    # Run the main function
    asyncio.run(main())