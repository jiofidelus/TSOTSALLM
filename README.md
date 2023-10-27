# TSOTSALLM: Large Language Models at large scales

TSOTSALLM is an LLM obtained after fine tuned llama2 with 7B parameters. the public repository of this LLM is here [meta-llama/Llama-2-7b-hf](https://huggingface.co/meta-llama/Llama-2-7b)
you can see more summary about TSOTSALLM on [Read summary](./TSOTSALLM.md)

<!-- setup development enviroment -->
## Development Enviroment

### Operating System

This pproject can run om:

* Linux distribution but we used Ubuntu 20.04
* Mac Os
* Windows

### Code Editor

* Visual Studio Code
* google Colab

### Install Dependancies

To reproduce this project locally make sure your have Python3 install on your device.
if you don't have python install on your device you can follow this link [Download python](https://www.python.org/downloads/)

After installed python3, open your terminal to install dependance of the project

* Firstly, clone the project:
  
```bash
git clone https://github.com/jiofidelus//TSOTSALLM.git
cd TSOTSALLM/toy_submission/llama_recipes
```

* Secongly, create virtual environment

```bash
pip install virtualenv
python -m venv venv
```

* Activate your environment
  
```bash
source venv/bin/activate
```

* Install project dependencies
  
```bash
pip install -r requirements.txt
pip install -r fast_api_requirements.txt
```

## Run Project

To Run the project make sure your A100 GPU (40GB) is availble.
if all is okay, you can run project via docker or simple execution of the train file.

* With Docker <br/>
  the project have two Docker file: [docker train](/toy_submission/llama_recipes/Dockerfile) and [docker inference](/toy_submission/llama_recipes/Dockerfile.inference)

  Train dataset navigate inside of the [docker train file](/toy_submission/llama_recipes/Dockerfile)
  inside you can replace the token and repository by your own repository and token

  To make inference navigate inside of the Train dataset navigate inside of the [docker inference file](/toy_submission/llama_recipes/Dockerfile)
  inside you can replace the token and repository by your own repository and token

  Go on [Docker Readme](/toy_submission/llama_recipes/README.md) to see how you can do to train model and make inference using DockerFile


* Train dataset with commande line
  
```bash
python train.py --model-name meta-llama/Llama-2-7b-hf --hf_rep yvelos/Tsotsallm-evaluation --output_dir /temp/model/Tsotsallm
```

NB: You can replace the arguments values by your own values. if you choose second method to train datase, you should create and <strong>.env file </strong> in your project and paste theses line in:

```bash
HUGGINGFACE_TOKEN="YOUR_TOKEN"
HUGGINGFACE_REPO="YOUR_USERNAME/YOUR_REPO"
```

Replace the value of these environments variable by your own. or can navigagete inside of the Docker file and then copy and paste thes elements. 
If you choose first method(Dockerfile), you can change value of this environment variable by your own. 

## About Dataset

The fine tuning of the TSOTSALLM is based on  different scenario
like BB(Big Bench), TruthfulQA, BBQ...

for each scenario we used different dataset that public available

### BBQ Scenario 

  the dataset that we are used to this scenario are available on:

  [https://raw.githubusercontent.com/nyu-mll/BBQ/main/data/](https://raw.githubusercontent.com/nyu-mll/BBQ/main/data/)

### TruthfulQA Scenario
  
  for this scenario we used the different dataset
  - [ai2_arc](https://huggingface.co/datasets/ai2_arc) store on huggingFace
  
  - [commonsense_qa](https://huggingface.co/datasets/commonsense_qa) store on huggingFace
  
  - [truthful_qa](https://huggingface.co/datasets/truthful_qa)

### BB Scenario
  
  the dataset that we used for this scenario are store on the huggingFace: lima and dolly databrick

  - [lima](https://huggingface.co/datasets/GAIR/lima)
  - [dolly-databricks](https://huggingface.co/datasets/databricks/databricks-dolly-15k)

### Summarization Scenario

  - [cnn_dailymail](https://huggingface.co/datasets/cnn_dailymail)
  - [xsum](https://huggingface.co/datasets/EdinburghNLP/xsum)


<!-- About Author  -->

## About Author

| Name            | Github Account      |     email     |
| ---------       | ---------           |    -------
| jean petit      |  @jeanpetitt        |  jean.bikim@facsciences-uy1.cm
| Martins         |  @FOLEFAC           |  martinsderick99@gmail.com
| Brice           | Fokobrice3          |  fokobrice3@gmail.com
| Fidel Jiomekong |  @jiofidelus        |  fidel.jiomekong@facsciences-uy1.cm