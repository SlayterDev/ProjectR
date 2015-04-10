from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('username', String(length=64)),
    Column('password', String(length=154)),
    Column('email', String(length=120)),
    Column('landlord_id', Integer),
    Column('unit', String(length=10)),
)

landlord = Table('landlord', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('email', VARCHAR(length=120)),
    Column('password', VARCHAR(length=154)),
    Column('property_name', VARCHAR(length=140)),
    Column('stripe_id', VARCHAR(length=140)),
    Column('stripe_key', VARCHAR(length=140)),
    Column('unit', VARCHAR(length=10)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user'].columns['unit'].create()
    pre_meta.tables['landlord'].columns['unit'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user'].columns['unit'].drop()
    pre_meta.tables['landlord'].columns['unit'].create()
