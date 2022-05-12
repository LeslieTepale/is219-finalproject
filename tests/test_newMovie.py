import logging

from app import db
from app.db.models import User, Movies

def test_adding_movie(application):
    log = logging.getLogger("myApp")
    with application.app_context():
        assert db.session.query(User).count() == 0
        assert db.session.query(Movies).count() == 0
        user = User('ltepale24@gmail.com', 'testtest')
        db.session.add(user)
        user = User.query.filter_by(email='ltepale24@gmail.com').first()
        log.info(user)
        assert user.email == 'ltepale24@gmail.com'
        user.movies= [Movies("Star Wars","99","it was alright","05/11/22")]
        db.session.commit()
        assert db.session.query(Movies).count() == 1
        movies1 = Movies.query.filter_by(title='Star Wars').first()
        assert movies1.title == "Star Wars"
        movies1.title = "Star Wars"
        db.session.commit()
        db.session.delete(user)
        db.session.delete(movies1)
        assert db.session.query(User).count() == 0
        assert db.session.query(Movies).count() == 0




