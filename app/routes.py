import os
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import cross_origin
from app import app
import re
import time

import sys
# sys.path is a list of absolute path strings
sys.path.append('D:/Previous Laptop/vit materials/Projects/WebApplicationLightSabre/Sabre Hackathon-20210218T080059Z-001/Sabre Hackathon')

import generate_desc
import textSpeech, imageText


UPLOAD_FOLDER = 'D:/Previous Laptop/vit materials/Projects/WebApplicationLightSabre/Sabre Hackathon-20210218T080059Z-001/Sabre Hackathon'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

@app.route('/')
@app.route('/index')
def index():
    
    return render_template('index.html')

@app.route('/about')
def picture():
    return render_template('about.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/picture', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            #filename = "uploaded_img.jpg"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_path = (app.config['UPLOAD_FOLDER'] + '/' +filename)
            description = generate_desc.final_main(filename)
            flash(description)
            #flash(file_path)
            #return render_template('captionDisplay.html', filename=filename)
            return redirect(url_for('textSpeechConversion', description = description, file_name=str(filename)))
            #return render_template('captionDisplay.html', user_image = file_path, caption = description)
    return render_template('uploader.html')
    
    
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)



@app.route('/text', methods=['GET', 'POST'])
def upload_Textfile():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            file.filename = "upload_img.jpg"
            #filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            file_path = (app.config['UPLOAD_FOLDER'] + '/' +file.filename)
            description = imageText.main(file_path)
            new_str = re.sub('[^a-zA-Z0-9\n\.]', '', description)
            description=new_str.split("\n")
            main_from=""
            main_to=""
            main_gate=""
            for text in description:
                if "From" in text:
                    main_from = text
                elif "To" in text:
                    main_to = text
                elif "GATE" in text:
                    main_gate = description[description.index(text) + 1]
                    
            description = "From " + main_from[4:] + " To " + main_to[2:] + " From gate " + main_gate
            flash(description)
            #flash(file_path)
            #return render_template('captionDisplay.html', filename=filename)
            return redirect(url_for('textSpeechConversion', description = description, file_name = str(file.filename)))
            #return render_template('captionDisplay.html', user_image = file_path, caption = description)
    return render_template('uploader.html')



@app.route('/sayit/<description>/<file_name>', methods=['POST', 'GET'])
@cross_origin()
def textSpeechConversion(description, file_name):
    if request.method == 'POST':
        #text = request.form['speech']
        gender = request.form['voices']
        textSpeech.text_to_speech(description, gender)
        return render_template('captionDisplay.html', description = description, file_name=file_name)
    else:
        return render_template('captionDisplay.html')