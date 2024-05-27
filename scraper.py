import requests
from bs4 import BeautifulSoup

class Scraper(object):
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0"
        }
    
    def get_page_html(self, url):
        page = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        return soup
    
    def get_beautifulsoup_by_html(self, html: str):
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    def find_all_elements_by_element_name(self, html: BeautifulSoup, element_name: str):
        result = html.find_all(element_name)
        return result

    def find_all_elements_by_id(self, html: BeautifulSoup, element_name: None, element_id: str):
        result = html.find_all(element_name, id=element_id)
        return result
    
    def find_all_elements_by_class(self, html: BeautifulSoup, element_name: None, class_name: str):
        result = html.find_all(element_name, class_=class_name)
        return result
    
    def find_specific_element_by_id(self, html: BeautifulSoup, element_name: None, element_id: str):
        result = html.find(element_name, id=element_id)
        return result
    
    def find_specific_element_by_class(self, html: BeautifulSoup, element_name: None, class_name: str):
        result = html.find(element_name, class_=class_name)
        return result