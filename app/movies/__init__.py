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
def browse_movies(page):
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
def retrieve_movies(movies_id):
    movies = Movies.query.get(movies_id)
    return render_template('review_view.html', movies=Movies)


@movies.route('/movies/<int:movies_id>/edit', methods=['POST', 'GET'])
@login_required
def edit_movies(movies_id):
    movie = Movies.query.get(movies_id)
    form = movie_edit_form(obj=movie)
    if form.validate_on_submit():
        movie.title = form.title.data
        db.session.add(movie)
        db.session.commit()
        flash('Location Edited Successfully', 'success')
        current_app.logger.info("edited a movie review")
        return redirect(url_for('movies.browse_movies'))
    return render_template('review_edit.html', form=form)


@movies.route('/movies/new', methods=['POST', 'GET'])
@login_required
def add_movie():
    form = movie_register_form()
    if form.validate_on_submit():
        movie = Movies.query.filter_by(title=form.title.data).first()
        if movie is None:
            movie = Movies(title=form.title.data, rating=form.rating.data, review=form.review.data, date=form.date.data)
            db.session.add(movie)
            db.session.commit()
            flash('Congratulations, you just entered a new review', 'success')
            return redirect(url_for('map.browse_movies'))
        else:
            flash('Already Registered')
            return redirect(url_for('map.locations'))
    return render_template('review_new.html', form=form)


@movies.route('/movies/<int:movies_id>/delete', methods=['POST'])
@login_required
def delete_movie(movies_id):
    movie = Movies.query.get(movies_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Review Deleted', 'success')
    return redirect(url_for('movies.browse_movies'), 302)

def showMovies():
    try:
        return render_template('review_new.html')
    except TemplateNotFound:
        abort(404)

