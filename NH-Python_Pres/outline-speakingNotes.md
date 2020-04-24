# A Survey of Natural Language Processing Techniques in Python


## Project Overview

- Project overview
    - Project examines public comments that were submitted for a proposed environmental rule change
    - Rule changes follow a set process
    - History: in 2015, under the Obama administration, the EPA ran a similar process to introduce 'The Clean Water Rule: Definition of "Waters of the United States"' (2015 rule) -> effectively broadened the scope of which waterways fell under CWA protection
    - The Clean Water Act: set of federal-level regulations that lay out the terms of engagement for industries for interactions with waterways under CWA-protection
        - Includes rules for discharging chemicals/pollutant, or fill/dredged materials, and rules for preventing oil spills
        - One part -> expanded definition to include waterways that are temporary or ephemeral in nature
        - Important in arid areas, environment (habitat, part or reproductive cycle for variety species fish/amphibians)
        - Pushback from industry - does this include an irriguation ditch? Also federal overreach (where draw line of States vs. Federal regs)
    - Fast forward to 2017, Trump takes office, issues executive order "Restoring the Rule of Law, Federalism, and Economic Growth by Reviewing the 'Waters of the United States' Rule".
        - EPA and Army to review 2015 rule, and revise/repeal as necessary
        - Repealed the 2015 rule, new definition of WOTUS taking effect in June (navigable waters protection rule)
    - Collected 8000 comments
        - Small fraction of 626K on site
    - Comments weren't a vote, so any sentiment I had to interpret and label myself
    - The comments weren't a random sample of Americans' views
        - Proactive process (find site, type comment), so polarized dataset (helps for sentiment analysis)
        - In general either supported rule change or opposed it, but some comments were off topic or hard to classify as a human reading them
