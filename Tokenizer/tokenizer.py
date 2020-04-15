import spacy


def external_spacy_tokenizer(doc):
    """
    Applies spaCy's built-in tokenizer pipeline capabilities to
        to keep a lemmatized version of each token for alpha-
        numeric word's only (excludes punctuation and whitespace)
    :param doc: string
    :return: list of lemmatized tokens found in `doc`
    """
    lemmatizer = spacy.lang.en.English()
    tokens = lemmatizer(doc)
    return([token.lemma_ for token in tokens
            if token.lemma_.isalnum()])
