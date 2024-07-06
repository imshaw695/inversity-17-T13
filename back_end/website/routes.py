import os
from flask import Flask, jsonify, send_from_directory, render_template, make_response, request
from flask import current_app as app


@app.route('/',methods=["GET", "POST"])
def upload_file():
    if request.method == 'POST':
        # Check if the POST request has the file part
        if 'cameraInput' not in request.files and "videoInput" not in request.files:
            return render_template('index.html', error='No file part')

        if 'cameraInput' in request.files:
            file = request.files['cameraInput']
        if 'videoInput':
            file = request.files['videoInput']

        # If the user does not select a file, the browser submits an empty file without a filename
        if file.filename == '':
            return render_template('index.html', error='No selected file')

        # Save the file to a folder (output_no_git in this case)
        output_folder = 'output_no_git'
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        file_path = os.path.join(output_folder, file.filename)
        file.save(file_path)

        return render_template('index.html', success='File uploaded successfully')

    return render_template('index.html')