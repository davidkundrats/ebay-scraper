from sklearn.model_selection import train_test_split
from transformers import BertTokenizer

##process string by camera name, lens when applicable?
#determine which model

def preprocess(text)-> list:
    """
    Preprocesses the given text using BERT tokenizer.

    Parameters:
    - text (str): The input text to be tokenized and encoded.

    Returns:
    - list: A list containing the encoded tokens of the input text.
    """
    
    bert_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', padding = True)
    tokenized_text = bert_tokenizer.tokenize(text)
    encoded_text = bert_tokenizer.encode(tokenized_text)
    return encoded_text
