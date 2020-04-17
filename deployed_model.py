#!/usr/bin/env python3

import pickle
import pandas as pd
import streamlit as st


@st.cache
def get_clf_model():
    with open('final_sentiment_clf.pkl', 'rb') as f:
        model = pickle.load(f)

    return model


st.title('Sentiment Classifier Demo')
st.markdown(
"""
Welcome to the live version of the WOTUS sentiment classifier!

Enter your comment about the EPA and Army's proposed re-definition of "Waters
of the United States" and see whether the model classifies it as "Opposing" or
"Supportive" of the rule change. The model also outputs the probability (or
confidence) it assigns to that label.

Additional project resources include a full
[project writeup](https://data-science-for-conservation.github.io/WOTUS_Revision/)
or the
[source code](https://github.com/Data-Science-for-Conservation/WOTUS_Revision)
that generated the model.
""")

sent_clf = get_clf_model()

classes = {0: "Opposing",
           1: "Supportive"}


def run_sent_analysis(comment):
    pred = sent_clf.predict_proba(comment)
    label = classes[pred[0].argmax()]
    prob = round(pred[0].max(), 3)

    results = pd.DataFrame([label, prob],
                           index=['Sentiment', 'Confidence'],
                           columns=['Value'])

    return results


comment = st.text_area('Enter your comment here',
    """
    It is important for water quality to protect our wetlands and waterways.
    We should be increasing protection not decreasing it.
    """)

try:
    result = run_sent_analysis(comment)
    st.table(result)
except ValueError as e:
    st.write(e)
