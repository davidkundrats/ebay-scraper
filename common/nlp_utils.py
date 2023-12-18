from sklearn.model_selection import train_test_split
from transformers import BertTokenizer

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
    
    bert_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', padding = True)
    tokenized_text = bert_tokenizer.tokenize(text)
    encoded_text = bert_tokenizer.encode(tokenized_text)
    return encoded_text
