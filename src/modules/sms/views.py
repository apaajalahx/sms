from . import sms
from flask import render_template, redirect, url_for, flash, jsonify, request
from src.worker import sendSms, QueueList
from queue import Queue
from threading import Thread
import threading
from src.models import Contacts, ThreadingStatus, AwsSetting, Twilio, NexmoVonage, Templates
from random import randrange
from src import db


@sms.get('/')
def index():
    page = request.args.get('page', 1, type=int)
    threadingStatus = ThreadingStatus.query.paginate(page=page, per_page=10, error_out=False)
    return render_template('dashboard/sms/index.html', items=threadingStatus.items, pagination=threadingStatus)

@sms.get('/list_current_process')
def currentprocess():
    return render_template('dashboard/sms/list_process.html')

@sms.get('/api/current_process')
def apicurrentprocess():
    listThread = list()
    for t in threading.enumerate():
        if t.name in QueueList:
            listThread.append(QueueList[t.name])
    return jsonify(listThread)

@sms.get('/thread/<string:name>')
def getthreadprocess(name):
    if name in QueueList:
        return jsonify(QueueList[name])

@sms.get('/add_process')
def add():
    contactsFolder = Contacts.groupByAll()
    aws = AwsSetting.query.all()
    twilio = Twilio.query.all()
    vonage = NexmoVonage.query.all()
    templates = Templates.query.all()
    return render_template('dashboard/sms/add.html', items=contactsFolder, aws=aws, twilio=twilio, vonage=vonage, templates=templates)

@sms.post('/add_process')
def addprocess():
    try:
        folder = request.form.get('folder_name')
        template_id = request.form.get('template_id')
        provider = request.form.get('provider')

        if folder is None or provider is None or template_id is None:
            flash('Folder and Provider cannot empty.', category='error')
            return redirect(url_for('sms.add'))

        split = provider.split(',')
        provider_id = split[0]
        provider_type = split[1]

        msg = Templates.query.filter(Templates.id==template_id).first()
        if msg is None:
            flash('Template not found.', category='error')
            return redirect(url_for('sms.add'))

        getAll = Contacts.query.filter(Contacts.folder_name==folder).all()
        if len(getAll) == 0:
            flash('Folder {} has no phonenumber'.format(folder))
            return redirect(url_for('sms.add'))
        
        q = Queue(maxsize=len(getAll))
        q.qsize()
        for data in getAll:
            q.put(data.phonenumber)
        thread_name = 'SENDSMS' + str(randrange(00000,99999))
        QueueList[thread_name] = {
            'is_active' : True,
            'completed' : False,
            'thread_name' : thread_name,
            'size' : len(getAll),
            'current_process' : 0,
            'success' : 0,
            'failed' : 0
        }
        saved = ThreadingStatus(name=thread_name,
                                is_active=True, 
                                completed=False, 
                                size=len(getAll), 
                                success_count=0, 
                                failed_count=0, 
                                Account_type=provider_type, 
                                Account_id=provider_id)
        db.session.add(saved)
        db.session.commit()
        worker = Thread(target=sendSms, args=(thread_name, msg.messages, provider_id, provider_type, q))
        worker.daemon = True
        worker.name = thread_name
        worker.start()
        flash('Success add new Process', category='info')
    except:
        flash('Failed add new Process', category='error')
    return redirect(url_for('sms.currentprocess'))