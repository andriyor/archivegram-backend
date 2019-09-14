import json
import codecs
import datetime
import os.path

from cachier import cachier
from instagram_private_api import Client, ClientCookieExpiredError, ClientLoginRequiredError


def to_json(python_object):
    if isinstance(python_object, bytes):
        return {'__class__': 'bytes',
                '__value__': codecs.encode(python_object, 'base64').decode()}
    raise TypeError(repr(python_object) + ' is not JSON serializable')


def from_json(json_object):
    if '__class__' in json_object and json_object['__class__'] == 'bytes':
        return codecs.decode(json_object['__value__'].encode(), 'base64')
    return json_object


def onlogin_callback(api, new_settings_file):
    cache_settings = api.settings
    with open(new_settings_file, 'w') as outfile:
        json.dump(cache_settings, outfile, default=to_json)
        print('SAVED: {0!s}'.format(new_settings_file))


api = None

try:
    settings_file = "instagramsettings"
    username, password = os.environ.get("INSTAGRAM_USERNAME"), os.environ.get("INSTAGRAM_PASSWORD")
    if not os.path.isfile(settings_file):
        # settings file does not exist
        print('Unable to find file: {0!s}'.format(settings_file))

        # login new
        api = Client(username, password,
                     on_login=lambda x: onlogin_callback(x, settings_file))
    else:
        with open(settings_file) as file_data:
            cached_settings = json.load(file_data, object_hook=from_json)
        print('Reusing settings: {0!s}'.format(settings_file))

        device_id = cached_settings.get('device_id')
        # reuse auth settings
        api = Client(username, "lH3q7fXA3AVp", settings=cached_settings)

except (ClientCookieExpiredError, ClientLoginRequiredError) as e:
    print('ClientCookieExpiredError/ClientLoginRequiredError: {0!s}'.format(e))

    # Login expired
    # Do relogin but use default ua, keys and such
    api = Client(username, password, device_id=device_id,
                 on_login=lambda x: onlogin_callback(x, settings_file))


@cachier(stale_after=datetime.timedelta(weeks=3))
def search_instagram_users(login):
    return api.search_users(login)
