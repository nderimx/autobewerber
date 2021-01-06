import unittest
import sys
import os
sys.path.append(os.getcwd()+"/src")
import scraper
import requests
from bs4 import BeautifulSoup
host_url = "https://www.jobs.ch"

def scrape_one_link(search_term):
    mod_search_term = search_term.replace(" ", "%20")
    search_url = host_url+"/en/vacancies/?term="+mod_search_term

    search_results_page = requests.get(search_url)
    page_html = BeautifulSoup(search_results_page.text, 'html.parser')
    return host_url+page_html.find('a', {'data-cy':'job-link'})['href']

search_term = "Information Security"

class TestScrape(unittest.TestCase):
    def test_live_scrape(self):
        print("\nScrape attributes from a live ad page:\n")

        attributes = scraper.scrape_ad(scrape_one_link(search_term))

        for i in range(5):
            self.assertTrue(attributes[i], "Attributes on the ad are empty")
            print(attributes[i])

    def test_link_getter(self):
        print("Scrape all ad links:")

        links = scraper.scrape_links(search_term)
        self.assertTrue(len(links)>100, "There are too few links")
        self.assertTrue(len(links), "There are no links as results")
        self.assertTrue(links[0], "At least one link is empty")
        self.assertIn("/en/vacancies/detail/", links[0], "At least one link does not work")


if __name__ == '__main__':
    unittest.main()