import os
import fitz  # PyMuPDF
from openai import OpenAI
import psycopg2
from psycopg2 import sql

# Configuration
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
SOURCE_FOLDER = "./source_documents"

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
    response = (
        client.embeddings.create(input=[text], model="text-embedding-ada-002")
        .data[0]
        .embedding
    )
    embedding = response['data'][0]['embedding']
    return embedding


def save_to_db(source_url, content, embedding):
    """Save document data to the PostgreSQL database."""
    insert_query = sql.SQL("""
        INSERT INTO source_documents (source_url, content, embedding)
        VALUES (%s, %s, %s);
    """)
    cur.execute(insert_query, (source_url, content, embedding))


def process_documents():
    """Process all PDF documents in the source folder."""
    for filename in os.listdir(SOURCE_FOLDER):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(SOURCE_FOLDER, filename)
            print(f"Processing {pdf_path}")

            # Extract text from PDF
            content = extract_text_from_pdf(pdf_path)

            # Get embedding from OpenAI
            embedding = get_embedding(content)

            # Save to database
            save_to_db(pdf_path, content, embedding)


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
