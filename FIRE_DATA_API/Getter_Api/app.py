#Flask Imports 
from flask import Flask, jsonify, request
from flask_restful import Api, reqparse
from flask_cors import CORS


from models import Schema
from service import ToDoService
app = Flask(__name__)

@app.route('/')
def hello():
  return "Hello World!"

if __name__ == "__main__":
  Schema()
  app.run(debug=True)

@app.route("/todo", method=["POST"])
def create_todo():