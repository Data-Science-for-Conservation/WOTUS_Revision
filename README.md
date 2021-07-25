# Analysis of Public Comments Regarding the EPA's Revised Definition of "Waters of the United States"

**Quick Links to Project Resources:**

- **[Project Overview](https://data-science-for-conservation.github.io/WOTUS_Revision/):** project background, challenges, analysis, and conclusions
- **[Jupyter Notebook](./WOTUS_analysis.ipynb):** source code and underlying analysis
- **[NH-Python Meetup Presentation](./NH-Python_Pres/):** slides presented to the NH-Python group in April 2020
<!-- - **[Deployed Models](#):** (coming soon!) deployed final production models -->

## Project Overview

This project applies Natural Language Processing (NLP) techniques to analyze the publicly submitted comments in response to the revised definition of "Waters of the United States" (WOTUS).

In early 2017, President Trump signed an Executive Order<sup>[1](#footnote1)</sup> requesting that agencies review a 2015 rule (The Clean Water Rule: defining "Waters of the United States") put in place under the Obama administration. The agencies, including the Environmental Protection Agency (EPA) and the Department of the Army, were instructed to rescind or replace the rule, in accordance with law.

The agencies have since conducted a reevaluation and revision of the definition of WOTUS. Their proposed rule redefined the scope of waters federally regulated under the Clean Water Act (CWA), and therefore adjusted which waterways now fall under federal authority. The proposed revisions were open for public comment for 60 days until April 15, 2019, and the revised rule took effect on December 23, 2019. With some exceptions, the comments generally fell into one of two buckets: they were either supportive of the proposed re-definition or opposed to changes to the 2015 rule.

This project analyzes the content of the comments that are publicly available in docket EPA-HQ-OW-2018-0149 on the [regulations.gov web page](https://www.regulations.gov/docket?D=EPA-HQ-OW-2018-0149).  This includes both unsupervised and supervised approaches with the goals to determine topics, examine clusters, and perform sentiment analysis.

## Data Collection and Analysis

The comments were collected by running a web-scraping program (`./scraper.py`) that builds in ample wait times so as not to overload the website with requests. It looped over all public submissions in the docket that weren't contained in an attachment. This resulted in an unlabeled dataset of just over 8K comments. Once the data were collected, a random sample of 1,200 comments were manually labeled, then a variety of Natural Language Processing (NLP) techniques were applied.

## Setting Up the Local Environment

This project uses the [Anaconda distribution](https://www.anaconda.com/distribution/) to manage Python packages. There are two separate environments with all necessary respective packages to run the web scraper (`./environment_webby.yml`) and the NLP analysis (`./environment_nlp.yml`). If you're using Anaconda as well, you can run the following commands to re-create either environment locally, then activate it.

```bash
# nlp environment to run analysis:
conda env create --file environment_nlp.yml
conda activate nlp

# webby environment to run the scraper:
conda env create --file environment_webby.yml
conda activate webby
```

(If you don't like the name of either environment, you can edit the first line of your local versions of the `.yml` files and change it to whatever name you'd prefer before creating it.)

For the scraper, because it uses the Selenium webdriver to control a browser, you'll also need to download the appropriate webdriver executable and add it to your local `PATH`. Some popular options are:

- [Firefox's geckodriver](https://github.com/mozilla/geckodriver/)
- [Chromium's chromedriver](https://sites.google.com/a/chromium.org/chromedriver/)
- [Other browser support](https://selenium.dev/documentation/en/getting_started_with_webdriver/browsers/)

To actually run the scraper, first clone the project and navigate to it in your local directory. Then use the following commands to activate the environment and run the scraper:

```bash
conda activate webby
python scraper.py
```

Depending on the system, the scraper takes \~1.5-2 days to run - there are over 8,000 comments and the program bakes in delay time to both allow the page to load and to space requests so as not to overload the website.

Note:

<a name="footnote1">1</a>: Executive Order 13778, signed on February 28, 2017, titled "Restoring the Rule of Law, Federalism, and Economic Growth by Reviewing the 'Waters of the United States' Rule"
