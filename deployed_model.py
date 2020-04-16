#!/usr/bin/env python3

import pickle
import streamlit as st


"""
TODO:
- Import model
- Lay out app page
- Get user input
- Show class and probability output
"""


# Import model
@st.cache
def get_model():
    with open('final_sentiment_clf.pkl', 'rb') as f:
        model = pickle.load(f)

    return model


st.markdown(
"""
# Model Demo

Welcome to the live version of the WOTUS sentiment classifier!

For a full overview and summary of the project, visit the [GitHub page here]()
or find the
[source code](https://github.com/Data-Science-for-Conservation/WOTUS_Revision)
that generated the model.
""")

sent_clf = get_model()

# TODO: Get user input
