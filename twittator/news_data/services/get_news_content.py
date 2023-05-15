import urllib.request as req
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup
from bs4.element import Comment

class GetNewsContent:
    
    def get_original_content_url(self, raw_html):
        soup = BeautifulSoup(raw_html, 'html.parser')
        texts = soup.findAll(string = True)
        filtered_html = filter(self.tag_visible, texts)  
        parsed_texts = u" ".join(t.strip() for t in filtered_html)
        news_url = parsed_texts.split(' ')[1]

        return news_url
    
    def get_original_content_text(self, original_url):
        fake_request = self.generate_fake_request(original_url)
        request = urlopen(fake_request).read()
        soup = BeautifulSoup(request, 'html.parser')
        texts = soup.find('article')

        p_list = []
        for p in texts.select("p"):
            p_list.append(p.text)

        return p_list

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
    
    def generate_fake_request(
            self, 
            url: str
            ):
        return Request(
            url = url,
            headers = {'User-Agent': 'Mozilla/5.0'}
        )
    
    def filter_relevant_content(
            self, 
            p_list: list
            ):
        filtered_p_list = []

        for p_text in p_list:
            if len(p_text) > 120:
                if len(filtered_p_list) < 3:
                    filtered_p_list.append(p_text)
                else:
                    break

        return filtered_p_list
    
    def get_content(
            self, 
            url: str
            ):
        fake_request = self.generate_fake_request(url)
        
        request = urlopen(fake_request).read()
        
        original_url = self.get_original_content_url(request)

        p_list = self.get_original_content_text(original_url)

        final_p = self.filter_relevant_content(p_list)

        return (final_p, original_url)
