import os
import requests
from bs4 import BeautifulSoup


def get_site_links_with_titles(url):
    site = requests.get(url).text
    soup = BeautifulSoup(site, 'lxml')
    links = []
    titles = []
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        text = a_tag.text
        links.append(href)
        titles.append(text)
    return links, titles

def is_link_active(url):
    return requests.get(url).status_code == 200

def fix_link_syntax(url, site):
    if 'https://' in url:
        return url
    else:
        return site + url[1:]

def is_link_in_site(url, site):
    return site in url

def main(url):
    links, titles = get_site_links_with_titles(url)
    os.system('cls')
    broken_links = []
    for link, title in zip(links, titles):
        fixed_link = fix_link_syntax(link, url)
        if is_link_in_site(fixed_link, url):
            if is_link_active(fixed_link):
                continue
            else:
                broken_links.append(fixed_link)
    if broken_links != []:
        print('Broken links: ')
        for broke_link in broken_links:
            print(broke_link)
    else:
        print("Didn't find any broken links")   


if __name__ == '__main__':
    site = input('Website to check: ')
    main(site)