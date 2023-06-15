from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length
from flask_wtf import FlaskForm

class ProductForm(FlaskForm):
    url = URLField(label='Product Url', validators=[DataRequired()])
    submit = SubmitField('Submit')