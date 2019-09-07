#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extract data from the scrapped playbill content and store it in the database

Created on Sat Sep  7 11:46:18 2019

@author: Michael Silva
"""
import sqlite3
from bs4 import BeautifulSoup


def sql_insert(conn, table, row):
    cols = ','.join(row.keys())
    question_marks = ','.join(['?'*len(row)])
    values = (row.values())
    conn.execute('INSERT INTO '+table+' ('+cols+') VALUES ('+question_marks+')', values)


def clean_num(v):
    """Clean the numbers passed in"""
    if "$" in v:
        # Strip out the dollar signs and commas and cast as float
        v = v.replace("$", "").replace(",", "")
        v = float(v)
    if "%" in v:
        # Strip out percent sign, rescale, and cast as float
        v = v.replace("%", "") 
        v = float(v) / 100
    return v
    
# Set up the database
conn = sqlite3.connect("playbill.sqlite")
cur = conn.cursor()
# This table will hold the extracted data
cur.execute(
    """CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY, 
    show TEXT,
    theatre TEXT,
    gross DOUBLE,
    potential_gross DOUBLE,
    gross_diff DOUBLE,
    avg_ticket DOUBLE,
    top_ticket DOUBLE,
    seats_sold INTEGER,
    seats_in_theatre INTEGER,
    perfs INTEGER,
    previews INTEGER,
    percent_capacity DOUBLE,
    capacity_diff DOUBLE,
    week_ending DATE,
    week_total_gross DOUBLE)"""
)

cur.execute("SELECT * FROM scrape WHERE processed = 0 LIMIT 1;")

rows = cur.fetchall()
for row in rows:
    soup = BeautifulSoup(row[2], features="lxml")
    table = soup.find("table", {"class": "bsp-table"})
    tbody = table.find("tbody")
    table_rows = tbody.findAll("tr")
    for table_row in table_rows:
        # Start collecting data for this show
        show_data = {}
        for td in table_row.findAll("td"):
            print(td.text)
        #sql_insert(conn, "data", show_data)
        
