from flask import Blueprint, render_template
from flask_login import login_required, current_user


views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template('home.html', title='Notes App', user=current_user)

@views.route('/add-notes')
@login_required
def add_notes():
    return render_template('add_notes.html', title='Add Notes', user=current_user)

