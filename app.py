from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema

import instaloader
from instagram_service import build_story
import instagram_helper

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:18091997@localhost/archivegram"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)
CORS(app)

L = instaloader.Instaloader()
L.load_session_from_file("andriyorehov")


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    full_name = db.Column(db.String)
    profile_pic_url = db.Column(db.String)
    pk = db.Column(db.String(512))

    def __init__(self, username, full_name, profile_pic_url, pk):
        self.username = username
        self.full_name = full_name
        self.profile_pic_url = profile_pic_url
        self.pk = pk


class UserSchema(ModelSchema):
    class Meta:
        model = User


# db.create_all()
user_schema = UserSchema()


# def download_user_stories():
# profile = instaloader.Profile.from_username(L.context, "jc_ru")
# print(profile.userid)
# for story in L.get_stories(userids=[1388643]):
#     # story is a Story object
#     for item in story.get_items():
#         # item is a StoryItem object
#         L.download_storyitem(item, ':stories')


@app.route('/users', methods=['POST'])
def users():
    user = request.get_json()
    new_user = User(user['username'], user['full_name'], user['profile_pic_url'], user['pk'])
    db.session.add(new_user)
    return user_schema.dump(new_user)


@app.route('/users/<user_pk>', methods=['DELETE'])
def user_delete(user_pk):
    User.query.filter_by(pk=user_pk).delete()
    return 'OK'


@app.route('/users', methods=['GET'])
def users_get():
    query = User.query.all()
    serialized = [user_schema.dump(i) for i in query]
    return jsonify({"users": serialized})


@app.route('/instagram-user', methods=['GET'])
def instagram_user():
    username = request.args.get('username')
    results = instagram_helper.search_instagram_users(username)
    return jsonify(results)


@app.route('/stories/<path:path>')
def send_js(path):
    print(path)
    return send_from_directory('stories', path)


@app.route('/stories', methods=['GET'])
def stories():
    return jsonify(build_story('takubeats'))


if __name__ == "__main__":
    app.run(port=3000, debug=True)
