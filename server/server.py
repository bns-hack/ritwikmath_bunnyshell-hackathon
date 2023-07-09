from app import app
from routes import register

if __name__ == "__main__":
    register(app)
    app.run(debug=True, host="0.0.0.0", port=5000)