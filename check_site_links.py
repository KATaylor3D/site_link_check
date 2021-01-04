import os
import requests
from bs4 import BeautifulSoup
from time import sleep

sleep_time = 10

def build_starting_tuple(url):
    url = url
    parent = url
    text = 'OG url'
    status_code = 200
    return (url, parent, text, status_code)

def get_links_parents_and_texts(url_tup):
    url, parent, text, status_code  = url_tup
    try:
        site = requests.get(url, timeout=3).text
        soup = BeautifulSoup(site, 'lxml')
        url_tup = set()
        for a_tag in soup.findAll("a"):
            href = a_tag.attrs.get("href")
            text = a_tag.text
            url_tup.add((href, url, text))
        return url_tup
    except requests.InvalidHeader as err:
        print(err)
        print(f'Invalid Header. Failed to get_links_with_parent for url: {url} child of {parent}')
        return (url, parent, text)
    except requests.RequestException as err:
        print(err)
        print(f'Failed to get_links_with_parent for url: {url} child of {parent}')
        return (url, parent, text)

def mend_links(url_tup, site):
    mended_links = set()
    for url, parent, text in url_tup:
        if url == None:
            mended_links.add((site, site, 'OG url'))
        elif url.startswith('mailto:') or url.startswith('tel:') or url.startswith('javascript:'):
            mended_links.add((site, site, 'OG url'))
        elif '?EventViewMode' in url:
            mended_links.add((site, site, 'OG url'))
        elif url.startswith('https://') or url.startswith('http://'):
            mended_links.add((url, parent, text))
        elif url.startswith('/'):
            mended_links.add((site + url[1:], parent, text))
        else:
            mended_links.add((site + url, parent, text))
    return mended_links

def add_status_code(url_tup):
    url, parent, text = url_tup
    while True:
        try:
            status_code = requests.get(url).status_code
            if status_code == 429:
                print('Too many requests in an amount of time')
                print(f'Waiting {sleep_time} second(s) and will try again')
                sleep(sleep_time)
                continue
            elif status_code == 200:
                break
            else:
                break
        except requests.RequestException as err:
            print(err)
            print(f"Failed getting status code for {url_tup}")
            status_code = 0
            break
    return (url, parent, text, status_code)

def is_link_in_site(url_tup, site):
    url, *b = url_tup
    return url.startswith(site)

def list_to_examine(url_tup):
    comp = []
    for url, *b in url_tup:
        comp.append(url)
    return comp

def search_site_for_links_statuses(site):
    original_link = build_starting_tuple(site)
    visited_links = set()
    all_links = set()
    all_links.add(original_link)
    scanning = True
    while scanning:
        if all_links == set():
            scanning = False
        else:
            os.system('cls')
            print(f"{len(all_links)} site(s) to visit")
            print(f"{len(visited_links)} site(s) visited")
            url = all_links.pop()
            print(f"Visiting {url}...")
            print(f'    Removed {url} from all_links')
            visited_links.add(url)
            print(f'    Added {url} to visited_links')
            if is_link_in_site(url, site) and url[3] == 200 and not url[0].endswith('.pdf'):
                links = get_links_parents_and_texts(url)
                links = mend_links(links, site)
                for link in links:
                    if link[0] not in list_to_examine(visited_links) and link[0] not in list_to_examine(all_links):
                        full_link = add_status_code(link)
                        all_links.add(full_link)
                        print(f"    Added {full_link} to all_links")
                    else:
                        print(f"    Skipped {link} to all_links")
    return visited_links

def get_report_from_file(filename):
    url_tups = set()
    with open(filename, 'r') as file:
        content = file.read()
    seperate_tups = content.split('\n')[:-1]
    for tup in seperate_tups:
        trimmed_str = tup[1:-1]
        link, parent, *end = trimmed_str.split(", ")
        link = link[1:-1]
        parent = parent[1:-1]
        end = str(end)[1:-1]
        text, status_code = end.rsplit(", ", 1)
        text = text[2:-2]
        status_code = int(status_code[1:-1])
        url_tup = (link, parent, text, status_code)
        url_tups.add(url_tup)
    return url_tups

def get_problem_links(url_tups):
    problem_links = set()
    for url_tup in url_tups:
        if url_tup[3] != 200 and url_tup[3] != 404:
            problem_links.add(url_tup)
    return problem_links

def get_broken_links(url_tups):
    broken_links = set()
    for url_tup in url_tups:
        if url_tup[3] == 404:
            broken_links.add(url_tup)
    return broken_links

def create_filename_from_url(url):
    if "www." in url:
        filename = url.split("www.")[1]
        filename = filename.split('/')[0] + '.txt'
    else:
        filename = url.split("://")[1]
        filename = filename.split('/')[0] + '.txt'
    return filename

def save_report(site, url_tups):
    filename = create_filename_from_url(site)
    problem_links = get_problem_links(url_tups)
    broken_links = get_broken_links(url_tups)
    with open(filename, 'w') as file:
        for link in broken_links:
            file.write(str(link) + '\n')
        for link in problem_links:
            file.write(str(link) + '\n')
        file.write(f"There are {len(broken_links)} broken links and {len(problem_links)} problem links")

def logic(url):
    site = url
    filename = create_filename_from_url(site)
    if os.path.exists(filename):
        report = get_report_from_file(filename)
    else:
        link_statuses = search_site_for_links_statuses(site)       
        save_report(site, link_statuses)
        report = link_statuses
    if report:
        return report
    else:
        return "Didn't find any problem links"

def main():
    os.system('cls')
    site = input('Website to check: ')
    filename = create_filename_from_url(site)
    if os.path.exists(filename):
        report = get_report_from_file(filename)
    else:
        link_statuses = search_site_for_links_statuses(site)
        save_report(site, link_statuses)
        report = link_statuses
    if report:
        for line in report:
            print(line)
    else:
        print("Didn't find any problem links")

if __name__ == '__main__':
   print('Call main() to run command line interface')
   print('Run interface.py for gui tool')