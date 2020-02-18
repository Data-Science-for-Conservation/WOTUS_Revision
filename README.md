# Analysis of Public Comments Regarding the EPA's Revised Definition of "Waters of the United States" (WOTUS)

In early 2017, President Trump signed an Executive Order<sup>[1](#footnote1)</sup> requesting that agencies review a 2015 rule put in place by the Obama administration regarding the "Waters of the United States". The agencies, including the Environmental Protection Agency (EPA) and the Department of the Army, were instructed to rescind or replace the rule, in accordance with law.

The agencies have since conducted a reevaluation and revision of the definition of WOTUS. Their proposed rule redefined the scope of waters federally regulated under the Clean Water Act (CWA). (In other words, it changes which waterways fall under federal authority.) The re-definition was open for public comment until April 15, 2019, and the revised rule took effect on December 23, 2019.

This project analyzes the content of comments that are publicly available in the docket on the [regulations.gov web page](https://www.regulations.gov/docket?D=EPA-HQ-OW-2018-0149). The comments were collected by running a web scraping program (`./scraper.py`) which looped over all public submissions in the docket that didn't contain an attachment. Once the data were collected, a variety of Natural Language Processing (NLP) techniques were applied. These included topic analysis, clustering, and similarity analysis. As this is an un-labeled dataset, it wasn't possible to apply supervised learning techniques such as classification, sentiment analysis, or transfer learning.

Visit the [repository website](https://data-science-for-conservation.github.io/WOTUS_Revision/) for a summary of the analysis performed and project takeaways.

## Setting Up the Local Environment and Running the Scraper

This project uses the [Anaconda distribution](https://www.anaconda.com/distribution/) to manage Python packages. An environment with all necessary packages to run `scraper.py` is saved in `./environment.yml`. If you're using Anaconda as well, you can run the following commands to create the `webby` environment locally.

```bash
conda env create --file environment.yml
```

(If you don't like the name `webby`, you can edit the first line of your local version of the `environment.yml` file and change it to whatever name you'd prefer.)

Because the scraper uses the Selenium webdriver to control a browser, you'll also need to download the appropriate webdriver executable and add it to your local `PATH`. Popular options are Firefox's [geckodriver](https://github.com/mozilla/geckodriver/) or Chromium's [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/), with [other browser support found here](https://selenium.dev/documentation/en/getting_started_with_webdriver/browsers/).

To actually run the scraper, first clone the project and navigate to it in your local directory. Then use the following commands to activate the environment and run the scraper:

```bash
conda activate webby
python scraper.py
```

Depending on the system, the scraper takes \~1.5-2 days to run - there are over 8,000 comments and the program bakes in delay time to allow the page to load.

Notes:

<a name="footnote1">1</a>: Executive Order 13778, signed on February 28, 2017, titled "Restoring the Rule of Law, Federalism, and Economic Growth by Reviewing the 'Waters of the United States' Rule"
