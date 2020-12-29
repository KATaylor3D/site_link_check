import os
import requests
from bs4 import BeautifulSoup
from time import sleep

sleep_time = 0.2

def get_site_links(url):
    site = requests.get(url).text
    soup = BeautifulSoup(site, 'lxml')
    links = []
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        links.append(href)
    return list(set(links))

def fix_links(urls, site):
    filtered_links = []
    for url in urls:
        if url == None:
            filtered_links.append(site)
        elif url.startswith('mailto:') or url.startswith('tel:'):
            filtered_links.append(site)
        elif url.startswith('https://') or url.startswith('http://'):
            filtered_links.append(url)
        elif url.startswith('/'):
            filtered_links.append(site + url[1:])
        else:
            filtered_links.append(site + url)
    return list(set(filtered_links))

def links_in_site(urls, site):
    links = []
    for url in urls:
        try:
            if url.startswith(site):
                links.append(url)
        except:
            pass
    return links

def links_with_status_codes(urls):
    links_codes = []
    for url in urls:
        while True:
            sleep(sleep_time)
            try:
                status_code = requests.get(url).status_code
            except:
                status_code = 0
            if status_code != 429:
                break
        links_codes.append((url, status_code))
    return links_codes

def filter_links(urls, site):
    fixed_links = fix_links(urls, site)
    site_links = links_in_site(fixed_links, site)
    links_and_status_codes = links_with_status_codes(site_links)
    return links_and_status_codes



def main(site):
    visited_links = [(f'{site}', 200)]
    all_links = []
    links = get_site_links(site)
    filtered_links = filter_links(links, site)
    all_links = filtered_links
    all_links.remove((f'{site}', 200))
    scanning = True
    while scanning:
        if all_links != []:
            current_link = all_links[0]
            os.system('cls')
            print('Current link: ', current_link)
            print('Visited links: ', visited_links)
            print('Number of Unvisited links: ', len(all_links))
            print('Number of Visited links: ', len(visited_links))
            visited_links.append(current_link)
            all_links.remove(current_link)
            links = get_site_links(current_link[0])
            filtered_links = filter_links(links, site)
            for filtered_link in filtered_links:
                if filtered_link in visited_links:
                    print('already visited')
                else:
                    all_links.append(filtered_link)
            sleep(.75)
        else:
            scanning = False
    print(visited_links)

if __name__ == '__main__':
    os.system('cls')
    site = input('Website to check: ')
    main(site)