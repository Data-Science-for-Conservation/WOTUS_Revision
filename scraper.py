#!/Applications/anaconda/envs/webby/bin

'''
Uses Anaconda environment "webby" with selenium to load JavaScript on the page
and get content:
    - Python 3.7, selenium, requests, scrapy, and Beautiful Soup 4 (bs4)
    - Run `conda activate webby` then `python scraper.py`
'''


import csv
import time
from selenium import webdriver
import bs4


def main():
    csv_file_path = './Data/scraper_csv.csv'
    out_path = './Data/Comments/'

    scrape_comments(csv_file_path, out_path)


def scrape_comments(csv_file_path, out_path):
    css_sel = '.GIY1LSJIXD > div:nth-child(2)'
    # id_prefix = 'EPA-HQ-OW-2018-0149-'

    with open(csv_file_path, newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Skip header
        for i, row in enumerate(csvreader):
            if i > 10:
                break

            ID = row[0]
            url = row[1]

            browser = webdriver.Firefox()
            browser.get(url)
            time.sleep(4)  # Allow time for page to load
            innerHTML = browser.execute_script("return document.body.innerHTML")
            soup = bs4.BeautifulSoup(innerHTML, features="lxml")
            elem = soup.select(css_sel)
            comment = elem[0].text
            # print(comment)

            # Save ID and comment to a text file
            file_path = out_path + '{}.txt'.format(ID)
            with open(file_path, 'w') as f:
                f.write(ID + '\n')
                f.write(comment)

            time.sleep(1)
            browser.quit()


if __name__ == '__main__':
    main()
