import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import argparse

from tools.utils import use_calculator
from dataset import get_data, TestDataset

def sample(model, problem, tokenizer, device, num_request, add_text_len):
    EQUALS_TOKENS = set([28, 796, 47505])

    ori_text = problem
    for _ in range(num_request):
        with torch.no_grad():
            tokens = tokenizer([problem], padding=False, return_tensors="pt").to(device)
            text_len = tokens["input_ids"].shape[1]

            out = model.generate(
                **tokens, max_length=text_len + add_text_len, pad_token_id=model.config.eos_token_id
            )
            text = tokenizer.batch_decode(out)[0]

            if out[0, -1].item() in EQUALS_TOKENS:
                answer = use_calculator(text)
                if answer is not None:
                    text = text + str(answer) + ">>"
            problem = text
    return {"full_text": problem, "answer": problem[len(ori_text):]}

def main(args):
    device = torch.device("cuda")
    tokenizer = GPT2Tokenizer.from_pretrained(args.load)
    model = GPT2LMHeadModel.from_pretrained(args.load)
    model.to(device)
    print("Model Loaded")

    test_examples = get_data(args.data)
    results = []
    for problem in test_examples:
        ques = problem["Problem"]
        len_quest = 10 #hyperparameter
        add_text = 1 #hyperparameter
        print(ques.strip())
        results.append(sample(model, ques, tokenizer, device, len_quest, add_text))
    
        print(results[-1]["answer"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
		"--load", type=str, 

		default="AlexWortega/taskGPT2-xl-v0.2a",
		help="Name or path to model"
	)
    parser.add_argument(
		"--data", type=str, 

		default="./data/test.json",
		help="Path to data test"
	)

    args = parser.parse_args()
    main(args)

