from app.readers.docs_reader import DocsReader
from loguru import logger
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlparse


class UrlReader(DocsReader):

    def __init__(self, source):
        self.source = source
        self.visited_url = set()


    def load(self):
        out = []
        is_scan_child = self.source.get("is_scan_child", False)
        url_queue = [] #defining a queue to capture sub_urls
        if "path" in self.source:
            urls = self.source["path"]
            for url in urls:
                url_queue.append(url)

            base_domain = urlparse(urls[0]).netloc

            print(url_queue)
            while url_queue :
                url = url_queue.pop(0)
                logger.info(f"scanning url {url}")
                if url in self.visited_url:
                    continue
                logger.info(f"urls in queue {len(url_queue)} visited {len(self.visited_url)}")
                self.visited_url.add(url)
                try:
                    response = requests.get(url, headers=self.source.get("headers", {}))

                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        if is_scan_child :
                            for a in soup.find_all('a', href = True) :
                                absolute_url = urljoin(url, a['href'])
                                if absolute_url not in self.visited_url and  urlparse(absolute_url).netloc == base_domain and absolute_url not in url_queue:
                                    url_queue.append(absolute_url)
                        tag = soup.body
                        text = ''.join(list(tag.strings)[:-1])
                        metadata = {
                            "path": url
                        }
                        out.append({"content": str(text), "metadata": metadata})
                    else:
                        logger.critical(f"Failed to retrieve content, status code: {response.status_code}")
                except Exception as e:
                    logger.error(e)
        return out