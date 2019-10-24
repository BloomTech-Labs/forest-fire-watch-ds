"""
Entry point for our Fire Data API
"""
from .app import create_app


app = create_app()
#this deals with the db somehow
# app.app_context().push()


