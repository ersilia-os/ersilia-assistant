import os
import random
import csv
import requests
import openai
from dotenv import load_dotenv
from tqdm import tqdm

ROOT = os.path.abspath(os.path.dirname(__file__))

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY
MODEL_NAME = "gpt-4o"

NUMBER_OF_QUERIES = 190
NUMBER_MODELS_MAX_OPTIONS = 5

OUTPUT_FILE = os.path.join(ROOT, "data", "ai_generated_queries.csv")
if not os.path.exists(OUTPUT_FILE):
    with open(OUTPUT_FILE, "w") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(["model_ids", "query"])

SYSTEM_PROMPT = """
You are a biomedical researcher. You will receive a set of models from the Ersilia Model Hub, specified with a title and a short description.
You need to return a question or request that could match the title and/or description for the model.
For example, if the model relates to antimalarial activity prediction, you could ask or request something like this:
- I want to predict the antiplasmodial activity of a set of compounds.
- I would like to know the antiplasmodial activity of natural product compounds.
- How do I estimate the antimalarial potential of my compounds?
It is possible that more than one model is provided. In this case, you should return a query that makes sense from a drug discovery or biomedicine perspective.
For example, if models relate to antitubercular activity and ADME properties. The main part of the query should be related to the activity against the pathogen, followed by the ADME properties, which are secondary. For example:
- How do I predict the activity against Mtb for compounds that are safe?
- I want the best antimicobacterial compounds of my dataset, and I want to know if my compounds are drug-like.

Notes:
- Include information about the drug development stage, if relevant.
- Strictly do not mention the name of the model, or do not refer to it specifically. This is like an exam, so no hints about the model should be given.

About formatting:
- Return the query question or statement exclusively. Do not add any context.
- Your answer should not be more than 50 words long, ideally around 200 characters.
- Strictly return one paragraph.
- It is possible that the provided models are totally unrelated and impossible to link in one same query in a way that makes sense from a drug discovery or biomedical perspective. In that case, feel free to overlooked the less relevant models.
""".strip()

BEGINNING_OPTIONS = [
    "I would like to...",
    "I am...",
    "How do I...",
    "I have...",
    "I want to...",
    "I am investigating...",
    "I am interested in...",
    "How would you...",
    "How do you...",
    "Is it possible to..."
]


def get_all_model_ids():
    with open(os.path.join(ROOT, "data", "model_ids.csv"), "r") as f:
        reader = csv.reader(f)
        next(reader)
        model_ids = [r[0] for r in reader]
    return model_ids


def sample_models(model_ids, num_models):
    return random.sample(model_ids, num_models)
    

def get_description(model_id):
    url = "https://raw.githubusercontent.com/ersilia-os/{0}/refs/heads/main/README.md".format(model_id)
    try:
        response = requests.get(url)
        text = response.text.split("## Identifiers")[0]
        return text
    except:
        return None


def generate_user_prompt(model_ids):
    user_prompt = "Produce a query that is related to these models:\n\n"
    user_prompt += "You can start your query with the with '{0}' or similar (no need to exactly start like this)".format(random.choice(BEGINNING_OPTIONS))
    descriptions = []
    for model_id in model_ids:
        description = get_description(model_id)
        if description is None:
            continue
        descriptions += [description]
    if len(descriptions) == 0:
        return None
    for description in descriptions:
        user_prompt += description + "\n"
    return user_prompt


def generate_query(user_prompt):
    response = openai.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()


if __name__ == "__main__":

    model_ids = get_all_model_ids()
    number_models_options = [i+1 for i in range(NUMBER_MODELS_MAX_OPTIONS)]

    for _ in tqdm(range(NUMBER_OF_QUERIES)):
        num_models = random.choice(number_models_options)
        model_ids_ = sample_models(model_ids, num_models)
        user_prompt = generate_user_prompt(model_ids_)
        if user_prompt is None:
            continue
        query = generate_query(user_prompt)
        with open(OUTPUT_FILE, "a") as f:
            writer = csv.writer(f, delimiter="\t")
            r = [";".join(model_ids_), query]
            writer.writerow([r[0], r[1]])
