import asyncio
import logging
from browser_use import Agent, Controller

from src.crud.wordpress_website_crud import WordpressWebsiteCrud
from src.schemas import WordpressWebsiteIn
from src.utils.browswer_utils import get_browser_context
from src.utils.llm_utils import get_llm

logger = logging.getLogger(__name__)
controller = Controller()


@controller.action("Update wordpress website", param_model=WordpressWebsiteIn)
def update_wordpress_website(d: WordpressWebsiteIn):
    WordpressWebsiteCrud.update_domain(d)
    return "Saved career to file"


async def main():
    last_id = 0
    batch_size = 2
    browser_contexts = [get_browser_context() for _ in range(batch_size)]
    while True:
        sites = WordpressWebsiteCrud.get_domains(last_id, batch_size)
        if not sites:
            break

        tasks = [f"""
    1. Visit domain "{site.domain}".
    2. Accept all cookie dialog or close it if popup appears.
    3. Choose a post that mostly can be commented and click on it.
    4. Continue if and only if the website can be left comment and support to comment with website url.
    5. Leave a comment on the post with the following information:
        - Name: Hirelala
        - Email: hirelala.com@gmail.com
        - Website url: https://employer.hirelala.com
        - Comment: Base on the post title, write a comment that is relevant to the post.
    6. Once finish, save the status to database using action "Update wordpress website" with the following information then quit:
        - id: {site.id}
        - status: "submitted" or "failed"
        - failed_reason: <The reason if failed>
    
    Note: Only 1 try is enough, if failed, return failure.
        """ for site in sites]

        agents = []
        for i, task in enumerate(tasks):
            agents.append(Agent(
                task=task,
                llm=get_llm(),
                controller=controller,
                browser_context=browser_contexts[i % batch_size],
                save_conversation_path="build/logs",
                use_vision=False,
                max_failures=1,
                max_actions_per_step=1,
            ))

        await asyncio.gather(*[agent.run(max_steps=10) for agent in agents])
        last_id = sites[-1].id

    for browser_context in browser_contexts:
        await browser_context.close()


if __name__ == '__main__':
    asyncio.run(main())

