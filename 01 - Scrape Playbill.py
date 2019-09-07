# -*- coding: utf-8 -*-
"""
Scrape playbill.com's "grosses" and store it in a sqlite database

Created on Fri Sep  6 13:57:37 2019

@author: Michael Silva
"""
import sqlite3
import requests
from bs4 import BeautifulSoup

# Set up the database
conn = sqlite3.connect("playbill.sqlite")
cur = conn.cursor()
# This table will hold the week, raw HTML, and a flag if the HTML is processed in future scripts
cur.execute(
    "CREATE TABLE IF NOT EXISTS scrape (id INTEGER PRIMARY KEY, week TEXT UNIQUE, html TEXT, processed INTEGER DEFAULT 0)"
)

# Scrape playbill.com
print("Getting weeks to scrape")
response = requests.get("http://www.playbill.com/grosses")
soup = BeautifulSoup(response.content, features="lxml")

# Get the weeks of data available
print("Begining to scrape")
options = soup.select("select[id=vault-search-results-sort-select] > option")
# Change order making oldest date first in the list
options.reverse()

# Loop through the weeks in the dropdown
for option in options:
    week = option.getText()
    # See if we have data
    cur.execute("SELECT * FROM scrape WHERE week LIKE '" + week + "'")
    row = cur.fetchone()
    if row is None:
        # No data for this week so let's scrape
        url = "http://www.playbill.com/grosses?week=" + week
        print("Scrapping " + url)
        r = requests.get(url)
        html = r.content
        cur.execute("INSERT INTO scrape (week, html) VALUES (?, ?)", (week, html))
        conn.commit()
    else:
        print(week + " data already scrapped!")

conn.close()
