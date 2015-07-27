class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'secrect'
    import os
    basedir = os.path.abspath(os.path.dirname(__file__))
    
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    #print 'sqlite started at ',SQLALCHEMY_DATABASE_URI
    #SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    #print 'sql migrate repo is at ',SQLALCHEMY_MIGRATE_REPO

class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
