import urllib.parse as urlparse

parsed = urlparse.urlparse('../dfahsdjkfa/path;parameters?query=argument#fragment')
# parsed = parsed._replace(netloc = 'Mohit.com', scheme = 'http')
print (parsed.geturl())
print (parsed.path)