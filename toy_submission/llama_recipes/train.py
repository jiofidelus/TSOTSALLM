import os
from dotenv import load_dotenv
from huggingface_hub import login, HfApi
# from llama_recipes.finetuning import main as finetuning

# def main():
#     load_dotenv()
#     login(token=os.environ["HUGGINGFACE_TOKEN"])

#     kwargs = {
#         "model_name": "meta-llama/Llama-2-7b-hf",
#         "use_peft": True,
#         "peft_method": "lora",
#         "quantization": True,
#         "batch_size_training": 2,
#         "dataset": "custom_dataset",
#         "custom_dataset.file": "./custom_dataset.py",
#         "output_dir": "./output_dir ",
#     }

#     finetuning(**kwargs)

#     api = HfApi()

#     api.upload_folder(
#         folder_path='./output_dir/',
#         repo_id=os.environ["HUGGINGFACE_REPO"],
#         repo_type='model',
#     )

# if __name__ == "__main__":
#     main()


# -*- coding: utf-8 -*-
"""Neurips_efficiency_LLM_challenge.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Tm0lUxZ9ilJJL8-tFw2eF7PrAMH5hjGy

# Fine-tuning✨✨ LLaMA using PEFT, QLora and Hugging Face utilities

In this project we'll use 4-bit quantification to fine tune LLama-2 in purpose to produce QA engine
"""

# @title Install dependancies

# @title Import dependancies

import torch as th
from peft import LoraConfig, prepare_model_for_kbit_training, get_peft_model, AutoPeftModelForCausalLM
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, TrainingArguments
from trl import SFTTrainer
import argparse
import time
from dataset import TsotsaDataset


def argsparser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-name", type=str,
                        required=True, help="Name of the base model")
    parser.add_argument("--dataset", type=str,
                        default="GAIR/lima", help="dataset used to train model")
    parser.add_argument("--split", type=str, default="train[:10%]")
    parser.add_argument("--hf_rep", type=str, required=True,
                        help="HuggingFace repository")
    parser.add_argument("--lr", type=float, default=2e-16,
                        help="Learning rate that allow to ajust model weight")
    parser.add_argument("--epochs", type=int, default=3,
                        help="chunk data to train it")
    parser.add_argument("--output_dir", type=str, required=True,
                        help="name of the fine-tuned model")
    parser.add_argument('--bf16', action='store_true',
                        default=True if th.cuda.get_device_capability()[0] == 8 else False)
    parser.add_argument(
        "--per_device_train_batch_size",
        type=int,
        default=1,
        help="Batch size to use for training.",
    )
    parser.add_argument(
        "--seed", type=int, default=42, help="Seed to use for training."
    )
    parser.add_argument(
        "--gradient_checkpointing",
        type=bool,
        default=True,
        help="Path to deepspeed config file.",
    )
    parser.add_argument(
        "--merge_weights",
        type=bool,
        default=True,
        help="Whether to merge LoRA weights with base model.",
    )
    args = parser.parse_args()
    return args


args = argsparser()


def loginHub():
    # @title Login on hugging face
    from huggingface_hub import login, notebook_login
    from dotenv import load_dotenv
    # notebook_login()

    # @title Load environments variables
    # from dotenv import load_dotenv
    import os

    # # Load the enviroment variables
    load_dotenv()
    # Login to the Hugging Face Hub
    login(token="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")
    return login


loginHub()

# BB Scenario QA
lima = TsotsaDataset(split="train[:20%]", type_dataset="bb", name='GAIR/lima')
lima._load_lima()
dolly = TsotsaDataset(
    split="train[:15%]", type_dataset="bb", name='databricks/databricks-dolly-15k')
dolly._load_dolly()
# truthfull QA
ai2_arc = TsotsaDataset(
    split="train[:10%]", type_dataset="TruthfullQA", name="ai2_arc")
# ai2_arc._load_ai2_arc()
common_sense = TsotsaDataset(
    split="train[:10%]", type_dataset="TruthfullQA", name="commonsense_qa")
# common_sense._load_commonsense_qa()
# Summary Scenario QA
cnn_dailymail = TsotsaDataset(
    split="train[:1%]", type_dataset='summary', name="cnn_dailymail")
# cnn_dailymail._load_cnn_dailymail()
xsum = TsotsaDataset(split="train[:1%]", type_dataset='summary', name="xsum")
# xsum._load_xsum()
# BBQ scenario
bbq = TsotsaDataset(split="", type_dataset='bbq',
                    name="category: {Age, Disability_status, Physical_apparence, Religion, Sexual_orientation}, Link: link https://raw.githubusercontent.com/nyu-mll/BBQ/main/data/{category}.jsonl")
# bbq._load_bbq()


