"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app,db
from flask import render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
from app.models import Movie
from app.forms import MovieForm
from flask_wtf.csrf import generate_csrf
import traceback
import os


###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
@app.route('/api/v1/movies', methods=['POST'])
def movies():
    form = MovieForm(request.form)
    print(form)
    
    if form.validate_on_submit():
        try:
            # Assuming the form has a 'poster' field for an uploaded file
            poster_file = request.files.get('poster')
            filename = secure_filename(poster_file.filename)
            poster_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            poster_file.save(poster_path)

            movie = Movie(
                title=form.title.data,
                description=form.description.data,
                poster=filename  # Assuming you store just the filename
            )
            db.session.add(movie)
            db.session.commit()

            return jsonify({
                "message": "Movie Successfully added",
                "title": movie.title,
                "poster": movie.poster,
                "description": movie.description
            }), 201

        except Exception as e:
            traceback.print_exc()  # Print the traceback to the console for debugging
            return jsonify({"error": "Internal Server Error"}), 500

    else:
        # Collect form validation errors
        errors = [{"field": field, "errors": errs} for field, errs in form.errors.items()]
        return jsonify({"errors": errors}), 400


@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()})

def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

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