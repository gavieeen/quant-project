from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_user, login_required, logout_user,current_user
from .models import *
from . import db
import json

views = Blueprint('views',__name__)

@views.route('/', methods = ["GET","POST"])
@login_required
def home():
    if request.method == "POST":
        filename = request.form.get("filename")
        algorithm = request.form.get("algorithm")

        if len(algorithm) < 1:
            flash("Algorithm is too short", category = "error")
        else:
            newAlgo = Algorithm(data = algorithm, filename = filename, user_id = current_user.id)
            db.session.add(newAlgo)
            db.session.commit()
            flash("Algorithm added!", category = "success")     
           
    return render_template("home.html", user = current_user)
@views.route("/delete-note", methods = ["POST"])
def delete_note():
    note = json.loads(request.data)
    #print(note)
    noteID = note["noteID"]
    algorithm = Algorithm.query.get(noteID)
    if algorithm:
        if note.user_id == current_user.id:
            db.session.delete(algorithm)
            db.session.commit()
    return jsonify({})


