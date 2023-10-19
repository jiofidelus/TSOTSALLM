from datasets import load_dataset, Dataset, Features, Value, ClassLabel
from random import randrange
import pandas as pd
import os
import requests
import jsonlines

path = f'{os.getcwd()}/data'
# path = f'{os.getcwd()}/toy_submission/llama_recipes/data'


def download_file(path_destination):
    categories = [
        "Age",
        "Disability_status",
        "Gender_identity",
        "Nationality",
        "Physical_appearance",
        "Race_ethnicity",
        "Race_x_SES",  # extra intersectional category as mentioned in section 3.2
        "Race_x_gender",  # extra intersectional category as mentioned in section 3.2
        "Religion",
        "SES",
        "Sexual_orientation",
    ]

    for category in categories:
        response = requests.get(
            f'https://raw.githubusercontent.com/nyu-mll/BBQ/main/data/{category}.jsonl')
        print(response.raise_for_status())

        with open(f'{path_destination}/data.jsonl', "wb") as file:
            file.write(response.content)


class TsotsaDataset:
    def __init__(self, split, type_dataset="bb"):
        self.dataset = []
        self.dataset_id = ""
        self.split = split
        self.type_dataset = type_dataset

    # get size of the dataset

    def __len__(self):
        return len(self.dataset)

    """
        getter methods
    """

    def get_type(self):
        return self.type_dataset

    def get_dataset(self):
        return self.dataset

    """_
        BIG Bench Scenario
    """
    # load lima dataset

    def _load_lima(self):
        self.dataset_id = "GAIR/lima"
        self.dataset = load_dataset(self.dataset_id, split=self.split)
        return self.dataset

    # load databricks dataset
    def _load_dolly(self):
        self.dataset_id = "databricks/databricks-dolly-15k"
        self.dataset = load_dataset(self.dataset_id, split=self.split)
        return self.dataset

    # load oasst1 dataset

    def _load_oasst1(self):
        self.dataset_id = "OpenAssistant/oasst1"
        self.dataset = load_dataset(self.dataset_id, split=self.split)

        return self.dataset

    # summerization dataset
    def _load_redpajama(self):
        self.dataset_id = "togethercomputer/RedPajama-Data-1T"
        self.dataset = load_dataset(
            self.dataset_id, split=self.split, name="arxiv")
        return self.dataset

    """_
        truthfullqa Scenario
    """
    # truthfullqa dataset

    def _load_ai2_arc(self):
        self.dataset_id = "ai2_arc"
        self.dataset = load_dataset(
            self.dataset_id, split=self.split, name="ARC-Easy")

        return self.dataset

    # truthfullqa dataset
    def _load_commonsense_qa(self):
        self.dataset_id = "commonsense_qa"
        self.dataset = load_dataset(self.dataset_id, split=self.split)
        return self.dataset

    """ 
        Summarization 
    """

    def _load_xsum(self):
        self.dataset_id = "xsum"
        self.dataset = load_dataset(self.dataset_id, split=self.split)
        return self.dataset

    def _load_cnn_dailymail(self):
        self.dataset_id = "cnn_dailymail"
        self.dataset = load_dataset(
            self.dataset_id, split=self.split, name='3.0.0')
        return self.dataset

    """ 
        BBQ Datasete
    """

    def _load_bbq(self):
        # download_file(path)
        for file in os.listdir(path):
            print(file)
            if file.endswith(".jsonl"):
                with jsonlines.open(f'{path}/{file}') as reader:
                    for data in reader:
                        self.dataset.append(data)

        self.dataset = self.dataset[:5000]
        # print(self.dataset.columns)
        print("Size of dataset", len(self.dataset))
        return self.dataset

    """ 
        formating function for each type of scenarios
    """

    def prepare_bb_scenario(self, sample):

        if 'conversations' in sample:
            instruction = sample['conversations'][0]
            response = sample['conversations'][1]
            del sample['conversations']
            sample['instruction'] = instruction
            sample['response'] = response

        string = f"""
        ### Welcome in your assistant!!!!!!!
                
        ### INSTRUCTIONS:
        \n{sample['instruction']}
                
        ### Answer
        \n{sample['response']}
        """
        return string

    def prepare_truthfulqa_scenario(self, sample):
        sample_dict = sample['choices']
        text_list = sample_dict['text']
        label_list = sample_dict['label']
        formatted_list = []
        for i in range(len(text_list)):
            formatted_list.append(f"{label_list[i]}. {text_list[i]} \n\t")
        string = f"""
        ### Welcome in your assistant!!!!!!!
            
        ### INSTRUCTIONS:
        {sample['question']}
            
        ### Choices
        {"".join(formatted_list)}

        ### Answer
        {sample['answerKey']}

        """
        return string

    def prepare_summerization_scenario(self, sample):
        if 'highlights' and 'article' in sample:
            summary = sample['highlights']
            document = sample['article']
            del sample['highlights']
            del sample['article']
            sample['summary'] = summary
            sample['document'] = document
        string = f"""
            ### Welcome in your assistant!!!!!!!
            
            ### INSTRUCTIONS:
            
            {sample['document']}


            ### Answer
            {sample['summary']}

        """
        # print(string)
        return string

    def prepare_bbq_scenario(self, sample):

        ans0 = sample['ans0']
        ans1 = sample['ans1']
        ans2 = sample['ans2']
        label = sample['label']
        question = sample['question']
        context = sample['context']
        context_condition = ''
        question_polarity = ''
        if sample['question_polarity'] == 'nonneg':
            question_polarity = 'Postitve'
        else:
            question_polarity = 'Negative'

        if sample['context_condition'] == 'ambig':
            context_condition = 'Ambigous'
        else:
            context_condition = 'Non-Ambigous'
        category = sample['category']

        choices = []
        reference = {
            'label': ['A', 'B', 'C'],
            'text': [ans0, ans1, ans2]
        }

        correct_answer = reference['label'][label]
        for i in range(len(reference['label'])):
            choices.append(
                f'{reference["label"][i]}. {reference["text"][i]} \n\t')
        string = f"""
        ### Welcome in your assistant!!!!!!!
            
        ### Context
        {context}
        {question_polarity}
        {context_condition}   
            
        ### INSTRUCTIONS:  
        {question}
            
        ### Choices
        {''.join(choices)}
            
        #### Category
        {category}

        ### Answer
        {correct_answer}

        """
        # print(string)
        return string


