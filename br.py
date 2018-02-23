from bs4 import BeautifulSoup
from urllib.request import urlopen


def table_criteria(tag):
    """Criteria for stats tables for find_all"""
    if not tag.has_attr("class"):
        return False
    else:
        return (tag.name == "table" and
                "stats_table" in tag["class"] and
                "sortable" in tag["class"])


def row_criteria(tag):
    """Criteria for row in stats table for find_all"""
    if not tag.name == "tr":
        return False
    if not tag.has_attr("class"):
        return True
    return ("league_average_table" not in tag["class"] and
            "stat_total" not in tag["class"] and
            "thead" not in tag['class'])


def tables(url):
    """Return all tables from baseball reference as dictionary"""
    dataDict = {}

    # Tables easily accessible
    soup = BeautifulSoup(urlopen(url), "lxml")
    tables = soup.find_all(table_criteria)

    # Tables within comments to fill out list of tables
    comments = soup.find_all('div', class_='placeholder')
    for comment in comments:
        try:
            sub_soup = BeautifulSoup(comment.next_sibling.next_sibling, 'lxml')
        except TypeError:
            pass
        tables.extend(sub_soup.find_all(table_criteria))

    # Add each table to the dictionary
    for table in tables:
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

        dataDict[caption] = [header[0], body]

    return dataDict
