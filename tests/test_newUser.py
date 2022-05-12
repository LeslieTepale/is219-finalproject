import logging

from app import db
from app.db.models import User

def test_adding_user(application):
    log = logging.getLogger("myApp")
    with application.app_context():
        assert db.session.query(User).count() == 0
        user = User('ltepale24@gmail.com', 'testtest')
        db.session.add(user)
        user = User.query.filter_by(email='ltepale24@gmail.com').first()
        log.info(user)
        assert user.email == 'ltepale24@gmail.com'
        db.session.delete(user)
        assert db.session.query(User).count() == 0
