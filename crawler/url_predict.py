import pickle
import os
from urllib.parse import urlparse
import re
from tld import get_tld

# trained_model_path = os.path.join(os.path.dirname(__file__),'..', 'model', "malicious_url.pkl")

class Url_predict:
  def __init__(self, url):
    self._url = url
    self.categories = {0:'benign', 1:'defacement', 2:'phising', 3:'malware'}
    self.is_ip = None
    self.abnormal = None
    self.url_len = None
    self.special_characters = ['@','?','-','=','.','#','%','+','$','!','*',',','www', "https", "http"]
    self.special_char_count = None
    self.redirects = None
    self.dirs = None
    self.short_url = None
    self.suspicious = None
    self.tld_length = None
    self.digit_count = None
    self.alpha_count = None
    self.hostname_length = None
    self.prepared_data = []
    self.predicted_value = None

  def have_ip_address(self, url):
    match = re.search(
          '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
          '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4
          '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)' # IPv4 in hexadecimal
          '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}', url)  # Ipv6

    return 1 if match else 0

  def abnormal_url(self, url):
    hostname = urlparse(url).hostname
    hostname = str(hostname)
    match = re.search(hostname, url)

    return 1 if match else 0
  
  def no_of_redirects(self, url):
    parse_object = urlparse(url).path
    return str(parse_object).count('//')

  def no_of_dir(self, url):
    parse_object = urlparse(url).path
    return str(parse_object).count('/')
  
  def sortening_service(self, url):
    match = re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                        'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                        'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                        'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                        'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                        'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                        'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|'
                        'tr\.im|link\.zip\.net',
                        url)
    return 1 if match else 0

  def suspicious_words(self, url):
    match = re.search('PayPal|login|signin|bank|account|update|free|lucky|service|bonus|ebayisapi|webscr',
                      url)
    return 1 if match else 0
  
  def get_tld_length(self, url):
    _tld = get_tld(url,fail_silently=True)

    if _tld:
      return int(len(str(_tld)))
    return 0
  
  def count_numbers(self, url):
    cnt = 0
    for ch in url:
      if ch.isdigit(): cnt+=1
    return cnt

  def count_alpha(self, url):
    cnt = 0
    for ch in url:
      if ch.isalpha(): cnt+=1
    return cnt

  def prepare(self):
    self.is_ip = self.have_ip_address(self._url)
    self.prepared_data.append(self.is_ip)

    self.abnormal = self.abnormal_url(self._url)
    self.prepared_data.append(self.abnormal)

    self.url_len = len(self._url)
    self.prepared_data.append(self.url_len)

    self.special_char_count = []
    for special_character in self.special_characters:
      self.special_char_count.append(self._url.count(special_character))

    self.prepared_data.extend(self.special_char_count)

    self.redirects = self.no_of_redirects(self._url)
    self.prepared_data.append(self.redirects)

    self.dirs = self.no_of_dir(self._url)
    self.prepared_data.append(self.dirs)

    self.short_url = self.sortening_service(self._url)
    self.prepared_data.append(self.short_url)

    self.hostname_length = len(urlparse(self._url).netloc)
    self.prepared_data.append(self.hostname_length)

    self.suspicious = self.suspicious_words(self._url)
    self.prepared_data.append(self.suspicious)

    self.tld_length = self.get_tld_length(self._url)
    self.prepared_data.append(self.tld_length)

    self.digit_count = self.count_numbers(self._url)
    self.prepared_data.append(self.digit_count)

    self.alpha_count = self.count_alpha(self._url)
    self.prepared_data.append(self.alpha_count)

    # print("prepared")
    return

  def predict_url(self):
    if self.prepared_data is None:
      print("ERROR: Data must be prepared before predicting")
      return

    ## define path of the pickle file
    model_path = os.path.join(os.path.dirname(__file__),'..', 'model', "Decisionmalicious_url.pkl")
    
    print(len(self.prepared_data))
    _model = pickle.load(open(model_path, 'rb'))
    self.predicted_value = _model.predict([self.prepared_data])

    print(self.predicted_value)
    print(self.categories[self.predicted_value[0]])

    return
  
if __name__ == "__main__":
  url = "http://www.pashminaonline.com/pure-pashminas"

  obj = Url_predict(url)
  obj.prepare()
  obj.predict_url()