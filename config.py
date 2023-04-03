import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'A-VERY-LONG-SECRET_KEY'
    RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY') or 'A-VERY-LONG-RECAPTCHA_PUBLIC_KEY'
    RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY') or 'A-VERY-LONG-RECAPTCHA_PRIVATE_KEY'

    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost:3306/mydatabase'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.qq.com'
    MAIL_POST = 465
    MAIL_USE_SSL = False
    MAIL_USE_TLS = True
    MAIL_USERNAME = '@qq.com'
    MAIL_PASSWORD = ''