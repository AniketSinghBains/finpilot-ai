import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

def train_model():

    df = pd.read_csv("data/expense_training.csv")

    X = df["description"]
    y = df["category"]

    vectorizer = CountVectorizer()
    X_vec = vectorizer.fit_transform(X)

    model = MultinomialNB()
    model.fit(X_vec, y)

    return model, vectorizer


def predict_category(text):

    model, vectorizer = train_model()

    text_vec = vectorizer.transform([text])

    prediction = model.predict(text_vec)

    return prediction[0]
