from . import template
from flask import render_template, redirect, url_for, request, flash
from src.models import Templates
from src import db


@template.get('')
def index():
    page = request.args.get('page', 1, type=int)
    templ = Templates.query.paginate(page=page, per_page=10, error_out=False)
    return render_template('dashboard/template/index.html', items=templ.items, pagination=templ)

@template.get('/add')
def add():
    return render_template('dashboard/template/add.html')

@template.post('/add')
def addpost():
    text = request.form.get('template')
    if text is None:
        flash('Error Template text cannot null/empty', category='error')
    temp = Templates(messages=text)
    try:
        db.session.add(temp)
        db.session.commit()
        flash('Success Add New Template', category='info')
    except Exception:
        db.session.rollback()
        flash('Failed Add template, unkown error', category='error')
    return redirect(url_for('template.index'))

@template.get('/remove/<int:id>')
def remove(id):
    templ = Templates.query.filter(Templates.id == id).first_or_404()
    try:
        db.session.delete(templ)
        db.session.commit()
        flash('Success Remove contact', category='info')
    except:
        db.session.rollback()
        flash('Failed Remove contact', category='error')
    return redirect(url_for('template.index'))