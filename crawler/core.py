import multiprocessing
import queue
import threading
from time import sleep
from bs4 import BeautifulSoup
import requests

from url_queue import UrlQueue


data = [[1, 2, 3], [4, 5 ,6], [7, 8, 9], [10, 11, 12]]


class WebCrawler:

    def __init__(self) -> None:
        self.url_queue = UrlQueue()
        self.current_depth_unvisited_url_queue = queue.Queue()
        self.current_depth = 0

    def get_hyperlinks(urls) -> None:
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




    def just_trial(self, url):
        print("trial", url)

        for x in data[url]:
            self.url_queue.add_unvisited_url(x)
            print(x, "add")


    def crawl(self):
        while 1:
            try:
                url = self.current_depth_unvisited_url_queue.get()
                # print(url)
                self.just_trial(url)
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
                print("here")
                url = self.url_queue.get_unvisited_url()
                print(url)
                self.current_depth_unvisited_url_queue.put_nowait(url)
                # self.current_depth_unvisited_url_queue.task_done()
            
            # print("here")
            self.current_depth_unvisited_url_queue.join()
            print("joined")
            # print(self.url_queue.is_unvisited_urls_empty())
            self.current_depth += 1




    def start(self, crawl_mode = "bfs", max_depth = 10, concurrency = None):
        # https://www.codeproject.com/Questions/218217/How-to-decide-ideal-number-of-threads
        concurrency = concurrency if concurrency else (multiprocessing.cpu_count()*4)
        
        for i in range(2):
            self.current_depth_unvisited_url_queue.put_nowait(i)
        
        # this cause join problem in queue (or other may be)
        # self.reset_all()

        threads = self.create_threads(concurrency)

        sleep(0.5)
        if(crawl_mode.lower() == 'bfs'):
            self.bfs(max_depth)



    def reset_all(self):
        self.current_depth = 0
        self.current_depth_unvisited_url_queue.queue.clear()
        self.url_queue.clear()


if __name__ == "__main__":
    wc = WebCrawler()
    wc.start('bfs', 0, 1)