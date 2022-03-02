import argparse

from crawler.url_predict import Url_predict
from .core import WebCrawler

def main():
  parser = argparse.ArgumentParser(description= 'Crawler sites and extracting links and checking the validity also predict user specified urls')
  
  parser.add_argument(
    '--seeds', 
    default="https://www.google.co.in/",
    help='Seed url(s), if more than one add pipe(|) in betweeen. eg."x.com|y.com|z.com".'
  )
  
  parser.add_argument(
    '--crawl-mode', 
    default='bfs',
    help='Add crawling method, bfs or dfs.'
  )

  parser.add_argument(
    '--max-depth',
    default=1,
    type = int,
    help= "Specify max crawl depth."
  )

  parser.add_argument(
    "--concurrency",
    type = int,
    help='Specify concurrency number.',
  )

  parser.add_argument(
    '--predict',
    default=None,
    type= str,
    help="Predict if url is malicious or safe. Add url you want to predict its type",
  )

  args = parser.parse_args()

  crawl(args)


def crawl(args):
  if args.predict != None:
    try:
      obj = Url_predict(args.predict)
      obj.prepare()
      obj.predict_url()
    except Exception as e:
      print("[ERROR]: " + e)
  else:
    try:
      web_crawler = WebCrawler(args.seeds)
      web_crawler.start(
        crawl_mode=args.crawl_mode,
        max_depth=args.max_depth,
        concurrency=args.concurrency,
      )
    except Exception as e:
      print("[ERROR]: " + e)
    finally:
      print("[Finised]")