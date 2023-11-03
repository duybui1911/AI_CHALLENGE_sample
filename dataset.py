import json
import os
import re
import torch


def read_jsonl(path: str):
    with open(path) as f:
        data = json.load(f)
        return data


def get_data(path):
    '''
        If there are many json files to load:
        path_item = os.path.join("data/", f"{path}.jsonl")
        data_item = read_jsonl(path_item)
    ''' 
    data = read_jsonl(path)

    for ex in data:
        if ex["options"] != "":
            ex.update(Problem=ex["Problem"] + "\n Options: " + ex["options"])
        else:
            ex.update(Problem=ex["Problem"] + "\n" + "The answer to the question is:")
        #ex.update(answer=ex["answer"] + "<|endoftext|>")
        # Update the diagramRef tokenizer method here

    print(f"Loaded {len(data)} examples")
    return data

class TestDataset(torch.utils.data.Dataset):
    '''
        tokenizer: is a text -> token converter for model input
        data: is the data loaded from the "get_data" function
    '''
    def __init__(self, tokenizer, data, loss_on_prefix=True):
        self.data = data
        self.problems = [ex["Problem"] for ex in self.data]
        self.answer = [ex["answer"] for ex in self.data]
        self.problems = tokenizer(self.problems, padding=False)
        self.answer = tokenizer(self.answer, padding=False)
        self.loss_on_prefix = loss_on_prefix
        self.max_len_of_items = max(
            [
                len(self.problems["input_ids"][i]) + len(self.answer["input_ids"][i])
                for i in range(len(self.data))
            ]
        )
        #print(f"Max tokens: {self.max_len}")

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        qn_tokens = self.problems["input_ids"][idx]
        answer_tokens = self.answer["input_ids"][idx]
        pad_tokens = [0] * (self.max_len_of_items - len(qn_tokens) - len(answer_tokens))
        tokens = qn_tokens + answer_tokens + pad_tokens
        mask = (
            ([int(self.loss_on_prefix)] * len(qn_tokens))
            + ([1] * len(answer_tokens))
            + ([0] * len(pad_tokens))
        )
        tokens = torch.tensor(tokens)
        mask = torch.tensor(mask)
        return dict(input_ids=tokens, attention_mask=mask)
