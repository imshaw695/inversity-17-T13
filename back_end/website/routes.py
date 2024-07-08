import os
from flask import jsonify, send_from_directory, render_template, request
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
# Now comes the actual function definition for processing this page
def index():
    # This is a vue project that serves the static index file only
    return render_template("index.html")


@app.route("/send_message", methods=["POST"])
def send_message():
    # global df_chunks
    data = request.json
    conversation_history = data.get('conversation_history', [])
    # truncated_history = truncate_conversation_history(conversation_history)
    # response = ask(truncated_history, df_chunks)
    response = "This is a response from the flask server."
    conversation_history.append({"role": "assistant", "content": response})
    return jsonify({'response': response, 'conversation_history': conversation_history})
    # return dict(rc=0, message="Response from flask.")


@app.errorhandler(404)
# inbuilt function which takes error as parameter
def not_found(e):
    # defining function
    return render_template("index.html"), 404


@app.route("/favicon.png")
@app.route("/favicon.ico")
def show_favicon():
    path_for_favicon = os.path.join(app.root_path, "templates")
    return_package = send_from_directory(
        path_for_favicon, "favicon.ico", mimetype="image/vnd.microsoft.icon"
    )
    return return_package
