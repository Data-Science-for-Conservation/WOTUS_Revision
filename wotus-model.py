#!/usr/bin/env python3

import pickle
import random
import numpy as np
import pandas as pd
from sklearn.preprocessing import normalize
import streamlit as st


def main():
    st.title('Sentiment Classifier and Similarity Analysis Demo')
    st.markdown(
    """
    Welcome to the live versions of the WOTUS models!

    ## Sentiment Classifier

    Enter your comment about the EPA and Army's proposed re-definition of
    "Waters of the United States" and see whether the model classifies it as
    "Opposing" or "Supportive" of the rule change. The model also outputs the
    probability (or confidence) it assigns to that label.
    """)

    sent_clf = get_clf_model()

    classes = {0: "Opposed",
               1: "Supportive"}

    ex_comments = {1: 'It is important for water quality to protect our '
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

    ex_c = ex_comments[random.choice(range(1, 6))]

    comment = st.text_area('Enter your comment here', ex_c)

    try:
        pred = sent_clf.predict_proba([comment])
        label = classes[pred[0].argmax()]
        prob = pred[0].max()

        results = pd.DataFrame([label, prob],
                               index=['Sentiment', 'Confidence'],
                               columns=['Value'])

        subset = pd.IndexSlice['Confidence', 'Value']

        st.table(results.style.applymap(color_green,
                                        subset=subset)
                              .format('{:.3f}',
                                      subset=subset))

    except ValueError as e:
        st.write(e)

    # NMF Cosine Similarity
    nmf_pipe = get_nmf_model()
    X_all_labeled, y_all_labeled = get_all_labeled_comments()

    try:
        feats_df = get_nmf_feats(X_all_labeled, nmf_pipe)
        similarities = cosine_sim(feats_df, nmf_pipe, comment)
        df_n_largest = get_n_sims_w_labels(similarities, y_all_labeled, 5)

        st.markdown("## Five Most Similar Comments in the Labeled Dataset")

        for idx, row in df_n_largest.iterrows():
            st.write('**Comment Text:**', row['Comment'])
            st.write('**Cosine Similarity:**',
                     round(row['Cosine Similarity'], 3))
            st.write('**Label:**', row['Label'])
            st.write('-----------')
    except ValueError as e:
        pass

    st.markdown(
    """
    Additional project resources include a full
    [project writeup](https://data-science-for-conservation.github.io/WOTUS_Revision/)
    or the
    [source code](https://github.com/Data-Science-for-Conservation/WOTUS_Revision)
    that generated the model.
    """)


@st.cache(allow_output_mutation=True)  # Changes caused by .predict() ok
def get_clf_model():
    """
    Loads pre-trained pickled model
    :return: scikit-learn pipeline including vectorizer and model
    """
    with open('final_sentiment_clf.pkl', 'rb') as f:
        model = pickle.load(f)

    return model


@st.cache(allow_output_mutation=True)  # Changes caused from applying model ok
def get_nmf_model():
    """
    Loads pre-trained pickled model
    :return: scikit-learn pipeline including a vectorizer and NMF model
    """
    with open('nmf_pipe.pkl', 'rb') as f:
        nmf_pipe = pickle.load(f)

    return nmf_pipe


@st.cache()
def get_all_labeled_comments():
    """
    Loads two DataFrames for the entire set of labeled comments
    :param path: a path to the pickled dataset
    :return: two DataFrames, X_all_labeled has original index and the comments,
        y_all_labeled has the comment text as the index and the labels
    """
    lab_comments = pd.read_pickle('./Data/comments_word_labels.pkl')

    X_all_labeled = lab_comments.drop('Support_Rule_Change', axis=1)
    y_all_labeled = lab_comments.set_index('Comment')
    y_all_labeled.columns = ['Label']

    return X_all_labeled, y_all_labeled


def color_green(val):
    """
    Takes a scalar, returns a string with the CSS
    property `'color: green'`
    """
    # color = 'green' if type(val) == np.float64 else 'black'
    # return f'color: {color}'
    return 'color: green'


def get_nmf_feats(X_all_labeled, nmf_pipe):
    """
    :param X_all_labled: DataFrame with text for all labeled comments
    :param nmf_pipe: trained scikit-learn pipeline including a vectorizer and
        NMF model that can handle raw text
    :return: DataFrame of the labeled comments that have been run through the
        NMF model, then normalized, and the index contains the original comment
        text
    """

    # Use pipeline to transform the set of all labeled comments
    W1 = nmf_pipe.transform(X_all_labeled['Comment'])
    norm_feats = normalize(W1)
    feats_df = pd.DataFrame(norm_feats, index=X_all_labeled['Comment'])

    return feats_df


def cosine_sim(feats_df, nmf_pipe, comment):
    """
    :param feats_df: DataFrame of normalized NMF model values with comment text
        as index
    :param nmf_pipe: a vectorizer-NMF pipeline to process `comment`
    :param comment: str, the comment to use to find other similar ones to in
        the training set
    :return: pd.Series of the dot product of feats_df and processed comment
    """
    a = nmf_pipe.transform([comment])
    a = normalize(a)
    similarities = feats_df.dot(a[0])

    return similarities


def get_n_sims_w_labels(similarities, y, n_largest):
    """
    Concatenates the cosine similarities with labeled comments and returns a
        DataFrame with the n-largest most similar comments
    :param similarities: DataFrame of the dot product of a comment with all
        dataset comments (aka the cosine value)
    :param y: DataFrame with labeled comments as the index and one column with
        the comment label (0=Opposed, 1=Supportive of the rule change)
    :param n_largest: int indicating the number of most similar comments to
        retrieve
    :return: DataFrame of n_largest items with columns for 'Comment', 'Cosine
        Similarity' score, and 'Label' of the comment

    """
    df = pd.concat([similarities, y], axis=1).reset_index()

    df.columns = ['Comment', 'Cosine Similarity', 'Label']

    df.sort_values(by=['Cosine Similarity'],
                   axis=0,
                   ascending=False,
                   inplace=True)

    return df.head(n_largest)


if __name__ == '__main__':
    main()