# download_file(path)

# tsotsa = TsotsaDataset('train')
# tsotsa._load_lima()
# print(tsotsa.dataset)

# bbq_dataset = tsotsa._load_bbq()
# tsotsa.prepare_bbq_scenario(bbq_dataset[randrange(len(bbq_dataset))])

# print(tsotsa._load_lima())

# BB dataset
# dataset_lima = tsotsa._load_lima()
# dataset_dolly = tsotsa._load_dolly()
# tsotsa.prepare_bb_scenario(dataset_lima[randrange(len(dataset_lima))])
# tsotsa.prepare_bb_scenario(dataset_dolly[randrange(len(dataset_dolly))])

# Summarization
# xum_dataset = tsotsa._load_xsum()
# print(xum_dataset)
# cnn_dailymail_dataset = tsotsa._load_cnn_dailymail()
# print(cnn_dailymail_dataset)

# TruthfulQA dataset
# ai2_arc_dataset = tsotsa._load_ai2_arc()
# com_qa_dataset = tsotsa._load_commonsense_qa()
# tsotsa.prepare_truthfulqa_scenario(ai2_arc_dataset.iloc[randrange(len(ai2_arc_dataset))])


# print(tsotsa._load_databricks())
# print(tsotsa._load_oasst1())
# print(tsotsa._load_redpajama())
