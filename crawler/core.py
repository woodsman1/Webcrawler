from bs4 import BeautifulSoup
import requests


class WebCrawler:

  def __init__(self) -> None:
      pass

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