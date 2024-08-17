from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from . import db
from .models import Note
import json

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    today = datetime.now()
    return render_template('home.html', title='Notes App', user=current_user, date=today)

@views.route('/add-notes', methods=['GET', 'POST'])
@login_required
def add_notes():
    today = datetime.now()
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        if not title or not content:
            flash("Please fill both title and content for the note.", category='danger')
        else:
            new_note = Note(title=title, content=content, user_id=current_user.id, date=today )
            db.session.add(new_note)
            db.session.commit()  
            flash("New note has been added.", category='success')
            return redirect(url_for('views.view_notes'))

    return render_template('add_notes.html', title='Add Notes', user=current_user, date=today)

@views.route('/view-notes', methods=['GET', 'POST'])
@login_required
def view_notes():
    if request.method == 'GET':
        notes = Note.query.filter_by(user_id=current_user.id).all()  
        today = datetime.now()
        return render_template('view_notes.html', title='View Notes', user=current_user, notes=notes, date=today)

@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note: 
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            return jsonify({})
    return jsonify({})
    
@views.route('/search-note', methods=['GET'])
@login_required
def search_note():
    search_term = request.args.get('search_term', '')  # Use request.args for GET parameters
    notes = Note.query.filter(Note.title.contains(search_term), Note.user_id == current_user.id).all()
    today = datetime.now()
    return render_template('view_notes.html', title='Search Note', user=current_user, notes=notes, search_term=search_term, date=today)
