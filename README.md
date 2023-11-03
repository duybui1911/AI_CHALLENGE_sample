# AI_CHALLENGE_sample
Collaborative competition co-organized between [Applied Mathematics and Informatics Club ](https://www.facebook.com/AMIC.HUST) and [Google Developer Student Club - HUST](https://www.facebook.com/gdsc.hust), under the permission of Hanoi University of Science and Technology.

## Installation
```
pip3 install -r requirements.txt
```

## For loading model from [huggingface](https://huggingface.co/) or local:
```
python3 for_load_model.py --load [name or link model] --data [path to dataset]
```

## For request API
Change API KEY in file `openai_api_ket.txt` and run
```
python3 for_use_api.py --model_name [name model to request] --data [path to dataset]
```