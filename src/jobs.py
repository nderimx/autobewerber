from threading import Lock
import requests
from bs4 import  BeautifulSoup


class Jobs:
    def __init__(self):
        self.links = []
        self.descriptions = []
        self.mutex = Lock()

    def update_links(self, page_html, links):
        self.mutex.acquire()
        try:
            # self.descriptions = self.descriptions + [jb.string for jb in page_html.find_all('span', {'class': 'sc-fzqNJr Text__span-jiiyzm-8 Text-jiiyzm-9 VacancySerpItem___StyledText-qr45cp-6 hzFALC'})]
            self.links = self.links + [link['href'] for link in page_html.find_all('a', {"data-cy":"job-link"})]
        finally:
            self.mutex.release()

    def retrieve_page(self, page, search_url):
        page_url = search_url+"&page="+str(page)
        # print(page_url)
        try:
            page_result = requests.get(page_url)
        except:
            pass
            print("page "+str(page)+" could not be loaded")
        page_html = BeautifulSoup(page_result.text, 'html.parser')

        # descriptions = [jb.string for jb in page_html.find_all('span', {'class': 'sc-fzqNJr Text__span-jiiyzm-8 Text-jiiyzm-9 VacancySerpItem___StyledText-qr45cp-6 hzFALC'})]
        links = [link['href'] for link in page_html.find_all('a', {"data-cy":"job-link"})]
        self.update_links(page_html, links)