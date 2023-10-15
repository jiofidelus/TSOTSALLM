from datasets import load_dataset
from random import randrange
import pandas as pd, os, csv, json
import nltk
from bs4 import BeautifulSoup

path = f'{os.getcwd()}/toy_submission/llama_recipes/data'

class TsotsaDataset:
    def __init__(self):
        self.dataset = []
        self.dataset_id = ""
        
    # get size of the dataset
    
    def __len__(self):
        return len(self.dataset)
    """_
        BIG Bench Scenario
    """
    # load lima dataset 
    def _load_lima(self):
        # self.dataset_id = "GAIR/lima"
        # self.dataset = load_dataset(self.dataset_id, split="train")
        # with open(f"{path}/BBQ/lima.csv", "w+") as f:
        #     writer = csv.writer(f)
            
        #     # write header file
        #     writer.writerow(["instruction", "response", "source"])
        #     for data in self.dataset:
        #         writer.writerow([data['conversations'][0], data['conversations'][1], data['source']])
        self.dataset = pd.read_csv(f"{path}/BBQ/lima.csv")
        return self.dataset
    
    # load databricks dataset
    def _load_dolly(self):        
        self.dataset_id = "databricks/databricks-dolly-15k"
        self.dataset = load_dataset(self.dataset_id, split="train[:15%]")     
        with open(f"{path}/BBQ/dolly.csv", "w+") as f:
            writer = csv.writer(f)
            header = ["question", "response", "context", "category"]
            # write header file
            writer.writerow(header)
            for data in self.dataset:
                writer.writerows([data.values()])
        self.dataset = pd.read_csv(f"{path}/BBQ/dolly.csv") 
        return self.dataset
    
    # load oasst1 dataset
    def _load_oasst1(self):
        # self.dataset_id = "OpenAssistant/oasst1"
        # self.dataset = load_dataset(self.dataset_id, split="train")
        
        # with open(f"{path}/BBQ/oasst1.csv", "w+") as f:
        #     writer = csv.writer(f)
            
        #     # write header file
        #     writer.writerow(self.dataset.column_names)
        #     for data in self.dataset:
        #         writer.writerows([data.values()])
        
        self.dataset = pd.read_csv(f"{path}/BBQ/oasst1.csv")
        
        return self.dataset
    
    # summerization dataset
    def _load_redpajama(self):
        self.dataset_id = "togethercomputer/RedPajama-Data-1T"
        self.dataset = load_dataset(self.dataset_id, split="train[:20%]", name="arxiv")
        return self.dataset
    
    """_
        truthfullqa Scenario
    """
    # truthfullqa dataset    
    def _load_ai2_arc(self):
        self.dataset_id = "ai2_arc"
        self.dataset = load_dataset(self.dataset_id, split="train", name="ARC-Easy")
        
        # with open(f"{path}/TruthfulQA/ai2_arc.csv", "w+") as f:
        #     writer = csv.writer(f)
            
        #     # write header file
        #     writer.writerow(self.dataset.column_names)
        #     for data in self.dataset:
        #         writer.writerows([data.values()])
        
        # self.dataset = pd.read_csv(f"{path}/TruthfulQA/ai2_arc.csv")
        
        
        return self.dataset
    
    # truthfullqa dataset
    def _load_commonsense_qa(self):
        self.dataset_id = "commonsense_qa"
        self.dataset = load_dataset(self.dataset_id, split="train")
        
        # with open(f"{path}/TruthfulQA/commense_qa.csv", "w+") as f:
        #     writer = csv.writer(f)
            
        #     # write header file
        #     writer.writerow(self.dataset.column_names)
        #     for data in self.dataset:
        #         writer.writerows([data.values()])
        
        # self.dataset = pd.read_csv(f"{path}/TruthfulQA/commense_qa.csv")
        
        return self.dataset
    
    """ 
        formating function for each type of scenarios
    """
    
    def prepare_bbq_scenario(self, sample):
        string = f"""
            ### Welcome in your assistant!!!!!!!
            
            ### INSTRUCTIONS:
            
            {sample[0]}


            ### Answer
            {sample[1]}

        """
        print(string)
        return string
    
    def prepare_truthfulqa_scenario(self, sample):
        sample_dict = eval(sample['choices'])
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
        print(string)
        return string
    
    
    def prepare_summerization_scenario(self, sample):
        string = f"""
            ### Welcome in your assistant!!!!!!!
            
            ### INSTRUCTIONS:
            
            {sample[0]}


            ### Answer
            {sample[1]}

        """
        print(string)
        return string
    
    

# tsotsa = TsotsaDataset()

# print(tsotsa._load_lima())

# BBQ dataset
# dataset_lima = tsotsa._load_lima()
# dataset_dolly = tsotsa._load_dolly()
# tsotsa.prepare_bbq_scenario(dataset_lima.iloc[randrange(len(dataset_lima))])
# tsotsa.prepare_bbq_scenario(dataset_dolly.iloc[randrange(len(dataset_dolly))])

# TruthfulQA dataset
# ai2_arc_dataset = tsotsa._load_ai2_arc()
# com_qa_dataset = tsotsa._load_commonsense_qa()
# tsotsa.prepare_truthfulqa_scenario(ai2_arc_dataset.iloc[randrange(len(ai2_arc_dataset))])


# print(tsotsa._load_databricks())
# print(tsotsa._load_oasst1())
# print(tsotsa._load_redpajama())

