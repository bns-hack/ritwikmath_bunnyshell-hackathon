from routes.view import view_bp
from routes.api import api_bp
from routes.auth import auth_bp

def register(app):
    app.register_blueprint(view_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(auth_bp)