- Different players and viewpoints
    - Supportive: industry groups (agriculture: farmers/ranchers, extraction industry (mining/oil & gas), developers
        - Scope of 2015 rule unclear and too broad
        - One comment: "I need to look at my land and know what waterways fall under CWA without having to hire consultant"
        - Landowners: federal overreach on property rights
    - Opposed: took various forms, but main theme was the current process to repeal 2015 rule sacrificing environmental protections in favor of industry/economy
        - Environmental/conservation groups
        - Concerned rule changes opens waterways to pollution
        - Important waterways no longer protected in arid states
        - Loss of protection on wetlands (critical habitat for biodiversity)
    - Political ones: "O'Bummer", Trump a buffoon - while entertaining to read, those comments sounded more similar to each other than either side of the level-headed ones
- Word clouds - little hokey and over-used, but good sanity check (no surprises)
    - Zoom in to see the more opinionated pairings
- Venn Diagram - so ML task should be easy, right?
- Potential Hazard, similar language, we'll see if the models can handle this

## What is Machine Learning?

- Get everyone on same page
- What is Machine Learning?
     - Model building, which makes a simple representation of a real-world system. Uses: make a prediction, simulate a process, or understand system better
     - "Machine" part is because uses a computer. Subset of Artificial intelligence - uses computation to perform a cognitive task
     - "Learning" part is where it differs from traditional model-buidling
         - Traditional: takes inputs, applies a set of rules or formulas to the inputs, and generates output
 - Machine Learning flips this paradigm on its head: still have input, but instead of writing formulas or rules to calculate output, the model has a task to perform and it uses the examples you've fed it in your data to learn the relationships/patterns/rules to perform the task
     - What the model outputs (solves for) depends on what the task is that it's trying to perform
 - ML Tasks:
     - Supervised Learning: most intuitive to understand, often taught first. Your data includes the outcome that going forward, you want to predict. In project, didn't start with labeled data, but goal was to predict supportive vs opposed comments
     - Unsupervised Learning: few 'families' of analysis, none require labeled data. Project applied clustering first as a proxy
     - Where spend time:
         - Supervised: up front getting labeled data, framing problem (right evaluation metric, want precise definition of what you're predicting) -> project sentiment supportive vs opposed NOT negative/positive. But save time on evaluation (easy to interpret results)
         - Unsupervised: models don't accept labels, problem more amorphous (finding structure), but more time on back end to analyze the results of the model - what makes this cluster similar?
- Where does NLP fit into ML?
     - NLP definition
         - Languages are tricky: while they have rules, they're constantly evolving, there are lots of exceptions, slang/idioms, one word can be different parts of speech and have different meanings (object-oriented programming, dramatic courtroom scenario "I object!")
         - Messy, hard for a machine to understand
         - Applications: speech recognition (virtual assistants), translation, understanding text (written word)
     - Text is import: everywhere -> main way humans communicate to each other online
        - News articles and blogs, social media posts, product reviews, forum discussions and comment threads
    - Contains a lot of information, great potential to add value in an ML system. NLP is set of tools to access that info
- How do machines consume data
    - Text is easy for humans to digest, but not optimal for machines (they prefer numbers)
    - ML models are very picky - not only want tabular, numeric data, but most can't handle missing values, some require or perform better when all numbers are on the same scale
- Project DS Stack: How to use ML in Python
- Project Workflow
    - Overall process is iterative
    - The "process text" phase is crux of converting our set of comments into a feature matrix - table a numbers that capture meaning from the text in some way
    - Not the most exciting part of NLP, but critical to do before can use model
    - Split data into training set
    - Step 1: Tokenize each comment, which is breaking it down into base units (tokens). Think of a token as words - I used NLP library spaCy's tokenizer, which has built-in rules that were a little more sophisticated than the scikit-learn regular expression
    - Step 2: Lemmatizing - this takes different variations of the same word (think different tenses of verbs) and converts them all into their base form -> condenses feature set
    - Step 3: covered in word clouds, removes most frequent words in language (and, the, from, this, etc.). Optional step, depends on type of model you're using. Neural networks can handle complexity, and while stop words don't add a lot of meaning, do have grammatical value
    - Finally, Vectorizing actually converts the tokens into a numeric representation
        - Bag of Words: I used several variations, each one basically makes each token a feature column, then it counts or takes a frequency
- Vectorizer Comparison
    - Vectorizers calculate counts or frequencies of document tokens
    - Word vectors - there's pre-trained neural network that found a numeric representation of words that preserve some semantic meaning. This method averages each word vector per document
    - Pros and cons with any decision you make - needs to fit your project


## Clustering

- Overview
    - Clustering was done before data sample was labeled
    - Recall it's an unsupervised technique that finds groups of comments based on similarity
    - Goal was to see if a clustering model could segment the data based on sentiment
    - With clustering models, you the user provide the number of clusters you want it to find
    - Steps [see pres]
    - Example data: demo to show to evaluate each model. I fed the points into a KMeans algorithm, ran the model using different numbers of clusters, then plotted the metrics
- Examine cluster example
    - Inertia is a distance calculation - total sum of each point's distance to it's cluster's center. Generally lower is better, but the more clusters you add, it will continue to reduce inertia. So you look for the "elbow" where adding a new cluster doesn't reduce the metric much - it's the point of diminishing returns so to speak
    - Middle multiplies the inertia by the cluster number to penalize adding another cluster. Look for the minimum
    - Right silhouette score compares two sets of distances: the intra-cluster (distance between points in same cluster) and the distances to next nearest cluster. Closer to one is good
- Code Example - easy to do this in few lines of code in scikit-learn
- Comparison of model metrics -> generally get min at 2 clusters in middle chart, low silhouette scores for TFIDF/HashL2, better with Count and WordVec
- Examine clusters - seems to be underlying structure in data, but cluster colors not aligned with it
- Overlay labeled comments, can see that clusters have lot of overlap


## Sentiment Analysis

- Supervised technique, required labeled data. Overview of steps Round I (try many models "off the shelf", don't know what will work best with data), Round II (fine tune winners' circle to find best performer)
- Round I models, quick overview of each
- Round I outcome - takeaways: word vectors didn't crack top half, Random Forest outperformed XGBoost, all top models used simpler vectorizers
- Round II models, parameters tuned
- Round II outcome, Logistic Regression with TFIDF was winner
- Demo winning model

## Conclusions

- Language is nuanced, and teaching a model to recognize people's opinions (which I've been calling sentiment) was difficult in the unsupervised task, but easier in the supervised one. So examining it more:
    - Our vectorization techniques (counting words or averaging semantic values of words) all removed the *context* that those words happened in
    - The overlapping language and lack of context made it difficult for the clustering model to perform as we were hoping - as a proxy for a classifier without having to do the work of labeling data
    - On the other hand, the supervised learning models used the same vectorized data, but because we gave it a target to hit (the labels), they were able to find alternative underlying patterns to distinguish the comments
- In this case, the comments used similar enough language that the machine needed that supervised guidance to find the right way to distinguish comments
