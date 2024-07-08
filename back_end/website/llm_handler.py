import os
import pandas as pd
from scipy import spatial
import openai
import tiktoken
import logging

EMBEDDING_MODEL = "text-embedding-3-small"
GPT_MODEL = 'gpt-3.5-turbo'

# Setup logging
logging.basicConfig(level=logging.INFO)

# Fetch the API key from Secret Manager
try:
    openai_api_key = os.getenv('OPEN_API_KEY')  # Ensure this matches your secret name
    client_openai = openai.OpenAI(api_key=openai_api_key)
    logging.info("Successfully fetched OpenAI API key.")
except Exception as e:
    logging.error(f"Error fetching OpenAI API key: {e}")
    openai_api_key = None


def strings_ranked_by_relatedness(
    query: str,
    df: pd.DataFrame,
    text_col_name: str = "Chunk",
    embedding_col_name: str = "Embeddings",
    relatedness_fn=lambda x, y: 1 - spatial.distance.cosine(x, y),
    top_n: int = 20,
    client=client_openai
) -> tuple[list[str], list[float]]:
    """Returns a list of strings and relatednesses, sorted from most related to least."""
    query_embedding_response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=query,
    )
    query_embedding_response = client_openai.embeddings.create(
        model=EMBEDDING_MODEL,
        input=query,
    )
    query_embedding = query_embedding_response.data[0].embedding
    strings_and_relatednesses = [
        (row[text_col_name], relatedness_fn(query_embedding, row[embedding_col_name]))
        for i, row in df.iterrows()
    ]
    strings_and_relatednesses.sort(key=lambda x: x[1], reverse=True)
    strings, relatednesses = zip(*strings_and_relatednesses)
    return strings[:top_n], relatednesses[:top_n]


def num_tokens(text: str, model: str = GPT_MODEL) -> int:
    """Return the number of tokens in a string."""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))


MAX_HISTORY_LENGTH = 10  # Limit the conversation history to the last 10 interactions


def truncate_conversation_history(conversation_history):
    if len(conversation_history) > MAX_HISTORY_LENGTH:
        return conversation_history[-MAX_HISTORY_LENGTH:]
    return conversation_history


def query_message(
    conversation_history: list,
    df: pd.DataFrame,
    model: str,
    token_budget: int
) -> str:
    """Return a message for GPT, with relevant source texts pulled from a dataframe."""
    query = conversation_history[-1]['content']
    full_message = "\n".join([f"{m['role']}: {m['content']}" for m in conversation_history])
    strings, relatednesses = strings_ranked_by_relatedness(full_message, df)
    introduction = """Use the below texts on The Crown Estate's FY23 (2022/23) annual reports and accounts to answer the subsequent question. If the answer cannot be found in the
    texts, write "I could not find an answer." """
    question = f"\n\nQuestion: {query}"
    message = introduction
    for string in strings:
        next_article = f'\n\nTCE FY23 Annual Report section:\n"""\n{string}\n"""'
        if (
            num_tokens(message + next_article + question, model=model)
            > token_budget
        ):
            break
        else:
            message += next_article
    full_message = "\n".join([f"{m['role']}: {m['content']}" for m in conversation_history]) + message
    return full_message + question


def ask(
    conversation_history: list,
    df: pd.DataFrame,
    model: str = GPT_MODEL,
    token_budget: int = 16300 - 500,
    print_message: bool = False,
) -> str:
    """Answers a query using GPT and a dataframe of relevant texts and embeddings."""
    message = query_message(conversation_history, df, model=model, token_budget=token_budget)
    if print_message:
        print(message)
    messages = [
        {"role": "system", "content": "You answer questions about the Offshore Wind based on TCE Annual report and Offshore Wind Market Report by US Department of Energy"},
        {"role": "user", "content": message},
    ]
    response = client_openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0
    )
    response_message = response.choices[0].message.content
    return response_message
