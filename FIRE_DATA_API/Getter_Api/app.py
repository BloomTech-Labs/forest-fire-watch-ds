import os
#Flask Imports 
from flask import Flask, jsonify, request
from flask_restful import Api, reqparse
from flask_cors import CORS

from models import db
# from service import 


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
    )  # apparently this doesn't really work so commenting out for now

    app.app_context().push()
    db.init_app(app)

    # enable CORS on all app routes
    CORS(app)

    # initialize the api wrapper
    api = Api(app)

    # connects resources to api endpoint
    # api.add_resource(CheckFires, "/check_fires")
    # api.add_resource(AllFires, "/all_fires")

    return app





# from service import
# @app.route('/')
# def hello():
#   return "Hello World!"

# if __name__ == "__main__":
#   Schema()
#   app.run(debug=True)

# @app.route("/todo", method=["POST"])


