from flask import Flask, render_template, request

from flask_wtf import CSRFProtect
from form import ProductForm

import secrets

from view_review import SummerizX

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)

csrf = CSRFProtect(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    output = {
            'info': 'Your prduct review will show here', 
            'product': '',
            'summary': '',
            'img_src': ''
        }
    rainForest_api = False

    url = ''

    if request.method == 'POST' and request.headers.get('Content-Type') == 'application/json':
        smX = SummerizX(url)
        reviews_data = request.get_json()
        smX.reviews = reviews_data.reviews
        product, img_src, summerize = smX.summerize()

        output = {
            'info': '', 
            'product': reviews_data.product,
            'summary': summerize,
            'img_src': reviews_data.img_src
        }

    else:
        product_form = ProductForm()
        pass
        if product_form.validate_on_submit():

            url = product_form.url.data

            smX = SummerizX(url)

            summerize = smX.summerize()

            #temporary solution for when the host (pythonanywhere) blocks rainforestapi
            if type(summerize) == tuple:
                product, img_src, summary = summerize

                output = {
                    'info': '',
                    'product': product,
                    'summary': summary,
                    'img_src': img_src
                }

            else:
                rainForest_api = summerize

    return render_template('index.html', product_form=product_form, output=output, rainForest_api=rainForest_api)