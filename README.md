# Analysis of Public Comments Regarding the EPA's Revised Definition of "Waters of the United States" (WOTUS)

## Overview

In early 2017, President Trump signed an Executive Order<sup>[1](#footnote1)</sup> requesting that agencies review a 2015 rule put in place by the Obama administration regarding the "Waters of the United States". The agencies, including the Environmental Protection Agency (EPA) and the Department of the Army, were instructed to rescind or replace the rule, in accordance with law.

The agencies have since conducted a reevaluation and revision of the definition of WOTUS. Their proposed rule redefined the scope of waters federally regulated under the Clean Water Act (CWA), and therefore adjusted which waterways now fall under federal authority. The proposed revisions were open for public comment for 60 days until April 15, 2019, and the revised rule took effect on December 23, 2019. With some exceptions, the comments generally fell into one of two buckets: they were either supportive of the proposed re-definition or opposed to changes to the 2015 rule.

This project analyzes the content of the comments that are publicly available in docket EPA-HQ-OW-2018-0149 on the [regulations.gov web page](https://www.regulations.gov/docket?D=EPA-HQ-OW-2018-0149). The comments were collected by running a web scraping program (`./scraper.py`) which looped over all public submissions in the docket that weren't contained in an attachment. This resulted in a dataset of just over 8K comments. Once the data were collected, a variety of Natural Language Processing (NLP) techniques were applied. These included topic analysis, clustering, and (after manually labeling a sample set) classification and sentiment analysis.

## Where to Find Project Analyses

- [WOTUS_analysis Jupyter notebook](./WOTUS_analysis.ipynb) for all underlying analysis and code relating to this project
- [Repository's GitHub page](https://data-science-for-conservation.github.io/WOTUS_Revision/) for topic analysis summary, interactive visualizations, and takeaways

<!--
You can review the full project write-up, including interactive models [here]().
-->

## Project Challenges

The challenges of this project fell into two broad categories - ones relating to data collection and ones associated with the nature of the dataset.

**Data Collection**

The project relied on a web scraper to collect the text of the comments. The regulations.gov website has an API to request data, however, only organizations (not individuals) qualify for an API key. Retrieving data programmatically through the API would have reduced the overall time to compile a dataset, and also potentially increased the number of comments collected. Approximately 3K of the available 11K comments in the docket were locked up in attachments (mostly PDF or image formats), whose content was outside the capabilities of my non-OCR, consumer-level PDF-converter software. There's a possibility that the text of those comments could be accessed through an API call.

Additionally, the 8K-comment dataset represents only a fraction of all public comments submitted during the comment period. The docket lists a total of >600K comments received, however, there are only 11K comments available under public submissions. The EPA and Army explained this discrepancy:

>Agencies review all submissions, however some agencies may choose to redact, or withhold, certain submissions (or portions thereof) such as those containing private or proprietary information, inappropriate language, or duplicate/near duplicate examples of a mass-mail campaign. This can result in discrepancies between this count and those displayed when conducting searches on the Public Submission document type.

In light of this and the 3K comments only available in attachment form, the project had to assume the 8K sample of comments used in the analysis are generally representative of the public's views. Given the missing data and the comment above about removing duplicates in a mass-mail campaign, it was necessary to apply caution in drawing any conclusions about the *proportions* of comments for or against the rule change. There could be thousands of members of an organization sending the same mass-mail form in support or against the rule change, but it would only show up once in the submissions.

**Nature of the Dataset**

The dataset is comprised of unstructured, unlabeled text, which offered its own challenges. The lack of labeled data restricted the analysis to unsupervised learning techniques at first. However, a sample of the comments were manually labeled to gauge perform classification and sentiment analysis. Of course, this further limited the size of the dataset and having more labeled observations would likely improve the performance of the models.

Not surprisingly, the pre-processing choices for how to convert the text to a numeric representation (the term-document matrix) impacted the outcome of the models. While this is measurable in supervised learning techniques by reviewing model performance, it was more of a challenge with the unsupervised models. Where possible, quantitative metrics were used to compare the different pre-processing approaches - these included `perplexity` in the topic analysis or `inertia` and `silhouette score` in the clustering analysis. However, at a certain point, there was a need for more qualitative and subjective measures (particularly with topic analysis) to determine what constituted the best results.

Finally, the overlap of the language used in many comments added to the challenge of finding distinct topics or clusters. Below are two excerpts - both mention agriculture and the need for clean water - but are on opposing sides of the issue:

>"I support clean water. We need clear rules on how this is to be accomplished. I personally try hard to have as little erosion as possible. Terraces, grass waterways, contour farming, no-till, headlands, etc. As hard as I and other farmers try to conserve and keep waters clean, we need clear rules with common sense to provide us direction. Hopefully this is a step in that direction and we all can work together to feed the world."

>"I stand for clean water! Clean and healthy waterways are key to western agriculture, recreation and tourist economies that support our communities. These wholesale changes to the Clean Water Act to limit its jurisdiction provide loopholes in the law and give polluters incentives to discharge dangerous pollutants into unprotected waterways. Please protect our water - the essence of life upon which we all depend!"

## Collecting the Data: Setting Up the Local Environment and Running the Scraper

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
