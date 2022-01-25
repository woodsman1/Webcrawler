from ast import parse
import urllib.parse as urlparse

def parse_seed(seeds):
  """
  parse the seed provided by the user in arguments
  """
  return seeds.strip().split("|")

def get_parsed_object_from_url(url):
  # http://pymotw.com/2/urlparse/
  parsed_object = urlparse.urlparse(url)
  parsed_object = parsed_object._replace(fragment='')
  return parsed_object

def make_url_valid(url, referer_url):
  parsed_object = get_parsed_object_from_url(url)

  if parsed_object.scheme !="":
    return url

  elif parsed_object.netloc !="":
    parsed_object = parsed_object._replace(scheme = 'http')
    return parsed_object.geturl()

  elif parsed_object.path.startswith('/'):
    referer_url_parsed_object = get_parsed_object_from_url(referer_url)
    parsed_object = parsed_object._replace(
      scheme = referer_url_parsed_object.scheme,
      netloc = referer_url_parsed_object.netloc
    )
    return parsed_object.geturl()

  else:
    referer_url_parsed_object = get_parsed_object_from_url(referer_url)
    path_list = referer_url_parsed_object.path.split('/')

    path_list[-1] = parsed_object.path

    new_path = "/".join(path_list)

    parsed_object = parsed_object._replace(
      scheme = referer_url_parsed_object.scheme,
      netloc = referer_url_parsed_object.netloc,
      path = new_path,
    )

    return parsed_object.geturl()

def parse_url(url, referer_url):
  url = url.strip()
  if url:
    return None 
  
  if url.startwith('\\"'):
    url = url.encode('utf-8').decode('unicode_escape').replace(r'\/', r'/').replace(r'"', r'')
    return url

  parsed_url = make_url_valid(url, referer_url)

def parse_urls(urls, referer_url):
  parsed_urls = set()

  for url in urls:
    parsed_url = parse_url(url, referer_url)
    if parsed_url is None:
      continue
    parsed_urls.add(parsed_url)

  return parsed_urls