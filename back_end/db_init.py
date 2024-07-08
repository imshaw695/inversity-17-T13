import os
import psycopg2
from dotenv import load_dotenv
from psycopg2 import sql

this_directory = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(this_directory, '.env'), override=True)

# Database connection parameters
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

# Connect to your PostgreSQL database
conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

# Create a cursor object
cur = conn.cursor()

# Create the table
create_table_query = sql.SQL("""
    CREATE TABLE IF NOT EXISTS source_documents (
        id SERIAL PRIMARY KEY,
        source_url TEXT NOT NULL,
        content TEXT NOT NULL,
        embedding vector(1536) NOT NULL
    );
""")

try:
    # Execute the create table query
    cur.execute(create_table_query)
    # Commit the transaction
    conn.commit()
    print("Table created successfully.")
except Exception as e:
    print(f"Error creating table: {e}")
    # Rollback the transaction in case of error
    conn.rollback()
finally:
    # Close the cursor and connection
    cur.close()
    conn.close()