def train_model(model_id, datasets):
    i = 0
    hf_model_rep = args.hf_rep
    device_map = {'': 0}
    new_model = args.output_dir
    # run list of all dataset
    for dataset in datasets:
        if dataset.get_type() == "bb":
            formating_function = dataset.prepare_bb_scenario
        elif dataset.get_type() == "TruthfullQA":
            formating_function = dataset.prepare_truthfulqa_scenario
        elif dataset.get_type() == "summary":
            formating_function = dataset.prepare_summerization_scenario
        elif dataset.get_type() == 'bbq':
            formating_function = dataset.prepare_bbq_scenario
        if i == 0:
            model_id = model_id
        else:
            model_id = "merged_model"
            i += 1

        """
        bitsandBytes parameters
        """
        # activation 4-bit precision base model loaded
        use_4bits = True

        # Compute dtype for 4-bit base models
        bnb_4bits_compute_dtype = "float16"
        # quantisation type
        bnb_4bits_quan_type = "nf4"  # we can use nf4 of fp4
        # activation nested quantization for 4-bits base model (double quantization)
        use_double_quant_nested = False

        """
        QloRa parameters
        """
        # LoRa attention dimension
        lora_r = 64
        # alpha parameter for lora scaling
        lora_alpha = 16
        # dropout probality for lora layer
        lora_dropout = 0.1

        """
        TrainingArgument parameters
        """
        # Output directory where the model predictions and checkpoints will be stored
        ouput_dir = new_model
        # number_of_training epochs
        N_EPOCHS = args.epochs
        # Enable fp16/bf16 training
        fp16 = False
        # Batch size per GPU for training
        per_device_train_batch_size = args.per_device_train_batch_size
        # Number of update steps to accumulate the gradients
        gradient_accumulation_steps = 1
        # Enable gradient checkpointing
        gradient_checkpointing = args.gradient_checkpointing
        # Maximum gradient normal (gradient clipping)
        max_grad_norm = 0.3
        # Initial learning rate (AdamW optimizer)
        learning_rate = args.lr  # 1e-5
        # Weight decay to apply to all layers except bias/LayerNorm weights
        weight_decay = 0.001
        # Optimizer to use
        optim = "paged_adamw_32bit"
        # Learning rate schedule
        lr_scheduler_type = "cosine"
        # Number of training steps
        max_steps = -1
        # Ratio of steps for a linear warmup (from 0 to learning rate)
        warmup_ratio = 0.03
        # Group sequences into batches with same length
        group_by_length = False
        # Save checkpoint every X updates steps
        save_steps = 0
        # Log every X updates steps
        logging_steps = 25
        # Disable tqdm
        disable_tqdm = True

        """
        SFTTrainer parameters
        """
        # Maximum sequence length to use
        max_seq_length = 2048
        # Pack multiple short examples in the same input sequence to increase efficiency
        packing = True  # False

        # @title load dataset with instructions
        train_data = dataset.get_dataset()

        """# fine-tune a Llama 2 model using trl and the SFTTrainer

        to fine tuning our model, we need to convert our structured example of tasks by instructions. we define a formating function that take as inputs a sample and return string with our function format
        """

        # @title Using QLoRA technique to reduce memory footprint during the fine-tuning
        # get the type
        compute_dtype = getattr(th, bnb_4bits_compute_dtype)
        print(compute_dtype)

        # BitAndBytesConfg int-4 configuration
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=use_4bits,
            bnb_4bit_use_double_quant=use_double_quant_nested,
            bnb_4bit_quant_type=bnb_4bits_quan_type,
            bnb_4bits_compute_dtype=compute_dtype
        )

        # @title Load the pre-trained model
        model = AutoModelForCausalLM.from_pretrained(
            model_id, quantization_config=bnb_config,
            use_cache=False,
            device_map=device_map,
            low_cpu_mem_usage=True,
            return_dict=True,
            torch_dtype=th.float16)

        print(
            f"Nombre de paramètres du modèle de base : {model.num_parameters()}")

        # @title Load the tokenizer
        tokenizer = AutoTokenizer.from_pretrained(
            model_id, trust_remote_code=True)
        tokenizer.pad_token = tokenizer.eos_token
        tokenizer.padding_side = "right"
        tokenizer.name_or_path

        with open(f'Logs.txt', 'w') as f:
            f.write("TSOTSALLM Log file\n")
            f.write("=============== Model infos========================")
            f.write(f"Model name: {model_id}")
            f.write(f"Model parameters: {model.num_parameters()}")

            f.write(f"=============== Dataset infos========================")
            f.write(f"Dataset: {dataset.get_type()}")
            f.writer(f"Dataset Name: {dataset.get_name()}")
            f.write(f"Len dataset: {len(train_data)}")

        # @title Lora config based on Qlora paper
        """
        The SFTTrainer supports a native integration with peft, which makes it
        super easy to efficiently instruction tune LLMs.
        We only need to create our LoRAConfig and provide it to the trainer.
        """
        peft_config = LoraConfig(
            lora_alpha=lora_alpha,
            lora_dropout=lora_dropout,
            r=lora_r,
            bias="none",
            task_type="CAUSAL_LM"
        )
        # @title Define parameters in TrainingArguments
        args_training = TrainingArguments(
            output_dir=ouput_dir,
            num_train_epochs=N_EPOCHS,
            per_device_train_batch_size=per_device_train_batch_size,
            gradient_accumulation_steps=gradient_accumulation_steps,
            gradient_checkpointing=gradient_checkpointing,
            optim=optim,
            save_steps=save_steps,
            logging_steps=logging_steps,
            save_strategy="epoch",
            learning_rate=learning_rate,
            weight_decay=weight_decay,
            fp16=fp16,
            # bf16=args.bf16,
            max_grad_norm=max_grad_norm,
            warmup_ratio=warmup_ratio,
            max_steps=max_steps,
            group_by_length=group_by_length,
            lr_scheduler_type=lr_scheduler_type,
            # disable_tqdm=disable_tqdm,
            report_to="tensorboard",
            seed=args.seed
        )

        """Before we can start our training, we need to define the hypersparemeters In a TrainingArgument object we want to use"""
        # @title Create a Trainer
        """
        We now have every building block we need to create our SFTTrainer to start then training our model.
        """

        trainer = SFTTrainer(
            model=model,
            train_dataset=train_data,
            peft_config=peft_config,
            max_seq_length=max_seq_length,
            tokenizer=tokenizer,
            packing=packing,
            formatting_func=formating_function,
            args=args_training
        )

        # @title Start Training
        """
        Start training our model by calling the train() method on our Trainer instance.
        """
        start_time = time.time()
        print("Start Training", start_time)
        trainer.train()
        print(trainer)
        end_time = f"{(time.time() - start_time) / 60:.2f}"
        print(f"Total training time {end_time} min")
        with open(f'Logs.txt', 'w') as f:
            f.write("=============== Training infos========================")
            f.write(f"Start time training: {start_time}")
            f.write(f"Metrics :\n {trainer.train()}")
            f.write(
                f"Total training time {end_time} min")
        # save metrics
        # trainer.save_metrics()

        # save_model in local
        trainer.save_model()

        """# Merge the model and adpater and save it

        if running in a T4 instance we have to clean the memory
        """

        # @title empty VRAM
        import gc
        del model
        del trainer
        gc.collect()

        th.cuda.empty_cache()

        gc.collect()

        # @title Reload the trained and saved model and merge it then we can save the whole model
        model_fine = AutoPeftModelForCausalLM.from_pretrained(
            args.output_dir,
            low_cpu_mem_usage=True,
            return_dict=True,
            torch_dtype=th.float16,
            device_map=device_map
        )

        # new_model.push_to_hub("yvelos/Tsotsallm-adapter")
        print(
            f"Nombre de paramètres du modèle fine tune : {model_fine.num_parameters()}")
        # @title Merge LoRa and Base Model

        merged_model = model_fine.merge_and_unload()
        print(
            f"Nombre de paramètres du modèle fusionee: {model_fine.num_parameters()}")
        merged_model.generation_config.temperature = 0.1
        merged_model.generation_config.do_sample = True
        merged_model.generation_config.num_beams = 4
        merged_model.generation_config._name_or_path = 'merged_model'
        # # config json
        merged_model.config.pretraining_tp = 1
        merged_model.config.temperature = 0.1
        merged_model.config.do_sample = True
        merged_model.config._name_or_path = 'merged_model'
        # save the merge model
        merged_model.save_pretrained(f"merged_model")
        tokenizer.save_pretrained("merged_model")

        with open(f'Logs.txt', 'w') as f:
            f.write("=============== Model Fine tuning infos========================")
            f.write(f"Model name: {model_fine}")
            f.write(f"Model parameters: {model_fine.num_parameters()}")
            f.write(f"Model config:\n {model_fine.config}")
            f.write(f"=============== Model merged infos========================")
            f.write(f"Model name: {merged_model}")
            f.write(f"Model parameters: {merged_model.num_parameters()}")
            f.write(f"Model config:\n {merged_model.config}")

            f.write(f"=============== END TO train model========================")
            f.close()

        # @title Push Merged Model to the Hub
        # merged_model.push_to_hub(args.hf_rep)
        # tokenizer.push_to_hub(args.hf_rep)
        del merged_model
        del model_fine

        th.cuda.empty_cache()
        print("===========END TO train model=====================")
    return tokenizer


def main1():
    print("""
        Start training our model By loading the dataset.
    """)
    # datasets = [lima, dolly, ai2_arc, common_sense, xsum, cnn_dailymail,bbq]
    datasets = [lima, dolly]
    tokenizer = train_model(
        datasets=datasets, model_id=args.model_name)
    model = AutoModelForCausalLM.from_pretrained(
        args.output_dir,
        low_cpu_mem_usage=True,
        return_dict=True,
        torch_dtype=th.float16,
        device_map={'': 0}
    )
    print(" Push Model to the Hub")
    model.push_to_hub("yvelos/Tes")
    tokenizer.push_to_hub('yvelos/Tes')
    # model.push_to_hub(args.hf_rep)

    print(
        f"End of training, the model is saved in {args.output_dir} and push to the hub")


if __name__ == "__main__":

    main1()
