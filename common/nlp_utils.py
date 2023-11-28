from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np

def setup(df:pd.DataFrame)-> LinearRegression:
    model = LinearRegression()
    print(type(model))
    tfidf_vectorizer = TfidfVectorizer()
    X = tfidf_vectorizer.fit_transform(df['Listed Name'])
    y = df['Sold Price']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size =.2, random_state = 42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    print(type(model))
    return model

def predict(model:LinearRegression):
    pass
    
