from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField
from wtforms.validators import DataRequired, ValidationError
import re

def check_currency(form, field):
    currency = str(field.data)
    check = re.match("^[0-9]*(\.[0-9]{0,2})?$", currency)
    if not check:
        raise ValidationError('Please add a currency! (For example 2.99, 12.42)')

class PlanCreationForm(FlaskForm):
    name = StringField('Plan Name', validators=[
        DataRequired()
    ])
    budget = DecimalField('Budget', places=2, validators=[
        DataRequired(), check_currency
    ])
    submit = SubmitField('Submit')

class ExpenseForm(FlaskForm):
    type = StringField('Expense Type', validators=[
        DataRequired()
    ])
    expense = DecimalField('Expense', places=2, validators=[
        DataRequired(), check_currency
    ])
    submit = SubmitField('Save')
