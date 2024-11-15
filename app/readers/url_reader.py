from app.readers.docs_reader import DocsReader
from loguru import logger
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import Dict
from urllib.parse import urlparse


class UrlReader(DocsReader):

    def __init__(self, source):
        self.source = source
        self.visited_url = set()



    def load(self):
        out = []
        max_depth = self.source.get("depth", 1)
        depth_map: Dict[str, int] = {}
        url_queue = []

        if "path" in self.source:
            urls = self.source["path"]

            for url in urls:
                url_queue.append(url)
                depth_map[url] = 1

            base_domain = urlparse(urls[0]).netloc

            while url_queue :
                url = url_queue.pop(0)

                current_depth = depth_map.get(url, 1)
                logger.info(f"scanning url {url}")
                if url in self.visited_url or current_depth > max_depth:
                    continue
                logger.info(f"urls in queue {len(url_queue)} visited {len(self.visited_url)}")
                self.visited_url.add(url)
                try:
                    response = requests.get(url, headers=self.source.get("headers", {}))

                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        for a in soup.find_all('a', href = True) :
                                absolute_url = urljoin(url, a['href'])
                                if absolute_url not in self.visited_url and  urlparse(absolute_url).netloc == base_domain and absolute_url not in url_queue:
                                    if current_depth + 1 <= max_depth or max_depth == 0:
                                        url_queue.append(absolute_url)
                                        depth_map[absolute_url] = current_depth + 1
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