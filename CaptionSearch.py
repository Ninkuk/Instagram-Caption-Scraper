from selenium import webdriver
from bs4 import BeautifulSoup
import re
import time


# takes user input of username and string to search
def get_user_requirements():
    url = 'https://www.instagram.com/'
    username = input("Enter the username you wish to scrape:")
    string_to_search = input("Enter the string to search:")
    url += str(username)
    get_links(url, string_to_search)


# scrolls through the user page and gathers all the posts' links
def get_links(url, string_to_search):
    links = []
    browser = webdriver.Chrome()
    browser.get(url)
    last_height = browser.execute_script("return document.body.scrollHeight")
    while True:
        source = browser.page_source
        data = BeautifulSoup(source, 'html.parser')
        body = data.find('body')
        script = body.find('span')

        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        try:
            script.findAll('a')
        except:
            print("Sorry! An unexpected error occurred. Please make sure you enter a valid username")
            break

        for link in script.findAll('a'):
            if re.match("/p", link.get('href')):
                to_add = 'https://www.instagram.com' + link.get('href')
                if to_add not in links:
                    links.append(to_add)

        time.sleep(3)
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    print(len(links), "posts found")
    browser.close()
    filter_captions(links, string_to_search)


# this searches the string in the caption of all the posts
def filter_captions(links, string_to_search):
    filtered_links = []
    browser = webdriver.Chrome()
    for link in links:
        browser.get(link)
        source = browser.page_source
        data = BeautifulSoup(source, 'html.parser')
        for text in data.findAll('span'):
            if string_to_search.lower() in text.text.lower():
                if link not in filtered_links:
                    filtered_links.append(link)

    print(len(filtered_links), 'results founds')
    browser.close()
    write_to_file(filtered_links)


# finally this stores the resulting links in a txt file
def write_to_file(filtered_links):
    file_name = input("What would you like to call the file:")
    with open(f"{file_name}.txt", 'w') as f:
        for item in filtered_links:
            f.write("%s\n" % item)


# Main method
if __name__ == '__main__':
    get_user_requirements()
