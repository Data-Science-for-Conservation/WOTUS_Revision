#!/usr/bin/env python3

'''
Uses Anaconda environment "webby" with Selenium (to load JavaScript on the page
    with the content), then Beautiful Soup to parse the HTML:
    - Navigate into the project folder
    - Create environment:
        `conda env create --file environment_webby.yml`
    - Switch to environment: `conda activate webby`
    - Run script: `python scraper.py`
    - Deactivate the environment when done: `conda deactivate`
Notes:
1) Depending on your system, the scraper may take ~1.5-2 days to run - there
    are over 8,000 comments and the program bakes in sleep time to allow the
    page to load and to space requests so as not to overload the site's server
2) Web scrapers are brittle by nature - changes to the HTML structure of the
    target webpage can break the scraper. Always check that the path to the
    unique element the scraper targets is updated in the script
'''


import os
import csv
import time
import sqlite3
from sqlite3 import Error
from selenium import webdriver
import bs4


def main():

    # Paths and inputs
    base_dir = os.getcwd()
    data_dir = os.path.join(base_dir, 'Data/')
    db_file = data_dir + 'comments.db'

    # CSS Selector on each page that holds the comment text
    css_sel = 'div.px-2:nth-child(2)'

    # CSV with URL to each comment (downloaded from docket page)
    csv_file_path = data_dir + 'scraper_csv.csv'

    # Create table statement
    sql_create_table = """CREATE TABLE IF NOT EXISTS comments (
                              "Document ID" text PRIMARY KEY,
                              Comment text
                          );"""

    # Establish database connection
    db_conn = create_conn(db_file)

    # Create table
    if db_conn is not None:
        create_table(db_conn, sql_create_table)
    else:
        print("ERROR: Failed to connect to database!")

    # Run the web scraper
    scrape_comments(csv_file_path, css_sel, db_conn)

    # Close the database connection
    db_conn.close()


def create_conn(db_file):
    '''
    :param db_path: path and file name where database will be saved
    :return: connection to database
    '''
    conn = None

    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)


def create_table(db_conn, create_table_sql):
    '''
    Creates a table from the `create_table_sql` and saves to database linked
        via the `db_conn` connection.
    :param db_conn: sqlite Connection object to database
    :param create_table_sql: str, a SQL CREATE TABLE statement
    :return: None
    '''
    try:
        cursor = db_conn.cursor()
        cursor.execute(create_table_sql)
        db_conn.commit()
    except Error as e:
        print(e)


def scrape_comments(csv_file_path, css_sel, db_conn):
    '''
    The web scraper loops over a CSV file located at `csv_file_path` that has
    unique web addresses for each comment, grabs text from `css_sel element` on
    the page, and saves the comment's ID and text to a database linked via the
    `db_conn` connection.

    :param csv_file_path: path to a CSV-formatted file with two columns - a
        comment ID and the URL to that comment. Assumes CSV has a header row
    :param css_sel: CSS selector path to the element containing the targeted
        text at the given URL
    :param db_conn: sqlite Connection object to database

    :return: None

    >>>scrape_comments('./my_csv_data', 'div:nth-child(2)', db_conn)
    '''

    with open(csv_file_path, newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Skip header
        count = 0

        for row in csvreader:
            if count == 5:
                break
            count += 1

            ID = row[0]
            url = row[1]

            # Open a browser and fetch the comment text
            browser = webdriver.Firefox()
            browser.get(url)
            time.sleep(4)  # Allow time for page to load
            inHTML = browser.execute_script("return document.body.innerHTML")
            soup = bs4.BeautifulSoup(inHTML, features="lxml")
            elem = soup.select(css_sel)

            try:
                comment = elem[0].text
                print(comment)
            except IndexError as e:
                print('Error processing comment: {}'.format(ID))
                print(e)
                browser.quit()
                continue

            # Save ID and comment to database
            try:
                cursor = db_conn.cursor()
                cursor.execute("INSERT INTO comments VALUES (?, ?)",
                               (ID, comment))
                db_conn.commit()
            except Error as e:
                print('Error saving comment {} to database'
                      .format(ID))
                print(e)
                continue

            time.sleep(1)
            browser.quit()


if __name__ == '__main__':
    main()
