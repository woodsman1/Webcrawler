import multiprocessing
import threading
from bs4 import BeautifulSoup
import requests


class WebCrawler:

    def __init__(self) -> None:
    #   self.website_list = seeds
    #   self.url_queue = Queue
    #   self.current_depth_unvisited_url_queue = Queue
        pass

    def create_threads(self, no_threads):
        threads = []
        for _ in range(no_threads):
            thread = threading.Thread(targe=self.crawl) # define crawl
            # this might cause error
            # thread.daemon = True
            thread.start()
            threads.append(thread)
        return threads

    def join_threads(slef, threads):
        for thread in threads:
            thread.join()
        return

    def start(self, crawl_mode = "bfs", max_depth = 10, concurrency = None):
        
        concurrency = concurrency if concurrency else (multiprocessing.cpu_count()*4)
        # print(info of the details and start)

        # reset all the data

        threads = self.create_threads(concurrency)

        self.join_threads(threads)


    def get_urls() -> list:
        urls = []
        ## get the url from queue
        ## but temporarly appended manually
        urls.append("https://codeforces.com/")
        return urls


    def parse_data(urls) -> None:
        for url in urls:
            print(url)
            r = requests.get(url)
            sp = BeautifulSoup(r.text, 'lxml')
            data = sp.find_all("a", href=True)

            for x in data:
                link = x['href']
                if not link.startswith("https://"):
                    link = url + link[1:]
                print(link)


if __name__ == "__main__":
    wc = WebCrawler()
    urls = wc.get_urls()
    wc.parse_data(urls)