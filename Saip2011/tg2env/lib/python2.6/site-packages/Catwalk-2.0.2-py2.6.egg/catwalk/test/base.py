import os
from sqlalchemy import *
from sqlalchemy.orm import *
from model import *
from cStringIO import StringIO
from cgi import FieldStorage

session = None
engine = None
connect = None

sorted_user_columns = ['_password', 'created', 'display_name', 'email_address',
                       'groups', 'password', 'sprox_id', 'town',
                       'town_id', 'user_id', 'user_name']

database_setup=False
def setup_database():
    global session, engine, database_setup, connect, metadata

    #singletonizes things
    if not database_setup:
        engine = create_engine(os.environ.get('DBURL', 'sqlite://'), strategy="threadlocal")
        connect = engine.connect()
    #    print 'testing on', engine
        metadata.bind = engine
        metadata.drop_all()
        metadata.create_all()

        Session = sessionmaker(bind=engine, autoflush=True, autocommit=False)
        session = Session()
        database_setup = True
    return session, engine, metadata

records_setup = None
def setup_records(session):


    #session.expunge_all()

    user = User()
    user.user_name = u'asdf'
    user.email_address = u"asdf@asdf.com"
    user.password = u"asdf"
    session.add(user)

    arvada = Town(name=u'Arvada')
    session.add(arvada)
    session.flush()
    user.town = arvada

    session.add(Town(name=u'Denver'))
    session.add(Town(name=u'Golden'))
    session.add(Town(name=u'Boulder'))

    #test_table.insert(values=dict(BLOB=FieldStorage('asdf', StringIO()).value)).execute()
    #user_reference_table.insert(values=dict(user_id=user.user_id)).execute()

#    print user.user_id
    for i in range (5):
        group = Group(group_name=unicode(i))
        session.add(group)

    user.groups.append(group)

    session.flush()
    return user

def teardown_database():
    pass
    #metadata.drop_all()

