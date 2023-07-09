from flask import Blueprint, render_template

view_bp = Blueprint('view', __name__, url_prefix='/')


@view_bp.get('/')
def fetchAlllogs():
    try:
        return render_template('index.html')
    except Exception as ex:
        return render_template('errors/503.html')