from flask import Blueprint
from flask_login import login_required

sms = Blueprint('sms', __name__)

@sms.before_request
@login_required
def before_request():
    pass