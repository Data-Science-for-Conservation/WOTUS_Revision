#!/usr/bin/env python3

'''
Uses Anaconda environment "webby" with Selenium (to load JavaScript on the page
    with the content), then Beautiful Soup to parse the HTML:
    - Navigate into the project folder
    - Create environment:
        `conda env create --file environment.yml`
    - Switch to environment: `conda activate webby`
    - Run script: `python scraper.py`
    - Deactivate the environment when done: `conda deactivate`
Notes:
1) Depending on your system, the scraper may take ~1.5-2 days to run - there
    are over 8,000 comments and the program bakes in sleep time to allow the
    page to load
2) Web scrapers are brittle by nature - changes to the HTML structure of the
    target webpage can break the scraper. Always check that the path to the
    unique element the scraper targets is updated in the script
'''


import csv
import time
from selenium import webdriver
import bs4


def main():
    css_sel = '.GIY1LSJIXD > div:nth-child(2)'
    csv_file_path = './Data/scraper_csv.csv'
    out_path = './Data/Comments/'

    # Run the web scraper
    scrape_comments(csv_file_path, css_sel, out_path)


def scrape_comments(csv_file_path, css_sel, out_path):
    '''
    The web scraper loops over a CSV file located at `csv_file_path` that has
    unique web addresses for each comment, grabs text from `css_sel element` on
    the page, and saves the comment's ID and text as a text file to `out_path`
    using the ID as the file name.

    :param csv_file_path: path to a CSV-formatted file with two columns - a
        comment ID and the URL to that comment. Assumes CSV has a header row
    :param css_sel: CSS selector path to the element containing the targeted
        text at the given URL
    :param out_path: path where to save each comment as a text file

    :return: None

    >>>scrape_comments('./my_csv_data', '.GIY1LSJIXD > div:nth-child(2)',
        './TextFiles/')
    '''

    with open(csv_file_path, newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Skip header
        for row in csvreader:
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
                # print(comment)
            except IndexError as e:
                print('Error processing comment: {}'.format(ID))
                print(e)
                browser.quit()
                continue

            # Save ID and comment to a text file
            file_path = out_path + '{}.txt'.format(ID)
            with open(file_path, 'w') as f:
                f.write(ID + '\n')
                f.write(comment)

            time.sleep(1)
            browser.quit()


if __name__ == '__main__':
    main()
