import torch
from torch.utils.data import DataLoader, TensorDataset
from transformers import BertForSequenceClassification, BertTokenizer
from torch.optim import AdamW
##process string by camera name, lens when applicable?
#determine which model

def preprocess(text, max_length = 40):
    """
    Preprocesses the given text using BERT tokenizer.

    Parameters:
    - text (str): The input text to be tokenized and encoded.

    Returns:
    - list: A list containing the encoded tokens of the input text.
    """
    bert_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    input_ids = []
    attention_mask = []
    
    encoded_dict = bert_tokenizer.encode_plus(
        text,                     
        add_special_tokens=True,  
        max_length=max_length,    
        padding='max_length',   
        return_attention_mask=True,
        truncation=True,
        return_tensors='pt',       
    )

    return encoded_dict

def train(preprocessed_vector, target_vector, num_epochs=00):
    input_ids = torch.tensor(preprocessed_vector).type(torch.LongTensor) 
    labels = torch.tensor(target_vector).type(torch.FloatTensor).unsqueeze(1)  

    model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=1)

    dataset = TensorDataset(input_ids, labels)
    data_loader = DataLoader(dataset, batch_size=32, shuffle=True)

    loss_fn = torch.nn.MSELoss()
    optimizer = AdamW(model.parameters(), lr=2e-5) 

    for epoch in range(num_epochs):
        model.train()
        total_loss = 0
        
        for batch in data_loader:
            b_input_ids, b_attention_masks, b_labels = batch
            b_labels = b_labels.float()
            model.zero_grad()

            outputs = model(b_input_ids)
            
            logits = outputs.logits
            print(logits.size())
            loss = loss_fn(logits, b_labels)
            total_loss += loss.item()

            loss.backward()

        # Optional: Gradient Clipping
        # torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)

            optimizer.step()

        avg_loss = total_loss / len(data_loader)
        print(f'Epoch: {epoch + 1}, Average Loss: {avg_loss}')

    model.save_pretrained('./ebay_scrape_model')

def tokenize(batch):
    tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
    return tokenizer(batch['text'], padding = True)
