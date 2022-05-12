"""This makes the test configuration setup"""
# pylint: disable=redefined-outer-name
import logging
import os

import pytest
from app import create_app, User
from app.db import db

@pytest.fixture()
def application():
    os.environ['FLASK_ENV'] = 'testing'

    application = create_app()
    with application.app_context():
        db.create_all()
        yield application
        db.session.remove()

@pytest.fixture()
def add_user(application):
    with application.app_context():
        user = User('ltepale24@gmail.com', 'testtest')
        db.session.add(user)
        db.session.commit()

@pytest.fixture()
def client(application):
    return application.test_client()

@pytest.fixture()
def runner(application):
    return application.test_cli_runner()
