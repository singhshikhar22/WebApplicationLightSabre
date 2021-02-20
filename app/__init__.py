from flask import Flask, flash, request, redirect, url_for, request
from werkzeug.utils import secure_filename
from config import Config

UPLOAD_FOLDER = 'D:/Previous Laptop/vit materials/Projects/WebApplicationLightSabre/Sabre Hackathon-20210218T080059Z-001/Sabre Hackathon'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

from app import routes