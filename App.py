from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_heroku import Heroku

app = Flask(__name__)
heroku = Heroku(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "SQLite://localhost/5000/"

CORS(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Userdata(db.Model):
  __tablename__="userdatas"
  id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String(20))
  last_name = db.Column(db.String(20))
  age = db.Column(db.String(20))
  short_description = db.Column(db.String(100))
  sub_heading = db.Column(db.String(50))
  headline = db.Column(db.String(50))
  description_one = db.Column(db.String(1000))
  description_two = db.Column(db.String(1000))
  images = db.Column(db.PickleType)
  social_media = db.Column(db.PickleType)

  def __init__(self, title, done):
    self.title = title
    self.done = done

class UserdataSchema(ma.Schema):
  class Meta:
    fields = (
      "id",
      "first_name",
      "last_name",
      "age",
      "short_description",
      "sub_heading",
      "headline",
      "description_one",
      "description_two",
      "images"
      )

userdata_schema = UserdataSchema()
userdatas_schema = UserdataSchema(many=True)


@app.route("/userdatas", methods=["GET"])
def get_userdatas():
  all_userdatas = Userdata.query.all()
  result = userdatas_schema.dump(all_userdatas)
  return jsonify(result)

@app.route("/userdata", methods=["POST"])
def add_userdata():
  first_name = request.json["first_name"]
  last_name = request.json["last_name"]
  age = request.json["age"]
  short_description = request.json["short_description"]
  sub_heading = request.json["sub_heading"]
  headline = request.json["headline"]
  description_one = request.json["description_one"]
  description_two = request.json["description_two"]
  images = request.json["images"]

  new_userdata = Userdata(
    first_name,
    last_name,
    age,
    short_description,
    sub_heading,
    headline,
    description_one,
    description_two,
    images
    )
  db.session.add(new_userdata)
  db.session.commit()

  created_userdata = Userdata.query.get(new_userdata.id)
  return userdata_schema.jsonify(created_userdata)

@app.route("/userdata/<id>", methods=["PUT"])
def update_userdata(id):
  userdata = Userdata.query.get(id)

  userdata.title = request.json["title"]
  userdata.done = request.json["done"]

  db.session.commit()
  return userdata_schema.jsonify(userdata)

@app.route("/userdata/<id>", methods=["DELETE"])
def delete_userdata(id):
  userdata = Userdata.query.get(id)
  db.session.delete(userdata)
  db.session.commit()

  return "RECORD DELETED"

if __name__ == "__main__":
  app.debug = True
  app.run()