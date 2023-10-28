**Only this README was modified on Saturday 28.10.2023 with links to appropriate resources (docker) in the GitHub repository.**

# TSOTSALLM: Large Language Models at Small Scales

TSOTSALLM is a LLM obtained after fine tuned llama2 with 7B parameters. The public repository of this LLM is: [meta-llama/Llama-2-7b-hf](https://huggingface.co/meta-llama/Llama-2-7b-hf)

[Click to have more information on TSOTSALLM](./TSOTSALLM.md)

<!-- Setup the development environment -->
## Development Environment

### Operating System

This project can run on the following operating systems:

* Linux distribution. The version we used for testing is Ubuntu 20.04
* Mac Os
* Windows

### Code Editor

* Visual Studio Code
* Google Colab

### Dependencies
To reproduce this project locally, Python 3 should be installed. If it is not the case, follow the following link for installation instructions: [Download python](https://www.python.org/downloads/)

Once Python 3 is installed, the following points give the steps to install all dependencies:

* Firstly, clone the project:
 
```bash
git clone https://github.com/jiofidelus//TSOTSALLM.git
cd TSOTSALLM/Tsotsallm/llama_recipes
```

* Secondly, create virtual environment

```bash
pip install virtualenv
python -m venv venv
```

* Activate your environment
 
```bash
source venv/bin/activate
```

* Install the project dependencies
 
```bash
pip install -r requirements.txt
pip install -r fast_api_requirements.txt
```

## Run the project

To Run the project make sure your A100 GPU (40GB) is available.

When everything is OK, you can run the project via docker or by executing the train file.

* Using Docker <br/>
The project has two Docker file: [docker train](/Tsotsallm/llama_recipes/Dockerfile.train) and [docker inference](/Tsotsallm/llama_recipes/Dockerfile.inference)

To train, navigate in the [docker train file](/Tsotsallm/llama_recipes/Dockerfile.train) and replace the token and repository by your own repository and token.

To make the inference navigate in [docker inference file](/Tsotsallm/llama_recipes/Dockerfile.inference) and replace the token and repository by your own repository and token.

The [Docker Readme](/Tsotsallm/llama_recipes/README.md) contains the instructions to launch the [docker train file](/Tsotsallm/llama_recipes/Dockerfile.train) and [docker inference file](/Tsotsallm/llama_recipes/Dockerfile.inference).

* Second method: clone the repository and train the model locally. To this end, replace the arguments values by your own values. Create and <strong>.env file </strong> in your project and paste the following text:

```bash
HUGGINGFACE_TOKEN="YOUR_TOKEN"
HUGGINGFACE_REPO="YOUR_USERNAME/YOUR_REPO"
```
Replace the value of these environments variable by your own. 

Execute the following commands to train the model:
 
```bash
python train.py --model-name meta-llama/Llama-2-7b-hf --hf_rep yvelos/Tsotsallm-beta --output_dir /temp/model/Tsotsallm
```
## About Dataset

The fine tuning of the TSOTSALLM is based on  different scenario
like BB(Big Bench), TruthfulQA, BBQ...

For each scenario we used different dataset that are publicly available.

### BBQ Scenario

The dataset that we are used to this scenario are available on:

[https://github.com/nyu-mll/BBQ/tree/main/data](https://github.com/nyu-mll/BBQ/tree/main/data)

### TruthfulQA Scenario
 
For this scenario we used the different dataset
  - [ai2_arc](https://huggingface.co/datasets/ai2_arc) store on huggingFace
 
  - [commonsense_qa](https://huggingface.co/datasets/commonsense_qa) store on huggingFace
 
  - [truthful_qa](https://huggingface.co/datasets/truthful_qa)

### BB Scenario
 
The dataset that we used for this scenario are store on the huggingFace: lima and dolly databrick

  - [lima](https://huggingface.co/datasets/GAIR/lima)
  - [dolly-databricks](https://huggingface.co/datasets/databricks/databricks-dolly-15k)

### Summarization Scenario

  - [cnn_dailymail](https://huggingface.co/datasets/cnn_dailymail)
  - [xsum](https://huggingface.co/datasets/EdinburghNLP/xsum)


<!-- About Author  -->

## About Author

| Name        	| Github Account  	| 	email 	|
| ---------   	| ---------       	|	-------
| jean petit  	|  @jeanpetitt    	|  jean.bikim@facsciences-uy1.cm
| Martins     	|  @FOLEFAC       	|  martinsderick99@gmail.com
| Brice       	| Fokobrice3      	|  fokobrice3@gmail.com
| Fidel Jiomekong |  @jiofidelus    	|  fidel.jiomekong@facsciences-uy1.cm
