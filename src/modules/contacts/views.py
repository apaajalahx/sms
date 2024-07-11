from . import contacts
from src.models import Contacts
from src import db
from flask import render_template, request, redirect, url_for, flash
import pandas as pd
from io import BytesIO


@contacts.get("")
def index():
    page = request.args.get('page', 1, type=int)
    contact = Contacts.groupBy(page)
    return render_template('dashboard/contacts/index.html', items=contact.items, pagination=contact)

@contacts.get("/folder/<string:name>")
def folder(name):
    page = request.args.get('page', 1, type=int)
    contact = Contacts.query.filter(Contacts.folder_name == name).paginate(page=page, per_page=10, error_out=False)
    return render_template('dashboard/contacts/folder.html', items=contact.items, pagination=contact)

@contacts.get('/import')
def importcontact():
    foldername = request.args.get('folder')
    return render_template('dashboard/contacts/import.html', folder=foldername)

@contacts.post('/import')
def importaction():
    foldername = request.form.get('folder_name')

    if foldername is None or foldername == '':
        flash("Folder name cannot be empty", category='error')
        return redirect(url_for('contacts.index'))
    
    file = request.files.get('import')
    excel = pd.read_excel(BytesIO(file.stream.read()))
    to_dict = excel.to_dict()
    contactList = list()
    for keys, value in to_dict['phonenumber'].items():
        value = str(value)
        if value[0:2] == '08':
            value = '+62' + value[1:-1]
        elif value[0:2] == '62':
            value = '+' + value
        elif value[0] == '8':
            value = '+62' + value
        contactList.append(Contacts(phonenumber=value))
    try:
        db.session.add_all(contactList)
        db.session.commit()
    except:
        db.session.rollback()
    file.close()
    flash('Success Import Contacts', category='info')
    return redirect(url_for('contacts.index'))

@contacts.get('/remove/<int:id>')
def remove(id):
    con = Contacts.query.filter(Contacts.id == id).first_or_404()
    try:
        db.session.delete(con)
        db.session.commit()
        flash('Success Remove contact', category='info')
    except:
        db.session.rollback()
        flash('Failed Remove contact', category='error')
    return redirect(url_for('contacts.index'))

@contacts.get('/removefolder/<int:name>')
def removefolder(name):
    
    try:
        Contacts.query.filter(Contacts.folder_name == name).delete()
        db.session.commit()
        flash('Success Remove Folder', category='info')
    except:
        flash('Failed Remove Folder', category='error')
        db.session.rollback()
    return redirect(url_for('contacts.index'))