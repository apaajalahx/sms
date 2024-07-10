from flask import Blueprint
from flask_login import login_required

contacts = Blueprint('contacts', __name__)

@contacts.before_request
@login_required
def before_request():
    pass