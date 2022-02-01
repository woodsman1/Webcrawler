import multiprocessing
import queue
import threading
import time
from bs4 import BeautifulSoup
import requests
from helper import save_data_to_csv
from url_parser import parse_seed, parse_urls
from url_queue import UrlQueue

class WebCrawler:

    def __init__(self, _seeds) -> None:
        self.url_queue = UrlQueue()
        self.current_depth_unvisited_url_queue = queue.Queue()
        self.current_depth = 0
        self.seeds = parse_seed(_seeds)
        self.url_queue.add_unvisited_urls(self.seeds)
        self.bad_url_mapping = dict()

    def get_hyperlinks(self, url, retry_time = 1) -> None:
        status_code = 0
        response_time = 0
        response_str = ''

        try:
            # print(url, "get hyperlink")
            start_time = time.time()
            resp = requests.get(url)
            response_time = time.time() - start_time

            sp = BeautifulSoup(resp.text, 'lxml')
            data = sp.find_all("a", href=True)

            raw_urls = set()

            for x in data:
                raw_url = x['href']
                raw_urls.add(raw_url)

            status_code = str(resp.status_code)

            # parse data (get filter data)
            parsed_urls = parse_urls(raw_urls, url)
            # add the parsed data
            self.url_queue.add_unvisited_urls(parsed_urls)

            response_str = "Success"

            if resp.status_code > 400:
                response_str = f'{status_code} HTTP Status Code'

            # parse data
        except requests.exceptions.SSLError as ex:
            status_code = 'SSLError'
            response_str = str(ex)
            retry_time = 0
        except requests.exceptions.InvalidSchema as ex:
            response_str = str(ex)
            status_code = 'InvalidSchema'
            retry_time = 0
        except requests.exceptions.ChunkedEncodingError as ex:
            response_str = str(ex)
            status_code = 'ChunkedEncodingError'
            retry_time = 0
        except requests.exceptions.InvalidURL as ex:
            response_str = str(ex)
            status_code = 'InvalidURL'
            retry_time = 0
        except Exception as ex:
            response_str = str(ex)
            status_code = 'Unknown Exception'
        
        if retry_time > 0:
            if not status_code.isdigit() or int(status_code) > 400:
                time.sleep((2-retry_time)*2)
                return self.get_hyperlinks(url, retry_time-1)
        else:
            self.bad_url_mapping[url] = response_str

        result = {
            'status_code' : status_code,
            'response_time' : response_time,
            'response_statement' :response_str,
        }

        self.url_queue.add_visited_url(url, result)
        return

    def crawl(self):
        while 1:
            try:
                url = self.current_depth_unvisited_url_queue.get()
                # print(url, "crawl")
                self.get_hyperlinks(url)
            finally:
                self.current_depth_unvisited_url_queue.task_done()

    def create_threads(self, no_threads):
        for _ in range(no_threads):
            thread = threading.Thread(target=self.crawl) # define crawl
            # this might cause error
            thread.daemon = True
            thread.start()

    def bfs(self, depth):
        """
        crawl the urls in breath first search manner
        """
        while self.current_depth <= depth: 
            while not self.url_queue.is_unvisited_urls_empty():
                url = self.url_queue.get_unvisited_url()
                # print(url, "bfs")
                self.current_depth_unvisited_url_queue.put_nowait(url)
            time.sleep(1)
                
            self.current_depth_unvisited_url_queue.join()
            self.current_depth += 1

    def start(self, crawl_mode = "bfs", max_depth = 10, concurrency = None):
        # https://www.codeproject.com/Questions/218217/How-to-decide-ideal-number-of-threads
        concurrency = concurrency if concurrency else (multiprocessing.cpu_count()*4)
        
        # this cause join problem in queue (or other may be)
        # self.reset_all()

        threads = self.create_threads(concurrency)

        if(crawl_mode.lower() == 'bfs'):
            self.bfs(max_depth)

        vis_url_dict = self.url_queue.get_visited_urls_set()

        # for url, detail in vis_url_dict.items():
        #     print(url ,':', detail)
        
        save_data_to_csv(vis_url_dict)
        return

    def reset_all(self):
        self.current_depth = 0
        self.current_depth_unvisited_url_queue.queue.clear()
        self.url_queue.clear()


if __name__ == "__main__":
    seed = "https://codeforces.com/"
    wc = WebCrawler(seed)
    wc.start('bfs', 1)