import scrapy
from scrapy.crawler import CrawlerProcess


class XHSHotTopicsSpider(scrapy.Spider):
    # test for git
    name = "xhs_hot_topics"
    allowed_domains = ["xiaohongshu.com"]
    # Entry URL for the Explore/Hot page
    start_urls = ["https://www.xiaohongshu.com/explore"]

    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
        "ROBOTSTXT_OBEY": False,
        "DOWNLOAD_DELAY": 1,
        "COOKIES_ENABLED": True,
        # Enable retry and proxy settings as needed
        "RETRY_ENABLED": True,
        "RETRY_TIMES": 3,
    }

    def parse(self, response):
        self.logger.info(f"Status: {response.status}")
        self.logger.info(response.text[:200])  # 打印前 200 字符看一下页面源
        # Example: extract trending topics from the explore page
        # Note: actual selectors need to be adapted based on the page structure
        for item in response.css("div.hot-list-item"):
            title = item.css("div.title::text").get()
            url = item.css("a::attr(href)").get()
            yield {
                "title": title.strip() if title else None,
                "url": response.urljoin(url) if url else None,
            }

        # If pagination exists, follow next page
        next_page = response.css("a.next::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)


if __name__ == "__main__":
    process = CrawlerProcess(
        settings={
            "FEEDS": {
                "hot_topics.json": {
                    "format": "json",
                    "encoding": "utf8",
                    "indent": 4,
                }
            }
        }
    )
    process.crawl(XHSHotTopicsSpider)
    process.start()  # the script will block here until the crawling is finished

# Instructions:
# 1. Save this file as xhs_hot_spider.py inside a Scrapy project or run directly with dependencies installed.
# 2. Install dependencies: `pip install scrapy`
# 3. Execute: `python xhs_hot_spider.py` to produce hot_topics.json
# 4. Update selectors and pagination logic based on actual XHS page structure.
