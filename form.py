from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, validators


class MyForm(FlaskForm):
    species = StringField('Species', validators=[validators.DataRequired(), validators.Length(min=3)])
    breed = StringField('Breed', validators=[validators.DataRequired(), validators.Length(min=3)])
    age = FloatField('Age', validators=[validators.DataRequired()])
    gender = StringField('Gender', validators=[validators.DataRequired(), validators.Length(min=3)])
    submit = SubmitField('Submit')