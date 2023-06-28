from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')  # Obtiene la nota del formulario HTML

        if len(note) < 1:
            flash('¡La nota es demasiado corta!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)  # Crea un nuevo objeto Note
            db.session.add(new_note)  # Agrega la nota a la base de datos
            db.session.commit()
            flash('¡Nota agregada!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)  # Esta función espera un JSON del archivo INDEX.js
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


@views.route('/edit-note', methods=['POST'])
def edit_note():
    note = json.loads(request.data)  
    noteId = note['noteId']
    newNote = note['newNote']

    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            note.data = newNote
            db.session.commit()

    return jsonify({})
