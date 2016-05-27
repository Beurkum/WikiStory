#!/usr/bin/env/python3
# WikiStory, a simple storytelling script that uses Wikipedia.
# Created by Cameron Terry on May 27, 2016.

from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

def openNewPage(link):
    html = urlopen(link)
    soup = BeautifulSoup(html, 'html.parser')
    return soup

reps = {}

soup = openNewPage('http://en.wikipedia.org/wiki/Apple_Inc.')

for new_page in range(10):
    #print(soup.title.text)
    footnote_regex = re.compile(r'\[\d+\]')
    wiki_link_regex = re.compile(r'/wiki/')

    # print first n paragraphs of page and grab links in paragraphs
    n = 5
    links = []
    last_link = ""

    for text in soup.find_all('p', limit=n):
        # grab only links that start with '/wiki'
        links = [tag['href'] for tag in text.select('a[href]') if tag['href'].startswith('/wiki/')]
        if not links == []:
            last_link = links[-1]
        unedited = text.get_text()
        for match in footnote_regex.findall(unedited):
            reps[match] = ''
        edited = replace_all(unedited, reps)
        print(edited)

    new_link = "http://en.wikipedia.org" + last_link
    soup = openNewPage(new_link)

