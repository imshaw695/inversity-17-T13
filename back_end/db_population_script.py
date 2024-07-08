import os
import fitz  # PyMuPDF
import tiktoken
from openai import OpenAI
import psycopg2
from dotenv import load_dotenv
from psycopg2 import sql

# Load environment variables
this_directory = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(this_directory, '.env'), override=True)

# Configuration
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
SOURCE_FOLDER = os.path.join(this_directory, "source_documents")

client = OpenAI()
embeddings_model = "text-embedding-ada-002"
# Database connection
conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

# Create a cursor object
cur = conn.cursor()


def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def get_embedding(text):
    """Get embedding from OpenAI API."""
    embedding = (
        client.embeddings.create(input=[text], model="text-embedding-ada-002")
        .data[0]
        .embedding
    )
    return embedding


def get_token_count_from_string(
    string: str, encoding_name: str = "gpt-3.5-turbo"
) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def save_to_db(source_url, content, embedding, token_count, chunk_index):
    """Save document data to the PostgreSQL database."""
    insert_query = sql.SQL("""
        INSERT INTO source_documents (source_url, content, embedding, token_count, chunk_index)
        VALUES (%s, %s, %s, %s, %s);
    """)
    cur.execute(insert_query, (source_url, content, embedding, token_count, chunk_index))


def chunk_text(text, chunk_size=750, overlap=250):
    """Chunk text into specified chunk size with overlap."""
    tokens = text.split()  # Simple tokenization based on whitespace
    chunks = []
    for i in range(0, len(tokens), chunk_size - overlap):
        chunk = tokens[i:i + chunk_size]
        chunks.append(' '.join(chunk))
        if i + chunk_size >= len(tokens):
            break
    return chunks


def process_documents():
    """Process all PDF documents in the source folder."""
    for filename in os.listdir(SOURCE_FOLDER):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(SOURCE_FOLDER, filename)
            print(f"Processing {pdf_path}")

            # Extract text from PDF
            content = extract_text_from_pdf(pdf_path)

            # Chunk the content with 750 token size and 250 token overlap
            content_chunks = chunk_text(content, chunk_size=750, overlap=250)

            for index, chunk in enumerate(content_chunks):
                # Get embedding from OpenAI
                embedding = get_embedding(chunk)

                # Count tokens in the chunk
                token_count = get_token_count_from_string(chunk)

                # Save to database
                save_to_db(pdf_path, chunk, embedding, token_count, index)


if __name__ == "__main__":
    try:
        process_documents()
        # Commit the transaction
        conn.commit()
        print("Documents processed and saved successfully.")
    except Exception as e:
        print(f"Error processing documents: {e}")
        # Rollback the transaction in case of error
        conn.rollback()
    finally:
        # Close the cursor and connection
        cur.close()
        conn.close()
