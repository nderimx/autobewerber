import requests
from bs4 import BeautifulSoup
import time
import re
import pandas
from jobs import Jobs
from threading import Thread
from datetime import date

host_url = "https://www.jobs.ch"

def scrape_links(search_term):
    mod_search_term = search_term.replace(" ", "%20")
    search_url = host_url+"/en/vacancies/?term="+mod_search_term

    search_results_page = requests.get(search_url)
    page_html = BeautifulSoup(search_results_page.text, 'html.parser')

    jobs = Jobs()

    # jobs.descriptions = [jb.string for jb in page_html.find_all('span', {'class': 'sc-fzqNJr Text__span-jiiyzm-8 Text-jiiyzm-9 VacancySerpItem___StyledText-qr45cp-6 hzFALC'})]
    jobs.links = [link['href'] for link in page_html.find_all('a', {"data-cy":"job-link"})]
    pages = int(page_html.find('span', {"data-cy":"page-count"}).string.split(' ')[2])
    # print(pages-1)
    threads = []
    for page in range(2, pages+1):
        threads.append(Thread(target = jobs.retrieve_page, args = (page, search_url)))
        threads[page-2].start()

    for thread in threads:
        thread.join()

    # for i in range(len(jobs.links)):
    #     print(jobs.links[i])
    # print(len(jobs.links))
    return jobs.links

def get_details_from_soup(soup):
    try:
        unternehmen         = soup.find('a', {"data-cy":"company-tab-title"}).string
    except Exception as e:
        print("Coudn't find unternehmen in soup: %s" % e)
        with open('debug.txt', 'w') as debug_output:        #dubug
            debug_output.write(soup.prettify())             #debug
        return "0", "0", "0", "0", "0"
    try:
        encoded_address = soup.find('table', {'class' : 'DetailCompanyBoxComponent___StyledTable-sc-15wqweb-3 czAVYV'}).find(string='Location').parent.parent.next_sibling
    except Exception as e:
        print("Coudn't find encoded_address in soup: %s" % e)
        with open('debug.txt', 'w') as debug_output:        #dubug
            debug_output.write(soup.prettify())             #debug
        return "0", "0", "0", "0", "0"
    proto_address = str(encoded_address).replace("<td>", "").replace("</br></td>", "").replace("<!-- -->", "").replace("</td>", "")
    if "<br>" in proto_address:
        full_address = proto_address.split("<br>")
    else:
        full_address = proto_address.split("<br/>")
    strasse             = full_address[0]
    platz               = full_address[1]
    stellenbeschreibung = soup.find('h1', {"data-cy":"vacancy-title"})['title']
    ansprache           = "Sehr geehrtes "+unternehmen.replace(" AG", "")+" Team"
    # email               = re.search("^.*@.*\.$com|ch", str(soup))
    # text                = soup.find('iframe', {"data-cy":"detail-vacancy-iframe-content"})#.get_text()
    return unternehmen, strasse, platz, stellenbeschreibung, ansprache

def scrape_ad(link):
    try:
        ad_page = requests.get(link)
    except:
        print("could not load ad page: %s" % link)
    page_html = BeautifulSoup(ad_page.text, 'html.parser')

    return get_details_from_soup(page_html)