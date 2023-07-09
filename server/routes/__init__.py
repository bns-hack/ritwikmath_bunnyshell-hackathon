from routes.view import view_bp
from routes.api import api_bp

def register(app):
    app.register_blueprint(view_bp)
    app.register_blueprint(api_bp)