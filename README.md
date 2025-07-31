# NAO README.md

## Introduction
This is the STARI labs collection of programs for the NAOs.

## Instructions:
1. start running a model
```
ollama run [model_name:num_parameters]
```
2. ssh into the NAO
```
ssh nao@nao.local
```
3. run the python script in the scripts folder
```
cd scripts
python sendrequestLLM.py
```
### NAOv6 - Server Client llama2 Chat Bot (whisper STT & naoqi TTS)
1. scp LLM/client_llm.py to ~/scripts
```
scp LLM/client_llm.py nao@NAO_IP:~/scripts/
```
2. pip install
```
pip install -r LLM/requirements.txt
```
3. run llama2 on server PC
```
ollama run llama2
```
4. launch Flask application
```
python3 LLM/server_LLM.py
```
5. ssh into NAO
```
ssh nao@NAO_IP
```
6. run NAO program
```
python2 ~/scripts/client_llm.py
```