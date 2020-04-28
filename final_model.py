"""
Script to re-create the final models prototyped in the WOTUS_analysis.ipynb
    notebook and save to pickled objects for the web app to run.
"""

import pickle
import pandas as pd
from sklearn.preprocessing import normalize
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.decomposition import NMF
from sklearn.linear_model import LogisticRegression

from Tokenizer.tokenizer import external_spacy_tokenizer as tokenizer


TRAIN_SENT_CLF = True
TRAIN_NMF = True
SAVE_MODELS = False


def main():
    # Data paths
    upsamp_path = './Data/upsamp_train.pkl'
    X_train_path = './Data/X_train.pkl'
    all_lab_path = './Data/comments_labeled.pkl'

    test_comment = """This revision removes bodies of water that are important
        for pollution filtration, nutrient cycling, among other ecosystem
        services. We need to make sure important water resources like wetlands
        are protected from degradation!"""

    if TRAIN_SENT_CLF:
        print('-' * 50)
        print('Training Sentiment Classifier')

        # Train sentiment classifier
        X_up, y_up = get_upsamp_labeled_comments(upsamp_path)

        tf_vec = TfidfVectorizer(tokenizer=tokenizer,
                                 stop_words=None,
                                 max_df=0.90,
                                 min_df=5)

        clf_pipe = make_pipeline(tf_vec,
                                 LogisticRegression(C=5,
                                                    n_jobs=-1,
                                                    random_state=42))

        clf_pipe.fit(X_up['Comment'], y_up)

        print(test_comment)
        print('Model prediction:')
        print(clf_pipe.predict_proba([test_comment]))

        if SAVE_MODELS:
            with open('sent_clf_scriptmod.pkl', 'wb') as f:
                pickle.dump(clf_pipe, f)

        print('Sentiment Classifier - > DONE')

    if TRAIN_NMF:
        print('-' * 50)
        print('Training NMF Model')

        # Train NMF on all comments, apply to labeled-only
        X_train = get_X_train_comments(X_train_path)
        X_all_labeled, y_all_labeled = get_all_labeled_comments(all_lab_path)

        count_vec = CountVectorizer(tokenizer=tokenizer,
                                    stop_words=None,
                                    max_df=0.90,
                                    min_df=5)

        nmf = NMF(n_components=8,
                  random_state=42)

        nmf_pipe = make_pipeline(count_vec, nmf)

        nmf_pipe.fit(X_train['Comment'])

        print('NMF model -> DONE')

        if SAVE_MODELS:
            with open('nmf_pipe.pkl', 'wb') as f:
                pickle.dump(nmf_pipe, f)

        print('Getting similarity matrix')

        feats_df = get_nmf_feats(X_all_labeled, nmf_pipe)
        similarities = cosine_sim(feats_df, nmf_pipe, test_comment)
        df_n_largest = get_n_sims_w_labels(similarities, y_all_labeled, 5)

        print(df_n_largest)
        print(df_n_largest['Cosine Similarity'])


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


def get_X_train_comments(path):
    """
    Loads a DataFrame containing the full training set of comments
    :param path: a path to the pickled dataset
    :return: DataFrame
    """
    X_train = pd.read_pickle(path)

    return X_train


def get_all_labeled_comments(path):
    """
    Loads two DataFrames for the entire set of labeled comments
    :param path: a path to the pickled dataset
    :return: two DataFrames, X_all_labeled has original index and the comments,
        y_all_labeled has the comment text as the index and the labels
    """
    lab_comments = pd.read_pickle(path)

    X_all_labeled = lab_comments.drop('Support_Rule_Change', axis=1)
    y_all_labeled = lab_comments.set_index('Comment')
    y_all_labeled.columns = ['Label']

    return X_all_labeled, y_all_labeled


def get_upsamp_labeled_comments(path):
    """
    Loads two DataFrames for the up-sampled labeled training set
    :param path: a path to the pickled dataset
    :return: two DataFrames, X_up_train includes comment text, y_up_train
        includes labels
    """
    upsampled = pd.read_pickle(path)

    X_up_train = upsampled.drop('Support_Rule_Change', axis=1)
    y_up_train = upsampled['Support_Rule_Change']

    return X_up_train, y_up_train


if __name__ == '__main__':
    main()
