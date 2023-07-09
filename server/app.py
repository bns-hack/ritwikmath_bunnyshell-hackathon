import os
from routes import register
from flask import Flask, request
from dotenv import load_dotenv
load_dotenv()

app: Flask = Flask(__name__)

if __name__ == "__main__":
    register(app)
    app.run(debug=True, host="0.0.0.0", port=5000)