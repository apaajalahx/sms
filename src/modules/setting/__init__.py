from flask import Blueprint
from flask_login import login_required

setting = Blueprint('setting', __name__)

@setting.before_request
@login_required
def test():
    pass