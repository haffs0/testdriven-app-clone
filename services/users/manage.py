# services/users/manage.py

import unittest
import coverage
from flask.cli import FlaskGroup

from project import create_app, db
from project.api.models import User


COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*',
        'project/config.py',
    ]
)
COV.start()

app = create_app()
cli = FlaskGroup(create_app=create_app)

@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command("test")
def test():
    """Runs the tests without code coverage"""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

@cli.command("seed_db")
def seed_db():
    """Seeds the database."""
    db.session.add(User(
        username='michael',
        email="hermanmu@gmail.com",
        password='greaterthaneight'
    ))
    db.session.add(User(
        username='michaelherman',
        email="michael@mherman.org",
        password='greaterthaneight'
    ))
    db.session.commit()

@cli.command("cov")
def cov():
    """Runs the unit test with coverage."""
    tests = unittest.TestLoader().discover('project/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1

if __name__ == '__main__':
    cli()
