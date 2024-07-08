import os
from flask import jsonify, send_from_directory, render_template, request
from website.utilities import execute_sql, get_embedding, get_response
from flask import current_app as app
# from website.llm_handler import ask, truncate_conversation_history
# from website.google_utils import get_bigquery_client, fetch_embeddings_from_bigquery
# import logging

# bq_client = get_bigquery_client()

# BigQuery dataset and table information
BQ_DATASET = os.getenv('BQ_DATASET')
BQ_TABLE = os.getenv('BQ_TABLE')

# Fetch embeddings from BigQuery
# try:
#     df_chunks = fetch_embeddings_from_bigquery(bq_client, BQ_DATASET, BQ_TABLE)
#     logging.info("Successfully fetched embeddings from BigQuery.")
# except Exception as e:
#     logging.error(f"Error fetching embeddings from BigQuery: {e}")
#     df_chunks = None


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
    """
    Serve the static index file for the Vue project.

    Returns:
        str: The rendered HTML for the index page.
    """
    try:
        return render_template("index.html")
    except Exception as e:
        app.logger.error(f"Error rendering index page: {e}")
        return "Error rendering index page", 500


@app.route("/send_message", methods=["POST"])
def send_message():
    """
    Handle sending a message to the server and getting a response.

    Returns:
        json: A JSON response containing the assistant's reply and the updated conversation history.
    """
    try:
        # global df_chunks
        data = request.json
        conversation_history = data.get('conversation_history', [])
        embeddings = get_embedding(data["message"])
        matches = get_close_matches(embeddings)
        matched_contents = [match[3] for match in matches]
        # truncated_history = truncate_conversation_history(conversation_history)
        # response = ask(truncated_history, df_chunks)
        response = get_response(matched_contents, data["message"])
        conversation_history.append({"role": "assistant", "content": response})
        # time.sleep(2)
        return jsonify({'response': response, 'conversation_history': conversation_history})
    except Exception as e:
        app.logger.error(f"Error in /send_message: {e}")
        return jsonify({'error': 'An error occurred while processing the request'}), 500


@app.errorhandler(404)
def not_found(e):
    """
    Handle 404 errors by rendering the index page.

    Args:
        e (Exception): The exception that was raised.

    Returns:
        tuple: The rendered HTML for the index page and the 404 status code.
    """
    app.logger.warning(f"404 error: {e}")
    return render_template("index.html"), 404


@app.route("/favicon.png")
@app.route("/favicon.ico")
def show_favicon():
    """
    Serve the favicon for the website.

    Returns:
        Response: The response object containing the favicon.
    """
    try:
        path_for_favicon = os.path.join(app.root_path, "templates")
        return send_from_directory(
            path_for_favicon, "favicon.ico", mimetype="image/vnd.microsoft.icon"
        )
    except Exception as e:
        app.logger.error(f"Error serving favicon: {e}")
        return "Error serving favicon", 500


def get_close_matches(embeddings, n=5):
    sql = f"""
        SELECT embedding <-> ('{embeddings}') as distance, *
        FROM source_documents
        ORDER BY distance LIMIT {n}
    """
    results = execute_sql(sql, records=True)
    return results['tuples']
