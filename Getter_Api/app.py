# System Imports
import os
import requests
import json 

#Flask Imports 
from flask import Flask, jsonify, request
from flask_restful import Api, reqparse
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# Local imports
from .models import db, Modis
from .functions import (
    pull_modis, 
    process_live_data, 
    add_training_data, 
    haversine
)

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
    # create db first

    # configure database variables
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["ENV"] = os.environ.get(
        "ENV"
    )

    app.app_context().push()
    db.init_app(app)

    # enable CORS on all app routes
    CORS(app)

    # initialize the api wrapper
    api = Api(app)

"""     @app.route("/instantiate_db", methods=["POST"])
    def instantiate_db():
        values = request.get_json()
        # expecting a json {'reset' : "TRUE", 'password' : 'ballderdash'}

        time_now = datetime.datetime.now()
        for key, item in values.items():
            print(key, type(item), item)

        if values["reset"] == "TRUE" and values["password"] == 'ballderdash':
            print('dropping db')
            db.drop_all()
            print('db dropped')
            db.create_all()
            print('db created')

            return jsonify(
                {"error": False, "message": "db created successfully", "time": time_now}
            )
        else:
            return jsonify(
                {
                    "error": True,
                    "message": "either auth failed or reset was not enabled",
                    "time": time_now,
                }
            ) """


    @app.route("/instantiate_db", methods=["GET"])
    def instantiate_db():
        time_now = datetime.datetime.now()
        print('dropping db')
        db.drop_all()
        print('db dropped')
        db.create_all()
        print('db created')

        return jsonify(
            {"error": False, "message": "db created successfully", "time": time_now}
        )

    
    @app.route("/update_db", methods=["GET"])
    def update_db():
        try:
            # Get new data and clean it
            dirty_data = pull_modis()
            clean_data = process_live_data(dirty_data)

            # Add data to db
            add_training_data(clean_data)
        
        except:
            return jsonify({"error": True, "message": "something happened"})


    return app


