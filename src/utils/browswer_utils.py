
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext, BrowserContextConfig, BrowserContextWindowSize

from src.constants.config import DirConfig


def get_browser_context(cookies_file_name: str = None) -> BrowserContext:
    browser = Browser(
        config=BrowserConfig(
            headless=False,
            #browser_binary_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
            #browser_binary_path='/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary',
            #browser_binary_path='/Applications/Firefox.app/Contents/MacOS/firefox',
            # browser_class="firefox",
            disable_security=False,
            extra_browser_args=[
                "--start-maximized",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--disable-component-extensions-with-background-pages",
                # "--remote-debugging-port=9222",
            ]
        )
    )

    cookies_file = DirConfig.cookies_dir.joinpath(f"{cookies_file_name}.json").as_posix() if cookies_file_name else None
    config = BrowserContextConfig(
        cookies_file=cookies_file,
        wait_for_network_idle_page_load_time=3.0,
        browser_window_size=BrowserContextWindowSize(width=1280, height=900),
        locale="en-US",
        #user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    )

    return BrowserContext(browser=browser, config=config)
