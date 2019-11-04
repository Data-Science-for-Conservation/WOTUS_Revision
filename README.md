# Analysis of Public Comments Regarding the EPA's Revised Definition of "Waters of the United States" (WOTUS)

In early 2017, President Trump signed an Executive Order<sup>[1](#footnote1)</sup> requesting that agencies review a 2015 rule regarding the "Waters of the United States". The agencies, including the Environmental Protection Agency (EPA) and the Department of the Army, were instructed to rescind or replace the rule, in accordance with law.

The agencies have since conducted a reevaluation and revision of the definition of "Waters of the United States". Their proposed rule redefines the scope of waters federally regulated under the Clean Water Act (CWA). This rule was open for public comment until April 15, 2019.

This project aims to analyze the content of comments that are publicly available on the [regulations.gov web page](https://www.regulations.gov/docket?D=EPA-HQ-OW-2018-0149) for this docket. It runs a web scraping program (`./scraper.py`) to loop over all docket public submissions that didn't contain an attachment, collect the text of the comment, then save each as a text file under `./Data/Comments/`. It then applies Natural Language Processing (NLP) techniques using a combination of [Scikit-Learn, NLTK and spaCy].

## Setting Up the Environment to Run the Scraper

This project uses the [Anaconda distribution](https://www.anaconda.com/distribution/) to manage Python packages. An environment with all necessary packages to run `scraper.py` is saved in `./environment.yml`. Run the following commands from your local project directory to create the `webby` environment locally, activate it, then run the scraper:

```bash
conda env create --file environment.yml
conda activate webby
python scraper.py
```

(If you don't like the name `webby`, you can edit the first line of your local version of the `environment.yml` file and change it to whatever name you'd prefer.)

Depending on the system, the scraper takes \~1 day to run - there are over 8,000 comments and the program bakes in delay time to allow the page to load.

Notes:

<a name="footnote1">1</a>: Executive Order 13778, signed on February 28, 2017, titled "Restoring the Rule of Law, Federalism, and Economic Growth by Reviewing the 'Waters of the United States' Rule"
