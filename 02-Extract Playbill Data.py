#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extract data from the scrapped playbill content and store it in the database

Created on Sat Sep  7 11:46:18 2019

@author: Michael Silva
"""
import sqlite3
import datetime
from bs4 import BeautifulSoup


def sql_insert(conn, table, row):
    """
    Insert a dictionary into a sqlite database

    Parameters:
    conn (object): sqlite connection
    table (str): Name of the database table
    row (dict): The key value pairs to be inserted

    Returns:
    None
    """
    cur = conn.cursor()
    columns = ", ".join(row.keys())
    placeholders = ":" + ", :".join(row.keys())
    query = "INSERT INTO " + table + " (%s) VALUES (%s)" % (columns, placeholders)
    cur.execute(query, row)
    conn.commit()


def clean_num(v):
    """
    Clean the numbers passed in

    Parameters: 
    v (str): The number that needs to be cleaned 
  
    Returns: 
    mixed: A clean integer or float
    """
    if "$" in v:
        # Strip out the dollar signs and commas and cast as float
        v = v.replace("$", "").replace(",", "")
        v = float(v)
    elif "%" in v:
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

cur.execute("SELECT * FROM scrape WHERE processed = 0;")

rows = cur.fetchall()
for row in rows:
    print("Working on " + row[1])
    week_ending = datetime.datetime.strptime(row[1], "%Y-%m-%d")
    soup = BeautifulSoup(row[2], features="lxml")
    week_total_gross = clean_num(
        soup.find("div", {"class": "week-total"}).find("span").text
    )
    table = soup.find("table", {"class": "bsp-table"})
    tbody = table.find("tbody")
    table_rows = tbody.findAll("tr")
    for table_row in table_rows:
        # Start collecting data for this show
        show_data = {"week_total_gross": week_total_gross, "week_ending": week_ending}
        for td in table_row.findAll("td"):
            td_class = td["class"][0]
            if td_class == "col-0":
                show_data["show"] = show = td.find("a").text.strip()
                show_data["theatre"] = td.text.replace(show, "").strip()
            elif td_class == "col-1":
                for span in td.findAll("span"):
                    val = clean_num(span.text)
                    if span["class"][0] == "data-value":
                        show_data["gross"] = val
                    else:
                        show_data["potential_gross"] = val
            elif td_class == "col-2":
                show_data["gross_diff"] = clean_num(td.text)
            elif td_class == "col-3":
                for span in td.findAll("span"):
                    val = clean_num(span.text)
                    if span["class"][0] == "data-value":
                        show_data["avg_ticket"] = val
                    else:
                        show_data["top_ticket"] = val
            elif td_class == "col-4":
                for span in td.findAll("span"):
                    val = clean_num(span.text)
                    if span["class"][0] == "data-value":
                        show_data["seats_sold"] = val
                    else:
                        show_data["seats_in_theatre"] = val
            elif td_class == "col-5":
                for span in td.findAll("span"):
                    val = clean_num(span.text)
                    if span["class"][0] == "data-value":
                        show_data["perfs"] = val
                    else:
                        show_data["previews"] = val
            elif td_class == "col-6":
                show_data["percent_capacity"] = clean_num(td.text)
            elif td_class == "col-7":
                show_data["capacity_diff"] = clean_num(td.text)
        sql_insert(conn, "data", show_data)
        cur.execute("UPDATE scrape SET processed = 1 WHERE id = ?", (row[0],))
        conn.commit()
