from datetime import datetime
import os

import instaloader
from pathlib import Path
import sqlalchemy as sa
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound

from sqlalchemy.orm import sessionmaker
from models import Story, StoryItem

load_dotenv()
engine = create_engine(os.environ.get("PG_DATABASE_URL"))
connection = engine.connect()
Base = declarative_base()
sa.orm.configure_mappers()
L = instaloader.Instaloader()
L.load_session_from_file("andriyorehov")

Base.metadata.create_all(connection)

Session = sessionmaker(bind=engine)
session = Session()


def download_user_story(username):
    profile = instaloader.Profile.from_username(L.context, username)
    for story in L.get_stories(userids=[profile.userid]):
        for item in story.get_items():
            folder_name = item.date_local.strftime("%Y-%m-%d")
            preview_file_name = item.date_utc.strftime("%Y-%m-%d_%H-%M-%S_UTC.jpg")
            preview_src = 'http://localhost:3000/stories/{}/{}/{}'.format(item.owner_username, folder_name,
                                                                          preview_file_name)
            if item.is_video:
                story_type = 'video'
                length = 0
                file_name = item.date_utc.strftime("%Y-%m-%d_%H-%M-%S_UTC.mp4")
                src = 'http://localhost:3000/stories/{}/{}/{}'.format(item.owner_username, folder_name, file_name)
            else:
                story_type = 'photo'
                length = 3
                file_name = item.date_utc.strftime("%Y-%m-%d_%H-%M-%S_UTC.jpg")
                src = 'http://localhost:3000/stories/{}/{}/{}'.format(item.owner_username, folder_name, file_name)

            try:
                story = session.query(Story).filter(
                    Story.username == item.owner_profile.username,
                    Story.time == datetime.date(item.date_local)).one()
            except NoResultFound:
                story = Story(item.owner_profile.username, datetime.date(item.date_local))
                session.add(story)
                session.commit()

            story_item = StoryItem(item.owner_id, item.owner_profile.profile_pic_url,
                                   item.owner_profile.username, item.mediaid, story.id, story_type,
                                   length, src, preview_src, '', '', item.date_local, False)
            session.add(story_item)
            session.commit()
            L.download_storyitem(item, Path('stories/{}/{}'.format(item.owner_username, folder_name)))


if __name__ == '__main__':
    download_user_story('shldk')
