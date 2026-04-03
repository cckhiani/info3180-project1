from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, IntegerField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, InputRequired, Length


class PropertyForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(message='Title is required'), Length(min=3, max=255)])
    description = TextAreaField('Description', validators=[DataRequired(message='Description is required')])
    bedrooms = IntegerField('Number of Bedrooms', validators=[InputRequired(message='Number of bedrooms is required')])
    bathrooms = IntegerField('Number of Bathrooms', validators=[InputRequired(message='Number of bathrooms is required')])
    location = StringField('Location', validators=[DataRequired(message='Location is required'), Length(min=3, max=255)])
    price = StringField('Price', validators=[DataRequired(message='Price is required')])
    property_type = SelectField('Property Type', choices=[('House', 'House'), ('Apartment', 'Apartment')], validators=[DataRequired(message='Property type is required')])
    photo = FileField('Property Photo', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!'), InputRequired(message='Photo is required')])
    submit = SubmitField('Add Property')
