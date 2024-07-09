from . import dashboard
from flask import render_template
from flask_login import login_required


@dashboard.get('/')
@login_required
def index():
    return render_template('dashboard/index.html')