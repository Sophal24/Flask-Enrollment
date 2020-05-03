import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'\xb1\x16N\x01\x02}{@\x81\xc3G\xe2\xd4\x93\x18\xf1'

    MONGODB_SETTINGS = { 'db' : 'UTA_Enrollment' }

