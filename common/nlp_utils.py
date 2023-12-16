from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from nltk.tokenize import word_tokenize
import nltk
from nltk.corpus import stopwords 
import pandas as pd
import numpy as np
import string 

##process string by camera name, lens when applicable?
#determine which model

def preprocess(text)-> list:
    """
    Preprocesses the given DataFrame by performing TF-IDF vectorization and splitting the data
    into training and testing sets for the Sold Price prediction.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing 'Listed Name' and 'Sold Price' columns.

    Returns:
    - tuple: A tuple containing X_train, X_test, y_train, y_test for model training and evaluation.
    """
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = nltk.word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    return ' '.join(filtered_tokens)
    

def train(X, y, model)-> LinearRegression:
    """
    Creates and trains a Linear Regression model using the provided training data and evaluates it
    on the test data. Prints the score of the model's performance.

    Parameters:
    - X_train: The feature matrix for training.
    - X_test: The feature matrix for testing.
    - y_train: The target labels for training.
    - y_test: The target labels for testing.

    Returns:
    - LinearRegression: Trained Linear Regression model.
    """
    vectorizer = CountVectorizer()
    X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = .2, random_state= 42)
    X_train_vectorized = vectorizer.fit_transform(X_train)
    X_test_vectorized = vectorizer.transform(X_test) 
    model.fit(X_train_vectorized, y_train)
    print(f'Model trained. Model Accuracy: {model.score(X_test_vectorized, y_test)}')
    return model

def model_creation_dt(*args) -> DecisionTreeRegressor:
    X_train, X_test, y_train, y_test = args
    model = DecisionTreeRegressor()
    model.fit(X_train, y_train)
    print(report_score(model, X_test, y_test))
    return model
    
def predict_lr(model:LinearRegression,X_test, y_test ):
    """
    Predicts 'Sold Price' using the provided trained Linear Regression model on test data.

    Parameters:
    - model (LinearRegression): The trained Linear Regression model.
    - X_test: The feature matrix for testing.
    - y_test: The target labels for testing.

    Prints the actual and predicted values for the first five samples in the test data.
    """
    for i in range(5):
        print(f'Actual: {y_test[i]}')
        print(f'Predicted {model.predict(X_test[i])}')

def report_score(model, X_test, y_test):
    return model.score(X_test, y_test)
    
