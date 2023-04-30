import urllib.request as req
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup
from bs4.element import Comment
from get_rss_data import GetNewsData


class GetNewsContent:
    def __init__(
            self,
            url
            ):
        
        fake_request = Request(
            url = url,
            headers = {'User-Agent': 'Mozilla/5.0'}
        )
        
        request = urlopen(fake_request).read()
        
        original_url = self.get_original_content_url(request)

        fake_request = Request(
            url = original_url,
            headers = {'User-Agent': 'Mozilla/5.0'}
        )

        request = urlopen(fake_request).read()
        soup = BeautifulSoup(request, 'html.parser')
        texts = soup.find('article')
        for p in texts.select("p"):
            print(p.text)

    def get_original_content_url(self, raw_html):
        soup = BeautifulSoup(raw_html, 'html.parser')
        texts = soup.findAll(string = True)
        filtered_html = filter(self.tag_visible, texts)  
        parsed_texts = u" ".join(t.strip() for t in filtered_html)
        news_url = parsed_texts.split(' ')[1]

        return news_url
    
    def get_original_content_text(self, raw_html):
        pass

    def tag_visible(self, element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True
    
    def tag_p(self, element):
        if element.parent.name in ['p', ['body']]:
            return True
        else:
            return False
        
    def tag_article(self, element):
        if element.parent.name in ['article']:
            return True
        else:
            return False

test_url = 'https://news.google.com/rss/articles/CBMioAFodHRwczovL3d3dy5zZXVkaW5oZWlyby5jb20vMjAyMy9maW5hbmNhcy1wZXNzb2Fpcy9uZW0tbnViYW5rLW5lbS1pbnRlci1lc3Nlcy1zYW8tb3MtMTAtbWVsaG9yZXMtY2FydG9lcy1kZS1jcmVkaXRvLXNlbS1hbnVpZGFkZS1lLXBhcmEtYWN1bXVsYXItbWlsaGFzLWRlLTIwMjMv0gEA?oc=5'

instance = GetNewsContent(test_url)

