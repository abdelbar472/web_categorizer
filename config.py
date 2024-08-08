from flask import Flask, session, render_template,redirect,request,url_for,jsonify,make_response
from datetime import timedelta
from flask_restful import Resource, reqparse, Api
from flask_sqlalchemy import SQLAlchemy
import random
from urllib.parse import urlparse
import requests
from PIL import Image, ImageTk
from io import BytesIO

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.secret_key = '1c947b92aa43e0863c14c4ff25f07b490a1c1225a913bedc36fb3d0be862376d'  # Replace with your own secret key
app.permanent_session_lifetime = timedelta(hours=5)
db = SQLAlchemy(app)
api = Api(app)
