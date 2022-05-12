import csv
import json
import logging
import os

from flask import Blueprint, render_template, abort, url_for, current_app, jsonify, flash
from flask_login import current_user, login_required
from jinja2 import TemplateNotFound

from app.db import db
from app.db.models import Movies
from app.movies.forms import movie_register_form, movie_edit_form
from werkzeug.utils import secure_filename, redirect
from flask import Response



movies = Blueprint('movies', __name__,template_folder='templates')

@movies.route('/movies', methods=['GET'], defaults={"page": 1})
@movies.route('/movies/<int:page>', methods=['POST','GET'])
def browse_locations(page):
    page = page
    per_page = 10
    pagination = Movies.query.paginate(page, per_page, error_out=False)
    data = pagination.items
    try:
        titles = [('number', '#'), ('title', 'Title'), ('rating', 'Rating'), ('review', 'Review'),
                  ('date', 'Date Reviewed'), ('user_id', 'User Id')]
        retrieve_url = ('map.retrieve_location', [('location_id', ':id')])
        edit_url = ('map.edit_locations', [('location_id', ':id')])
        add_url = url_for('map.add_location')
        delete_url = ('map.delete_location', [('location_id', ':id')])
        return render_template('browse_movies.html',data=data,pagination=pagination, titles=titles, model=Movies, add_url=add_url,
                               edit_url=edit_url,
                               delete_url=delete_url,
                            Movie=Movies, record_type="Movies")
    except TemplateNotFound:
        abort(404)

@movies.route('/movies/<int:movies_id>')
@login_required
def retrieve_location(movies_id):
    movies = Movies.query.get(movies_id)
    return render_template('review_view.html', movies=Movies)


@movies.route('/movies/<int:movies_id>/edit', methods=['POST', 'GET'])
@login_required
def edit_locations(movie_id):
    location = Location.query.get(location_id)
    form = location_edit_form(obj=location)
    if form.validate_on_submit():
        location.title = form.title.data
        db.session.add(location)
        db.session.commit()
        flash('Location Edited Successfully', 'success')
        current_app.logger.info("edited a location")
        return redirect(url_for('map.browse_locations'))
    return render_template('location_edit.html', form=form)


@movies.route('/locations/new', methods=['POST', 'GET'])
@login_required
def add_location():
    form = location_register_form()
    if form.validate_on_submit():
        location = Location.query.filter_by(title=form.title.data).first()
        if location is None:
            location = Location(title=form.title.data, longitude=form.longitude.data, latitude=form.latitude.data, population=form.population.data)
            db.session.add(location)
            db.session.commit()
            flash('Congratulations, you just created a location', 'success')
            return redirect(url_for('map.browse_locations'))
        else:
            flash('Already Registered')
            return redirect(url_for('map.locations'))
    return render_template('location_new.html', form=form)


@map.route('/locations/<int:location_id>/delete', methods=['POST'])
@login_required
def delete_location(location_id):
    location = Location.query.get(location_id)
    db.session.delete(location)
    db.session.commit()
    flash('Location Deleted', 'success')
    return redirect(url_for('map.browse_locations'), 302)
