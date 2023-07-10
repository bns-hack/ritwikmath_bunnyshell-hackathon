from flask import Blueprint, render_template

view_bp = Blueprint('view', __name__, url_prefix='/')


@view_bp.get('/')
def plan_view():
    try:
        return render_template('index.html')
    except Exception as ex:
        return render_template('errors/503.html')

@view_bp.get('/subscription')
def subscription_view():
    try:
        return render_template('subscription.html')
    except Exception as ex:
        return render_template('errors/503.html')