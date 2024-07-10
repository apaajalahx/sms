from . import setting
from src import db
from src.models import AwsSetting, NexmoVonage, Twilio
from flask import render_template, redirect, url_for, flash, request

## aws
@setting.get('/aws')
def awsindex():
    page = request.args.get('page', 1, type=int)
    aws = AwsSetting.query.paginate(page=page, per_page=10, error_out=False)
    return render_template('dashboard/aws/index.html', items=aws.items, pagination=aws)

@setting.get('/awsadd')
def awsadd():
    return render_template('dashboard/aws/add.html')

@setting.post('/awsadd')
def awsaddPost():
    access_key = request.form.get('aws_access_key')
    secret_key = request.form.get('aws_secret_key')
    region = request.form.get('aws_region')
    ph = request.form.get('phonenumber')
    if access_key is None or secret_key is None or region is None or ph is None:
        flash('Error make sure access_key, secret_key, region or phonenumber is filled.', category='error')
        return redirect(url_for('setting.awsadd'))

    if access_key == '' or secret_key == '' or region == '' or ph == '':
        flash('Error make sure access_key, secret_key, region or phonenumber is filled.', category='error')
        return redirect(url_for('setting.awsadd'))
    aws = AwsSetting(aws_access_key=access_key, aws_secret_key=secret_key, aws_region=region, phonenumber=ph)
    try:
        db.session.add(aws)
        db.session.commit()
        flash('Success add new aws account', category='info')
    except:
        flash('Error failed save new aws account', category='error')
        db.session.rollback()

    return redirect(url_for('setting.awsindex'))

@setting.get('/awsremove/<int:id>')
def awsremove(id):
    aws = AwsSetting.query.filter(AwsSetting.id == id).first_or_404()
    try:
        db.session.delete(aws)
        db.session.commit()
        flash('Success Remove Aws Account', category='info')
    except:
        db.session.rollback()
        flash('Failed Remove Aws Account', category='error')
    return redirect(url_for('setting.awsindex'))


# twilio
@setting.get('/twilio')
def twilioindex():
    page = request.args.get('page', 1, type=int)
    tw = Twilio.query.paginate(page=page, per_page=10, error_out=False)
    return render_template('dashboard/twilio/index.html', items=tw.items, pagination=tw)

@setting.get('/twilioadd')
def twilioadd():
    return render_template('dashboard/twilio/add.html')

@setting.post('/twilioadd')
def twilioaddPost():
    account_sid = request.form.get('twilio_account_sid')
    auth_token = request.form.get('twilio_auth_token')
    ph = request.form.get('phonenumber')
    if account_sid is None or auth_token is None or ph is None:
        flash('Error make sure twilio_account_sid and twilio_account_sid is filled.', category='error')
        return redirect(url_for('setting.twilioadd'))

    if account_sid == '' or auth_token == '' or ph == '':
        flash('Error make sure twilio_account_sid and twilio_account_sid is filled.', category='error')
        return redirect(url_for('setting.twilioadd'))
    tw = Twilio(twilio_account_sid=account_sid, twilio_auth_token=auth_token, phonenumber=ph)
    try:
        db.session.add(tw)
        db.session.commit()
        flash('Success add new twilio account', category='info')
    except:
        flash('Error failed save new twilio account', category='error')
        db.session.rollback()

    return redirect(url_for('setting.twilioindex'))

@setting.get('/twilioremove/<int:id>')
def twilioremove(id):
    tw = Twilio.query.filter(Twilio.id == id).first_or_404()
    try:
        db.session.delete(tw)
        db.session.commit()
        flash('Success Remove Twilio Account', category='info')
    except:
        db.session.rollback()
        flash('Failed Remove Twilio Account', category='error')
    return redirect(url_for('setting.twilioindex'))


# vonage
@setting.get('/vonage')
def vonageindex():
    page = request.args.get('page', 1, type=int)
    vn = NexmoVonage.query.paginate(page=page, per_page=10, error_out=False)
    return render_template('dashboard/vonage/index.html', items=vn.items, pagination=vn)

@setting.get('/vonageadd')
def vonageadd():
    return render_template('dashboard/vonage/add.html')

@setting.post('/vonageadd')
def vonageaddPost():
    api_key = request.form.get('vonage_api_key')
    api_secret = request.form.get('vonage_api_secret')
    ph = request.form.get('phonenumber')
    if api_key is None or api_secret is None or ph is None:
        flash('Error make sure api_key and api_secret is filled.', category='error')
        return redirect(url_for('setting.vonageadd'))

    if api_key == '' or api_secret == '' or ph == '':
        flash('Error make sure api_key and api_secret is filled.', category='error')
        return redirect(url_for('setting.vonageadd'))
    vn = NexmoVonage(vonage_api_key=api_key, vonage_api_secret=api_secret, phonenumber=ph)
    try:
        db.session.add(vn)
        db.session.commit()
        flash('Success add new vonage account', category='info')
    except:
        flash('Error failed save new vonage account', category='error')
        db.session.rollback()

    return redirect(url_for('setting.vonageindex'))

@setting.get('/vonageremove/<int:id>')
def vonageremove(id):
    vn = NexmoVonage.query.filter(NexmoVonage.id == id).first_or_404()
    try:
        db.session.delete(vn)
        db.session.commit()
        flash('Success Remove Vonage Account', category='info')
    except:
        db.session.rollback()
        flash('Failed Remove Vonage Account', category='error')
    return redirect(url_for('setting.vonageindex'))