from flask import Flask, request, jsonify
from flask_cors import CORS

from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:18091997@localhost/archivegram"
db = SQLAlchemy(app)
CORS(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String)
    username = db.Column(db.String, unique=True, nullable=False)


class UserSchema(ModelSchema):
    class Meta:
        model = User


# db.create_all()

user_schema = UserSchema()


@app.route('/users', methods=['POST'])
def users():
    user = request.get_json()['user']
    username = user['username']
    db.session.add(User(username=username))
    db.session.commit()
    return username


@app.route('/users', methods=['GET'])
def users_get():
    query = User.query.all()
    serialized = [user_schema.dump(i) for i in query]
    return jsonify({"users": serialized})


if __name__ == "__main__":
    app.run(port=3000, debug=True)
