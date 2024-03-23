from app import create_app, db
from dotenv import load_dotenv
import os
import click
import sys

load_dotenv()

app = create_app(os.getenv("FLASK_CONFIG") or 'default')

@app.cli.command()
def test():
    """Run the unit tests"""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)