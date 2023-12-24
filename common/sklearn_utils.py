from sklearn.linear_model import LinearRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import mean_squared_error, r2_score

def preprocess_sk(text):
    vectorizer = TfidfVectorizer()
    return vectorizer.fit_transform(text)

def train_sk(X_train, y_train, model):
    model.fit(X_train, y_train)
    return model

def print_scores(X_train, X_test,y_train,  y_test, model):
    print(f'Score on training data: {model.score(X_train, y_train)}')
    print(f'Score on testing data: {model.score(X_test, y_test)}')
    pred = model.predict(X_test)
    mse = mean_squared_error(y_test, pred)
    r2 = r2_score(y_test, pred)
    print(f'Mean squared error: {mse}\nR2 score: {r2}') 
    
    
