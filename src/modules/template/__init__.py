from flask import Blueprint
from flask_login import login_required

template = Blueprint('template', __name__)

@template.before_request
@login_required
def before_request():
    pass