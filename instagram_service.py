import os
from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv

from models import Story

load_dotenv()
engine = create_engine(os.environ.get("DB_URL"))
Base = declarative_base()
Base.metadata.bind = engine
Session = sessionmaker(bind=engine)
session = Session()


def build_story(username):
    base = {}
    user_story = session.query(Story).filter(Story.username == username).all()
    base['id'] = user_story[0].owner_id
    base['photo'] = user_story[0].profile_pic_url
    base['name'] = user_story[0].username
    base['link'] = ''
    base['lastUpdated'] = ''
    base['seen'] = False
    ss = []
    for s in user_story:
        d = {}
        d['id'] = s.story_id
        d['type'] = s.type
        d['length'] = s.length
        d['src'] = s.src
        d['preview'] = s.preview
        d['link'] = ''
        d['linkText'] = ''
        d['time'] = datetime.timestamp(s.time)
        d['seen'] = s.seen
        ss.append(d)
    base['items'] = ss
    return base


if __name__ == '__main__':
    print(build_story('takubeats'))
