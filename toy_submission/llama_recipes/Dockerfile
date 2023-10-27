FROM ghcr.io/pytorch/pytorch-nightly:b3874ab-cu11.8.0

RUN apt-get update  && apt-get install -y git python3-virtualenv wget

WORKDIR /workspace

RUN wget https://gist.githubusercontent.com/mreso/ec65015cbfbd395f0c2adc17147adf1f/raw/41070f1058820b9e89bae885968cc666a7d6aa59/custom_dataset.py

ENV HUGGINGFACE_TOKEN="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"
ENV HUGGINGFACE_REPO="jeanpetitt/Tsotsall-evaluation"

COPY train.py ./

CMD [ "python", "train.py", "--hf_rep", "Your repository"]
