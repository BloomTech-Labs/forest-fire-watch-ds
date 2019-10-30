#Flask Imports 
from flask import Flask
from flask_restful import Api

# DS Logic imports
import pandas as pd
import numpy as np
from math import radians, cos, sin, asin, sqrt


def create_app():
    """
    Creates and configures an instance of our Flask API
    """
    app = Flask(__name__)
    app.run(debug=True)

    # initialize the api wrapper
    api = Api(app)

    @app.route("/running", methods=["GET"])
    def running():
        return 'Its up and possibly working'

    return app


