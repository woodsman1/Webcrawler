from queue import Queue

class UrlQueue:
  def __init__(self):
    self._visited_urls = dict()
    self._urls_till_now = set()
    self._unvisited_urls = Queue()

  def add_unvisited_url(self, url):
    if not url or url in self._urls_till_now:
      return
    self._unvisited_urls.put_nowait(url)
  
  def add_unvisited_urls(self, urls):
    if isinstance(urls, str):
      self.add_unvisited_url(urls)
    if isinstance(urls, (list,set)):
      for url in urls:
        self.add_unvisited_url(urls)
  
  def add_visited_url(self, url, url_result):
    if not url and url in self._visited_urls:
      return
    self._visited_urls[url] = url_result
  
  def remove_visted_url(self, url):
    self._visited_urls.pop(url)
    return

  # MIGHT CAUSE ERROR (NOT TESTED)
  def clear_unvisited_urls(self):
    # https://stackoverflow.com/questions/6517953/clear-all-items-from-the-queue
    with self._unvisited_urls.mutex:
      self._unvisited_urls.queue.clear()

  def get_unvisited_url(self):
    return self._unvisited_urls.get()

  def get_count_unvisited_url(self):
    return self._unvisited_urls.qsize()

  def get_visited_url(self, url):
    req = self._visited_urls[url]
    self.remove_visted_url(self, url)
    return req
  
  def get_count_visited_url(self):
    return len(self._visited_urls)

  def is_url_visited(self, url):
    return url in self._visited_urls
  
  def is_unvisited_urls_empty(self):
    return self._unvisited_urls.qsize() == 0

  def clear(self):
    self._urls_till_now.clear()
    self._visited_urls.clear()
    self.clear_unvisited_urls()