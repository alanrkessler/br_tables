# -*- coding: utf-8 -*-
"""Access Baseball Reference Tables.

Delivers tables in a dictionary that can be manipulated in pandas or numpy.
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup


def table_criteria(tag):
    """Criteria for stats tables for find_all"""
    table_tag = None
    if not tag.has_attr("class"):
        table_tag = False
    else:
        table_tag = (tag.name == "table" and
                     "stats_table" in tag["class"] and
                     "sortable" in tag["class"])
    return table_tag


def row_criteria(tag):
    """Criteria for row in stats table for find_all"""
    row_tag = None
    if not tag.name == "tr":
        row_tag = False
    elif not tag.has_attr("class"):
        row_tag = True
    else:
        row_tag = ("league_average_table" not in tag["class"] and
                   "stat_total" not in tag["class"] and
                   "thead" not in tag['class'])
    return row_tag


def tables(url):
    """Return all tables from a baseball reference url as dictionary"""
    data_dict = {}

    # List tables that are easily accessible
    soup = BeautifulSoup(urlopen(url), 'html.parser')
    tables_list = soup.find_all(table_criteria)

    # List tables that are within comments
    comments = soup.find_all('div', class_='placeholder')
    for comment in comments:
        try:
            soup = BeautifulSoup(comment.next_sibling.next_sibling,
                                 'html.parser')
        except TypeError:
            pass
        tables_list.extend(soup.find_all(table_criteria))

    # Add each table to the dictionary
    for table in tables_list:
        # Key is the table caption
        caption = table.find('caption').text

        # First value item is list of headers
        table_header = table.find('thead')
        rows = table_header.find_all('tr')
        header = []
        for row in rows:
            cols = row.find_all('th')
            cols = [i.text.strip() for i in cols]
            header.append([i for i in cols])

        # Second value item is data
        table_body = table.find('tbody')
        rows = table_body.find_all(row_criteria)
        body = []
        for row in rows:
            cols = row.find_all(['td', 'th'])
            cols = [ele.text.strip() for ele in cols]
            body.append([ele for ele in cols])

        data_dict[caption] = [header[0], body]

    return data_dict
