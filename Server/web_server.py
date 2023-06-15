from flask import Flask, request, render_template
from SummerX import SummerizX
from flask_cors import CORS

import json

app = Flask(__name__)
CORS(app, origins=r'https://www.amazon.com/*')

@app.route('/', methods=['GET', 'POST', 'OPTIONS'])
def index():
    if request.headers.get('content-type') == 'application/json':
        reviews = request.get_json().get('reviews')
        smX = SummerizX(reviews).summerize()
        
        return json.dumps({'template': render_template('index.html', smX=smX), 'review': smX})

    return render_template('index.html', smX='')