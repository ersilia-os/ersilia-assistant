from openai import OpenAI
from .defaults import LLAMAFILE_URL, STOP_TOKENS

system_prompt = """
You are a helpful scientific assistant who can detect whether a user's query is relevant to a drug discovery experiment.
Here are a few examples of queries that you can expect:
- "What is the molecular weight of aspirin?"
- "I am working on a drug discovery project for malaria. I am interested in compounds active in the sexual and asexual stages of the parasite. I want some good starting points with new mechanisms of action."
- "I work on malaria drug discovery. We need compounds with a longer half-life so that they do not need to be given daily. They should be available orally. Can you propose analogues of my dataset? They should be active in animal models not only in vitro."
Based on the context, you should determine whether the query is relevant to a drug discovery experiment.
If the query is relevant, you should return True. Otherwise, you should return False.
"""


def query_filter(query: str) -> bool:
    client = OpenAI(
        base_url=f"{LLAMAFILE_URL}/v1",
        api_key="sk-no-key-required",
    )
    completion = client.chat.completions.create(
        model="LLaMA_CPP",
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {"role": "user", "content": query},
        ],
    )
    return "True" in completion.choices[0].message.content
