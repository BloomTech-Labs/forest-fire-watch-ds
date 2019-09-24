"""
API Resources.
"""

from flask import jsonify, request
from flask_restful import Resource
from .functions import check_fires
from .models import db, Fire

# time import
import datetime


class CheckFires(Resource):
    """
    Get's User long/lat coordinates and returns a json with all fires in their radius
    """

    def post(self):
        values = request.get_json()

        user_coords = values["user_coords"]  # I want to get a json like:
        # {'user_coords' : (long, lat), 'distance': number}
        try:
            perimiter = values["distance"]
        except:
            perimiter = 50

        # get all positive fire coords from our db that are not older than 5 days
        time_limit = datetime.timedelta(days=5)
        ts = datetime.datetime.now()

        fire_query = Fire.query.filter(
            Fire.fire == 1, (ts - Fire.timestamp) < time_limit
        )
        fire_coords = [(float(x.longitude), float(x.latitude)) for x in fire_query]

        return jsonify(check_fires(user_coords, perimiter, fire_coords))


class AllFires(Resource):
    """
    Returns a json with all active fires
    """

    def get(self):

        # get all fire coords less than 5 days old
        time_limit = datetime.timedelta(days=5)
        ts = datetime.datetime.now()

        fire_coords = [
            (float(x.longitude), float(x.latitude))
            for x in Fire.query.filter(
                Fire.fire == 1, (ts - Fire.timestamp) < time_limit
            )
        ]

        results = {"Alert": True, "Fires": [tuple(x) for x in fire_coords]}

        return jsonify(results)
