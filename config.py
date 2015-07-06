SECRET_KEY = 'secrect'
import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
print 'sqlite started at ',SQLALCHEMY_DATABASE_URI
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
print 'sql migrate repo is at ',SQLALCHEMY_MIGRATE_REPO
