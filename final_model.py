import pickle
import pandas as pd
from sklearn.preprocessing import normalize
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.decomposition import NMF
from sklearn.linear_model import LogisticRegression
import spacy

# from Tokenizer.tokenizer import external_spacy_tokenizer


def get_X_train_comments(path):
    X_train = pd.read_pickle(path)
    return X_train


def get_all_labeled_comments(path):
    lab_comments = pd.read_pickle(path)
    X_all_labeled = lab_comments.drop('Support_Rule_Change', axis=1)
    y_all_labeled = pd.Series(lab_comments['Support_Rule_Change'],
                              index=X_all_labeled['Comment'],
                              name='Label')
    return X_all_labeled, y_all_labeled


def get_upsamp_labeled_comments(path):
    upsampled = pd.read_pickle(path)
    X_up_train = upsampled.drop('Support_Rule_Change', axis=1)
    y_up_train = upsampled['Support_Rule_Change']
    return X_up_train, y_up_train


# def load_lang_model():
#     return spacy.load('en_core_web_sm',
#                       disable=['tagger', 'parser', 'ner'])


# def get_stop_words(nlp):
#     stop_words = list(nlp.Defaults.stop_words)
#     return external_spacy_tokenizer(' '.join(stop_words))


def tokenizer(doc):
    """
    Applies spaCy's built-in tokenizer pipeline capabilities to
        to keep a lemmatized version of each token for alpha-
        numeric non-stop words only (excludes punctuation and whitespace)
    :param doc: string
    :return: list of lemmatized tokens found in `doc`
    """
    nlp = spacy.load('en_core_web_sm',
                     disable=['tagger', 'parser', 'ner'])
    return ([token.lemma_ for token in nlp(doc)
             if (token.lemma_.isalnum() and not token.is_stop)])


def train_sent_clf(X_up, y_up, tokenizer, stop_words):
    tf_vec = TfidfVectorizer(tokenizer=tokenizer,
                             stop_words=stop_words,
                             max_df=0.90,
                             min_df=5)

    clf_pipe = make_pipeline(tf_vec,
                             LogisticRegression(C=5,
                                                n_jobs=-1,
                                                random_state=42))

    clf_pipe.fit(X_up['Comment'], y_up)

    return clf_pipe


def train_nmf_model(X, tokenizer, stop_words):
    count_vec = CountVectorizer(tokenizer=tokenizer,
                                stop_words=stop_words,
                                max_df=0.90,
                                min_df=5)

    nmf = NMF(n_components=8,
              random_state=42)

    nmf_pipe = make_pipeline(count_vec, nmf)

    nmf_pipe.fit(X['Comment'])

    return nmf_pipe


def get_nmf_feats(X, nmf_pipe):
    W1 = nmf_pipe.transform(X['Comment'])
    norm_feats = normalize(W1)
    feats_df = pd.DataFrame(norm_feats, index=X['Comment'])

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
    df = pd.concat([similarities, y],
                   axis=1,
                   columns=['Comment', 'Cosine Sim', 'Label']).reset_index()

    df.sort_values(by='Cosine Sim', axis=1, ascending=False, inplace=True)

    return df.head(n_largest)


def main():
    # Data paths
    upsamp_path = './Data/upsamp_train.pkl'
    X_train_path = './Data/X_train.pkl'
    all_lab_path = './Data/full_labeled.pkl'

    # Load language model, get stop words list for tokenizers
    # nlp = load_lang_model()
    # ex_tokenized_stop_words = get_stop_words(nlp)

    X_up, y_up = get_upsamp_labeled_comments(upsamp_path)

    print('Training Sentiment CLF')

    sent_clf = train_sent_clf(X_up, y_up,
                              tokenizer,
                              None)

    test_comment = """This revision removes bodies of water that are important
    for pollution filtration, nutrient cycling, among other ecosystem services.
    We need to make sure important water resources like wetlands are protected
    from degradation!"""

    print(sent_clf.predict_proba([test_comment]))

    with open('sent_clf_scriptmod.pkl', 'wb') as f:
        pickle.dump(sent_clf, f)

    print('Sentiment Classifier - > DONE')
    # print('-' * 50)
    # print('Training NMF Model')

    # Train NMF on all comments, apply to labeled-only
    # X_train = get_X_train_comments(X_train_path)
    # X_all_labeled, y_all_labeled = get_all_labeled_comments(all_lab_path)

    # nmf_pipe = train_nmf_model(X_train,
    #                            tokenizer,
    #                            None)

    # feats_df = get_nmf_feats(X_all_labeled, nmf_pipe)
    # similarities = cosine_sim(feats_df, nmf_pipe, test_comment)
    # df_n_largest = get_n_sims_w_labels(similarities, y_all_labeled, 5)

    # print(df_n_largest)


if __name__ == '__main__':
    main()
