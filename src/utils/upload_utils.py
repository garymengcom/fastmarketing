from pathlib import Path
import logging
from browser_use import ActionResult
from browser_use.browser.context import BrowserContext

logger = logging.getLogger(__name__)


async def upload_file(index: int, browser: BrowserContext, local_path: str) -> ActionResult:
    try:
        path = Path(local_path).absolute()
    except Exception as e:
        logger.error(f'Error in getting absolute path: {str(e)}')
        return ActionResult(error=f'Invalid file path: {local_path}')
    if not path.exists():
        logger.error(f'File not found at path: {path}')
        return ActionResult(error=f'File not found at path: {path}')

    dom_el = await browser.get_dom_element_by_index(index)
    if dom_el is None:
        return ActionResult(error=f'No element found at index {index}')

    file_upload_dom_el = dom_el.get_file_upload_element()
    if file_upload_dom_el is None:
        logger.info(f'No file upload element found at index {index}')
        return ActionResult(error=f'No file upload element found at index {index}')

    file_upload_el = await browser.get_locate_element(file_upload_dom_el)
    if file_upload_el is None:
        logger.info(f'No file upload element found at index {index}')
        return ActionResult(error=f'No file upload element found at index {index}')

    try:
        await file_upload_el.set_input_files(path)
        msg = f'Successfully uploaded file "{path}" to index {index}'
        logger.info(msg)
        return ActionResult(extracted_content=msg)
    except Exception as e:
        logger.debug(f'Error in set_input_files: {str(e)}')
        return ActionResult(error=f'Failed to upload file to index {index}')