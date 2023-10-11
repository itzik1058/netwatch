import asyncio
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from playwright.async_api import async_playwright
from sqlalchemy.orm import Session

from netwatch.core.watcher import Watcher
from netwatch.models.facebook import FacebookComment, FacebookPost


class FacebookPageWatcher(Watcher):
    def __init__(self, page: str):
        super().__init__()
        self.page = page

    async def fetch(self, session: Session) -> None:
        post = FacebookPost(page_name=self.page)
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(f"https://www.facebook.com/{self.page}/posts")
            article = await page.wait_for_selector('div[role="article"]')
            if not article:
                raise Exception("post not found")
            links = await article.query_selector_all('a[role="link"]')
            hrefs = await asyncio.gather(
                *(link.get_attribute("href") for link in links)
            )
            post.url = next(filter(lambda href: "posts/" in href, hrefs))
            post.post_id = Path(urlparse(post.url).path).parts[3]
            existing_post = (
                session.query(FacebookPost)
                .filter_by(
                    page_name=self.page,
                    post_id=post.post_id,
                )
                .one_or_none()
            )
            if existing_post is not None:
                post = existing_post
            message = await article.query_selector(
                'div[data-ad-comet-preview="message"]'
            )
            button = await message.query_selector('div[role="button"]')
            if button:
                await button.dispatch_event("click")
            post.content = await message.text_content()
            for comment_article in await article.query_selector_all(
                'div[role="article"]'
            ):
                comment = FacebookComment(post_id=post.id)
                try:
                    comment_links = await article.query_selector_all('a[role="link"]')
                    comment_hrefs = await asyncio.gather(
                        *(link.get_attribute("href") for link in comment_links)
                    )
                    url = next(
                        filter(
                            lambda href: "comment_id" in href and "posts/" not in href,
                            comment_hrefs,
                        )
                    )
                    comment.id = parse_qs(urlparse(url).query)["comment_id"][0]
                except Exception:
                    pass
                text = await comment_article.query_selector('span[lang][dir="auto"]')
                comment.content = await text.text_content()
                existing_comment = (
                    session.query(FacebookComment)
                    .filter_by(post_id=comment.post_id, content=comment.content)
                    .one_or_none()
                )
                if existing_comment is not None:
                    comment = existing_comment
                post.comments.append(comment)
            await browser.close()
        session.add(post)
