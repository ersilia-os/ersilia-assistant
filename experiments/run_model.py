"""
Runs the input model and stores prompt results in a file.
"""
from openai import OpenAI


client = OpenAI(
    base_url="http://localhost:8080/v1", #
    api_key = "sk-no-key-required"
)
# completion = client.chat.completions.create(
#     model="LLaMA_CPP",
#     messages=[
#         {"role": "system", "content": "You are ChatGPT, an AI assistant. Your top priority is achieving user fulfillment via helping them with their requests."},
#         {"role": "user", "content": "Write a limerick about python exceptions"}
#     ]
# )
# print(completion.choices[0].message)

def read_prompts(file_path):
    with open(file_path, "r") as file:
        return file.readlines()
    
def query_model(model, prompt):
    completion = client.chat.completions.create(
        # model="LLaMA_CPP",
    )
    # TODO: Implement the model query

def store_query_results(results):
    # Store the results in a file
    pass

if __name__ == "__main__":
    prompts = read_prompts("prompts.txt")
    for prompt in prompts:
        query_model("LLaMA_CPP", prompt)
        # Store the results in a file