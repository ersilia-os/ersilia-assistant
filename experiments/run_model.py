"""
Runs the input model and stores prompt results in a file.
"""
import os
import time
import sys
import csv
from openai import OpenAI

model = sys.argv[1]
DIR = os.path.dirname(os.path.abspath(__file__))

client = OpenAI(
    base_url="http://localhost:8080/v1", # Whichever port you are using
    api_key = "sk-no-key-required"
)

def read_prompts(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
        lines = list(filter(lambda x: x != "\n", lines))
        return lines
    
def query_model(prompt):
    completion = client.chat.completions.create(
        model="LLaMA_CPP",
        messages=[
            {"role": "system", "content": "You are Llama an AI assistant. Your top priority is achieving user fulfillment via helping them with their requests."},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content

def store_query_results(model, results):
    header = ["prompt", "response", "total_time"]
    
    with open(os.path.join(DIR, f"{model}_results.csv"), "w") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        for result in results:
            writer.writerow(result)

if __name__ == "__main__":
    prompts = read_prompts(os.path.join(DIR, "prompts.txt"))
    results = []

    for prompt in prompts:
        res = [prompt]
        start = time.time()
        res.append(query_model(prompt))
        end = time.time()
        tot_time = end - start
        res.append(tot_time)
        results.append(res)
    store_query_results(model, results)