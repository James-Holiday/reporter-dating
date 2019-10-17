from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_heroku import Heroku

app = Flask(__name__)
heroku = Heroku(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://ythrqvqezptnld:0142f7424cc48e9b67d3130eb5829f75ae2ec4b0c89d09898b5004af62d7a709@ec2-184-73-209-230.compute-1.amazonaws.com:5432/dekpj71pm3iej7"

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
  profile_image = db.Column(db.String(1000))
  article_image = db.Column(db.String(1000))
  body_image_one = db.Column(db.String(1000))
  body_image_two = db.Column(db.String(1000))
  facebook = db.Column(db.String(1000))
  instagram = db.Column(db.String(1000))
  twitter = db.Column(db.String(1000))
  job_site = db.Column(db.String(1000))

  def __init__(
    self,
    first_name,
    last_name,
    age,
    short_description,
    sub_heading,
    headline,
    description_one,
    description_two,
    profile_image,
    article_image,
    body_image_one,
    body_image_two,
    facebook,
    instagram,
    twitter,
    job_site,
    ):
    self.first_name = first_name
    self.last_name = last_name
    self.age = age
    self.short_description = short_description
    self.sub_heading = sub_heading
    self.headline = headline
    self.description_one = description_one
    self.description_two = description_two
    self.profile_image = profile_image
    self.article_image = article_image
    self.body_image_one = body_image_one
    self.body_image_two = body_image_two
    self.facebook = facebook
    self.instagram = instagram
    self.twitter = twitter
    self.job_site = job_site

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
      "profile_image",
      "article_image",
      "body_image_one",
      "body_image_two",
      "facebook",
      "instagram",
      "twitter",
      "job_site"
      )

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
  profile_image = request.json["profile_image"]
  article_image = request.json["article_image"]
  body_image_one = request.json["body_image_one"]
  body_image_two = request.json["body_image_two"]
  facebook = request.json["facebook"]
  instagram = request.json["instagram"]
  twitter = request.json["twitter"]
  job_site = request.json["job_site"]

  new_userdata = Userdata(
    first_name,
    last_name,
    age,
    short_description,
    sub_heading,
    headline,
    description_one,
    description_two,
    profile_image,
    article_image,
    body_image_one,
    body_image_two,
    facebook,
    instagram,
    twitter,
    job_site
    )
  db.session.add(new_userdata)
  db.session.commit()

  created_userdata = Userdata.query.get(new_userdata.id)
  return userdata_schema.jsonify(created_userdata)

@app.route("/userdata/<id>", methods=["PUT"])
def update_userdata(id):
  userdata = Userdata.query.get(id)
  userdata.first_name = request.json["first_name"]
  userdata.last_name = request.json["last_name"]
  userdata.age = request.json["age"]
  userdata.short_description = request.json["short_description"]
  userdata.sub_heading = request.json["sub_heading"]
  userdata.headline = request.json["headline"]
  userdata.description_one = request.json["description_one"]
  userdata.description_two = request.json["description_two"]
  userdata.profile_image = request.json["profile_image"]
  userdata.article_image = request.json["article_image"]
  userdata.body_image_one = request.json["body_image_one"]
  userdata.body_image_two = request.json["body_image_two"]
  userdata.facebook = request.json["facebook"]
  userdata.instagram = request.json["instagram"]
  userdata.twitter = request.json["twitter"]
  userdata.job_site = request.json["job_site"]

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