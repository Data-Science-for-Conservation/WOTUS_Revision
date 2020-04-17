#!/usr/bin/env python3

import pickle
import random
import pandas as pd
import streamlit as st


@st.cache(allow_output_mutation=True)
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


example_comments = {1: 'It is important for water quality to protect our '
                       'wetlands and waterways. We should be increasing '
                       'protection not decreasing it.',
                    2: 'Clean water is the most important resource we have! '
                       'We should be protecting our waterways even more, not '
                       'opening them up for even less regulation.',
                    3: 'The amended WOTUS document is a much improved rewrite '
                       'of the most damaging document on regulating water '
                       'ever written for agriculture. I support this new '
                       'revised document on WOTUS.',
                    4: 'I support clean water and clear rules for WOTUS. We '
                       'need common-sense regulations to continually improve '
                       'our environmental performance. With the new proposed '
                       'water rule, there will be clear and specific '
                       'guidelines for me to follow. I strongly support the '
                       'proposed rule; clean water is important to farms '
                       'everywhere.',
                    5: 'Dear EPA,It has come to my attention that the Clean '
                       'Water Act is under attack. Please preserve it as it '
                       'is. It has done a wonderful job of protecting our '
                       'water resources! The Clean Water Act is the bedrock '
                       'environmental policy that protects Americans with '
                       'basic limits on industrial pollution of our waters. '
                       'It has had strong bipartisan support since it was put '
                       'in place nearly 50 years ago.'}

ex_c = example_comments[random.choice(range(1, 6))]

comment = st.text_area('Enter your comment here', ex_c)

try:
    result = run_sent_analysis([comment])
    st.table(result)
except ValueError as e:
    st.write(e)

st.markdown(
"""
Additional project resources include a full
[project writeup](https://data-science-for-conservation.github.io/WOTUS_Revision/)
or the
[source code](https://github.com/Data-Science-for-Conservation/WOTUS_Revision)
that generated the model.
""")
