import urllib.request as req

from bs4 import BeautifulSoup
from bs4.element import Comment
from get_rss_data import GetNewsData


class GetNewsContent:
    def __init__(
            self,
            url
            ):
        
        request = req.urlopen(url).read()
        
        original_url = self.get_original_content_url(request)
        
    def get_original_content_url(self, raw_html):
        soup = BeautifulSoup(raw_html, 'html.parser')
        texts = soup.findAll(string = True)
        filtered_html = filter(self.tag_visible, texts)  
        parsed_texts = u" ".join(t.strip() for t in filtered_html)
        news_url = parsed_texts.split(' ')[1]

        return news_url
    
    def get_original_content_text(self, raw_html):
        

    def tag_visible(self, element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True

test_url = 'https://news.google.com/rss/articles/CBMioAFodHRwczovL3d3dy5zZXVkaW5oZWlyby5jb20vMjAyMy9maW5hbmNhcy1wZXNzb2Fpcy9uZW0tbnViYW5rLW5lbS1pbnRlci1lc3Nlcy1zYW8tb3MtMTAtbWVsaG9yZXMtY2FydG9lcy1kZS1jcmVkaXRvLXNlbS1hbnVpZGFkZS1lLXBhcmEtYWN1bXVsYXItbWlsaGFzLWRlLTIwMjMv0gEA?oc=5'

instance = GetNewsContent(test_url)

