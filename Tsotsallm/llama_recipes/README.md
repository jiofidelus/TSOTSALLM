# Getting started
To obtain access to the model weights you need to fill out this [form](https://ai.meta.com/resources/models-and-libraries/llama-downloads/) to accept the license terms and acceptable use policy.

After access has been granted, you need to acknowledge this in your HuggingFace account for the model you want to fine-tune. In this example we will continue with the 7B parameter version available under this identifier: meta-llama/Llama-2-7b-hf

**NOTE** In this example the training result will be uploaded and downloaded through huggingface_hub. The authentication will be done through a token created in the settings of your HuggingFace account.
Make sure to give write access to the token and set the env variables in the Dockerfiles to your token and repo:

```bash
ENV HUGGINGFACE_TOKEN="YOUR_TOKEN"
ENV HUGGINGFACE_REPO="YOUR_USERNAME/YOUR_REPO"
```

# Fine-tune the model
With llama-recipes its possible to fine-tune Llama on custom data with a single command. To fine-tune on a custom dataset we need to implement a function (get_custom_dataset) that provides the custom dataset following this example [custom_dataset.py](https://github.com/facebookresearch/llama-recipes/blob/main/examples/custom_dataset.py).
We can then train on this dataset using this command line:

```bash
python train.py --model-name meta-llama/Llama-2-7b-hf --hf_rep yvelos/Tsotsallm-evaluation --output_dir /temp/model/Tsotsallm
```


```bash
docker build -f ./Dockerfile.train -t tsotsallm_train .

docker run --gpus "device=0" --rm -ti tsotsallm_train
```

The inference Docker is created and started with:

```bash
docker build -f ./Dockerfile.inference -t tsotsallm_inf .

docker run --gpus "device=0" -p 8080:80 --rm -ti tsotsallm_inf
```

To test the inference docker we can run this query:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"text": "What is the capital of Cameroon? "}' http://localhost:8080/tokenize
OR
curl -X POST -H "Content-Type: application/json" -d '{"text": "What is the capital of Cameroon? "}' http://localhost:8080/process
```
