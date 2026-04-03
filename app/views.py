"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file contains the routes for your application.
"""

from app import app, db
from app.models import Property
from app.forms import PropertyForm
from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from datetime import datetime
import os


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")


###
# Property Routes
###

@app.route('/properties/create', methods=['GET', 'POST'])
def create_property():
    """Display form and handle property creation."""
    form = PropertyForm()
    
    if request.method == 'POST' and form.validate_on_submit():
        # Handle file upload
        photo = form.photo.data
        filename = secure_filename(photo.filename)
        # Add timestamp to make filename unique
        filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}__{filename}"
        
        # Create uploads directory if it doesn't exist
        uploads_dir = os.path.join(app.root_path, 'static', 'uploads')
        os.makedirs(uploads_dir, exist_ok=True)
        
        # Save the file
        photo.save(os.path.join(uploads_dir, filename))
        
        # Create new property
        property_obj = Property(
            title=form.title.data,
            description=form.description.data,
            bedrooms=form.bedrooms.data,
            bathrooms=form.bathrooms.data,
            location=form.location.data,
            price=float(form.price.data),
            property_type=form.property_type.data,
            photo_filename=filename
        )
        
        db.session.add(property_obj)
        db.session.commit()
        
        flash('Property successfully added!', 'success')
        return redirect(url_for('properties'))
    
    if form.errors:
        flash_errors(form)
    
    return render_template('create_property.html', form=form)


@app.route('/properties')
def properties():
    """Display list of all properties."""
    all_properties = Property.query.all()
    return render_template('properties.html', properties=all_properties)


@app.route('/properties/<int:property_id>')
def property_detail(property_id):
    """Display individual property details."""
    property_obj = Property.query.get_or_404(property_id)
    return render_template('property_detail.html', property=property_obj)




# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
