import sys, os
sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath(".."))
from news_data.services.get_news_content import GetNewsContent


test_url = 'https://news.google.com/rss/articles/CBMioAFodHRwczovL3d3dy5zZXVkaW5oZWlyby5jb20vMjAyMy9maW5hbmNhcy1wZXNzb2Fpcy9uZW0tbnViYW5rLW5lbS1pbnRlci1lc3Nlcy1zYW8tb3MtMTAtbWVsaG9yZXMtY2FydG9lcy1kZS1jcmVkaXRvLXNlbS1hbnVpZGFkZS1lLXBhcmEtYWN1bXVsYXItbWlsaGFzLWRlLTIwMjMv0gEA?oc=5'

instance = GetNewsContent()

print(instance.run(test_url))