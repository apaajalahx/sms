from . import contacts
from src.models import Contacts
from src import db
from flask_login import login_required
from flask import render_template, request, redirect, url_for
import pandas as pd
from io import BytesIO


@contacts.get("")
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    contact = Contacts.query.paginate(page=page, per_page=10, error_out=False)
    return render_template('dashboard/contacts/index.html', items=contact.items, pagination=contact)

@contacts.get('/import')
@login_required
def importcontact():
    return render_template('dashboard/contacts/import.html')

@contacts.post('/import')
@login_required
def importaction():
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
    return redirect(url_for('contacts.index'))