import os
from dotenv import load_dotenv
import psycopg2
from openai import OpenAI

this_directory = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(this_directory, "..", ".env"), override=True)

client = OpenAI()
embeddings_model = "text-embedding-ada-002"
model_gpt = "gpt-4o"


def execute_sql(sql, commit=False, records=False, records_package=False):
    with get_db_connection() as connection:
        if not records_package:
            with connection.cursor() as cursor:
                result = cursor.execute(sql)

                if records:
                    tuples = cursor.fetchall()
                    column_names = [desc[0] for desc in cursor.description]
                    column_names = {}

                    for index, column_name in enumerate(cursor.description):
                        column_name = column_name[0]
                        column_names[column_name] = dict(index=index, column_name=column_name)

                    result = dict(tuples=tuples, column_names=column_names)

                if commit:
                    connection.commit()
                pass
        else:
            with connection.cursor() as cursor:
                table = "documents"
                query = f"""
                        INSERT INTO {table} (url, slice_index, token_count, content_plain_text, embedding)
                        VALUES (%s, %s, 100, %s, %s)
                    """
                result = cursor.execute(query, (records_package["metadata"]["url"], records_package["metadata"]["slice_index"], records_package["content"], records_package["embeddings"]))

    cursor.close()
    connection.close()

    return result


def get_db_connection():

    # Database connection parameters
    # openai_api_key = os.environ.get("openai_key")
    DB_HOST = os.environ.get("DB_HOST")
    DB_PORT = os.environ.get("DB_PORT")
    DB_NAME = os.environ.get("DB_NAME")
    DB_USER = os.environ.get("DB_USER")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")

    # Connect to the database
    connection = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

    return connection


def get_embedding(text):
    """Get embedding from OpenAI API."""
    embedding = (
        client.embeddings.create(input=[text], model="text-embedding-ada-002")
        .data[0]
        .embedding
    )
    return embedding


def get_response(content, question):
    system_prompt = """You are a helpful assistant that takes the provided content and answers the users question with it.'
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"content: {content}"},
        {"role": "user", "content": f"User response: {question}"},
    ]
    response = client.chat.completions.create(
        model=model_gpt, temperature=0, messages=messages
    )

    return response.choices[0].message.content
