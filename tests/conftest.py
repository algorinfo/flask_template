import os

import pickle
import pytest
from changeme.db.sql import SQL
from changeme import conf, create_app
from sqlalchemy import MetaData, create_engine

cfg = conf.Config()


def delete_tables():
    engine = create_engine(cfg.SQL)
    meta = MetaData(bind=engine)
    meta.reflect()
    # meta.create_all(conn)
    with engine.connect() as conn:
        for t in reversed(meta.sorted_tables):
            print(t)
            # conn.execute(t.delete())


@pytest.fixture
def clean_db():
    _db = SQL(sqluri=cfg.SQL)
    _db.drop_all()
    _db.create_db()

    return _db


@pytest.fixture(scope="function")
def db():
    # Create the database and the database table
    # sqldb.setup_connection('sqlite:///tests/test.db')
    sqldb = SQL(sqluri=cfg.SQL)
    session = sqldb.get_session()

    yield session
    session.close()


@pytest.fixture
def flaskclient():
    """ Flask http test client
    """
    app = create_app()

    with app.test_client() as client:
        # with app.app_context():
        #    init_db()
        yield client




    
# If you need to test async code
# @pytest.mark.asyncio
# @pytest.fixture(scope='function')
# async def volume():
#    vs = VolumeStore([_VOLUME])
#    yield vs
#    await vs.close()



# Redis and aioredis
# @pytest.mark.asyncio
# @pytest.fixture(scope='function')
# async def aredis():
#     redis = await aioredis.create_redis(f'redis://{_REDIS}')
#     await redis.flushdb()
#     yield redis
# 
#     redis.close()
#     await redis.wait_closed()
# 
# 
# @pytest.fixture(scope='function')
# def redis():
#     rh = _REDIS.split(":")[0]
#     rp = _REDIS.split(":")[1]
# 
#     r = Redis(host=rh, port=rp)
#     r.flushdb()
#     yield r
#     r.close()
