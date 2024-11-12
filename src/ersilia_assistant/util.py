from openai import OpenAI
from .defaults import LLAMA_SERVER, QUERY_RELEVANCE_FILTER_PROMPT


def llm_filter(query: str, system_prompt: str = QUERY_RELEVANCE_FILTER_PROMPT) -> bool:
    client = OpenAI(
        base_url=f"{LLAMA_SERVER}/v1",
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
