from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
landlord = Table('landlord', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('email', String(length=120)),
    Column('password', String(length=154)),
    Column('property_name', String(length=140)),
    Column('stripe_id', String(length=140)),
    Column('stripe_key', String(length=140)),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('username', String(length=64)),
    Column('password', String(length=154)),
    Column('email', String(length=120)),
    Column('landlord_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['landlord'].create()
    post_meta.tables['user'].columns['landlord_id'].create()
    post_meta.tables['user'].columns['password'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['landlord'].drop()
    post_meta.tables['user'].columns['landlord_id'].drop()
    post_meta.tables['user'].columns['password'].drop()
