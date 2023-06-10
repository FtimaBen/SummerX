from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5

from flask_wtf import CSRFProtect
from flask import Flask
from form import ProductForm

import secrets

from view_review import SummerizX

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)

csrf = CSRFProtect(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    product_form = ProductForm()
    output = {'info': 'Your prduct review will show here'}

    if product_form.validate_on_submit():
        url = product_form.url.data
        
        smX = SummerizX(url)
        product, summary, summary_2 = smX.summerize()

        output = {
            'product': product, 
            'summary': summary
        }

    return render_template('index.html', product_form=product_form, output=output)
