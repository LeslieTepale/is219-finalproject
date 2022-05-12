from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields import *

class movie_register_form(FlaskForm):
    title = TextAreaField('Title', [validators.DataRequired(),], description="Enter a movie")
    rating = TextAreaField('Rating', [validators.DataRequired(),], description="Enter a rating percentage")
    review = TextAreaField('Review', [ validators.DataRequired(),], description="Enter your review")
    date = TextAreaField('Date Reviewed', [validators.DataRequired(),], description="Enter review date")
    submit = SubmitField()

class movie_edit_form(FlaskForm):
    title = TextAreaField('Title', [validators.length(min=6, max=300)],
                          description="Please add movie title")
    rating = TextAreaField('Rating', [validators.length(min=1, max=300)],
                          description="Please add rating percentage")
    review = TextAreaField('Review', [validators.length(min=1, max=300)],
                          description="Please add your review")
    date = TextAreaField('Date', [validators.length(min=1, max=300)],
                          description="Please add a new date")
    submit = SubmitField()