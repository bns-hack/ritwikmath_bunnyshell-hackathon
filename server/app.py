import os
from flask import Flask, request
from dotenv import load_dotenv
load_dotenv()

app: Flask = Flask(__name__)

@app.get('/')
def index():
    return os.getenv('MONGO_URL')

if __name__ == "__main__":
    app.run(debug=True)