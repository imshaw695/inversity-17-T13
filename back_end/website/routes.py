import os
from flask import Flask, jsonify, send_from_directory, render_template, make_response, request
from flask import current_app as app

@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
# Now comes the actual function definition for processing this page
def index():
    # This is a vue project that serves the static index file only
    path_for_temlate = os.path.join(app.root_path, "templates")
    return render_template("index.html")


@app.route("/test", methods=["POST"])
def test():
    return dict(rc=0, message="Response from flask.")


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
