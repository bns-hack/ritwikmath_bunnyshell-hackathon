import os
from flask import Flask, request, Blueprint, render_template
from dotenv import load_dotenv
load_dotenv()

app: Flask = Flask(__name__)

@app.get('/')
def index():
    return render_template('index.html')

@app.get('/env')
def env():
    return os.getenv('MONGO_URL')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)