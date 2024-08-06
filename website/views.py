from flask import Blueprint, render_template, request, flash, jsonify, redirect
from flask_login import login_user, login_required, logout_user,current_user
from .models import *
from . import db
import json
from . import backtraderlogic
import os 

views = Blueprint('views',__name__)
ALLOWED_EXTENSIONS = {'py'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@views.route('/', methods = ["GET","POST"])
@login_required
def home():
    if request.method == "POST":
        filename = request.form.get('filename')

        if 'file' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
        
        file = request.files['file']

        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            file_content = file.read()  # Read and decode the file content as a string

            # Save the algorithm to the database
            new_algorithm = Algorithm(filename=filename, data=file_content, user_id=current_user.id)
            db.session.add(new_algorithm)
            db.session.commit()
            
            start, end, plot_file = backtraderlogic.run_algorithm(file_content) 
            print(start, " ", end)  

            # Store the plot file path in the database or session
            new_algorithm.plot_file = plot_file
            db.session.commit()

    algorithms = Algorithm.query.filter_by(user_id=current_user.id).all()
    return render_template("home.html", user=current_user, algorithms=algorithms, plot_file='static/plot.png')
    
@views.route("/delete-algorithm", methods = ["POST"])
def delete_algorithm():
    algorithm_data = json.loads(request.data)
    algo_id = algorithm_data["algoID"]
    algorithm = Algorithm.query.get(algo_id)
    if algorithm:
        if algorithm.user_id == current_user.id:
            db.session.delete(algorithm)
            db.session.commit()
    return jsonify({})


