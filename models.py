import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Story(Base):
    __tablename__ = 'story'
    id = sa.Column(sa.Integer, primary_key=True)
    owner_id = sa.Column(sa.String)
    profile_pic_url = sa.Column(sa.String)
    username = sa.Column(sa.String)

    story_id = sa.Column(sa.String)
    type = sa.Column(sa.String)
    length = sa.Column(sa.Integer)
    src = sa.Column(sa.String)
    preview = sa.Column(sa.String)
    link = sa.Column(sa.String)
    link_text = sa.Column(sa.String)
    time = sa.Column(sa.DateTime)
    seen = sa.Column(sa.Boolean)

    def __init__(self, owner_id, profile_pic_url, username, story_id, type, length, src, preview, link, link_text,
                 time, seen):
        self.owner_id = owner_id
        self.profile_pic_url = profile_pic_url
        self.username = username
        self.story_id = story_id
        self.type = type
        self.length = length
        self.src = src
        self.preview = preview
        self.link = link
        self.link_text = link_text
        self.time = time
        self.seen = seen