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
    Column('stripe_refresh', String(length=140)),
    Column('stripe_access', String(length=140)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['landlord'].columns['stripe_access'].create()
    post_meta.tables['landlord'].columns['stripe_refresh'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['landlord'].columns['stripe_access'].drop()
    post_meta.tables['landlord'].columns['stripe_refresh'].drop()
