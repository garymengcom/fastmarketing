import asyncio
import json
import logging
from typing import List
from browser_use import Agent, Controller
from browser_use.agent.views import ActionResult
from browser_use.browser.context import BrowserContext

from src.constants.config import BasicConfig, DirConfig
from src.crud.directory_website_crud import DirectoryWebsiteCrud
from src.schemas import DirectoryWebsiteOut, DirectoryWebsiteIn
from src.utils.browswer_utils import get_browser_context
from src.utils.llm_utils import get_llm
from src.utils.safe_utils import generate_password
from src.utils.upload_utils import upload_file

logger = logging.getLogger(__name__)
controller = Controller()


@controller.action("Update directory website", param_model=DirectoryWebsiteIn)
def update_directory_website(d: DirectoryWebsiteIn):
    DirectoryWebsiteCrud.update_domain(d)
    return "Saved career to file"


@controller.action("Get all directory websites")
def get_all_directory_websites() -> List[DirectoryWebsiteOut]:
    domains = DirectoryWebsiteCrud.get_domains()
    return [DirectoryWebsiteOut.model_validate(d) for d in domains]

@controller.action('Read json information')
def read_json(path: str) -> dict:
    with open(path, 'r') as f:
        return json.loads(f.read())

@controller.action(
    'Upload rectangle logo to element - call this function to upload if element is not found, try with different index of the same upload element',
)
async def upload_rectangle_logo(index: int, browser: BrowserContext, upload_path: str):
    return await upload_file(index, browser, upload_path)

@controller.action(
    'Upload square logo to element - call this function to upload if element is not found, try with different index of the same upload element',
)
async def upload_square_logo(index: int, browser: BrowserContext, upload_path: str):
    return await upload_file(index, browser, upload_path)

@controller.action(
    'Upload favicon to element - call this function to upload if element is not found, try with different index of the same upload element',
)
async def upload_favicon(index: int, browser: BrowserContext, upload_path: str):
    return await upload_file(index, browser, upload_path)

@controller.action(
    'Upload screenshots to element - call this function to upload if element is not found, try with different index of the same upload element',
)
async def upload_screenshots(index: int, browser: BrowserContext, upload_paths: List[str]):
    for upload_path in upload_paths:
        try:
            await upload_file(index, browser, upload_path)
        except Exception as e:
            logger.error(f"Error uploading favicon: {e}")
            return ActionResult(error=f"Error uploading favicon: {e}")
    return ActionResult(extracted_content="Uploaded screenshots successfully")

project_dir = DirConfig.basic_info_dir / "employer-hirelala"

async def main():
    """Get the list of all directory websites using the action "Get all directory websites"."""
    task = f"""
1. Visit: https://www.ontoplist.com/
2. Try to submit my website to the directory with following information:
- website basic information in json file path: {project_dir / "employer.hirelala.com.json"}

3. Upload the following files if required, else skip:
- website favicon file path: {project_dir / "assets/hirelala-favicon.png"}
- website rectangle logo file path: {project_dir / "assets/hirelala-logo-rectangle.png"}
- website square logo file path: {project_dir / "assets/hirelala-logo-square.png"}
- website screenshot 1 file path: {project_dir / "assets/screenshot1.png"}
- website screenshot 2 file path: {project_dir / "assets/screenshot2.png"}
- website screenshot 3 file path: {project_dir / "assets/screenshot3.png"}

4. If login is required, attempt to create a user profile using the following fields:
- Email: {BasicConfig.gmail_account}
- Password: {BasicConfig.signup_password}
- Phone: {BasicConfig.mobile_number}
- Date of Birth: {BasicConfig.date_of_birth}

5. For each attempt, record:
- id: ID of the directory site  
- domain: Domain of the site  
- account: The username or email used. Set to empty string if not applicable
- password: The password used. Set to empty string if not applicable
- status: "created" or "created_failed" or "no_signup"
- failed_reason: Reason for failure (if any)

Notes:
- Mark as failed if got the error from LLM model, e.g., ResponsibleAIPolicyViolation, the reason is "error from LLM model"
- Mark as failed if it is not free to submit, the reason is "not free to submit"
- Save the results using "Update directory website" action.
- Auto fill the form if the it not in basic information with the most relevant information.
    """

    agent = Agent(
        task=task,
        llm=get_llm(),
        controller=controller,
        browser_context=get_browser_context(),
        save_conversation_path="build/logs",
        use_vision=True,
    )

    await asyncio.gather(agent.run())


if __name__ == '__main__':
    asyncio.run(main())

