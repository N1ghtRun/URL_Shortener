import os

from aiopg.sa import create_engine
import sqlalchemy as sa

metadata = sa.MetaData()
tbl = sa.Table('links', metadata,
               sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
               sa.Column('new_link', sa.String(255)),
               sa.Column('old_link', sa.String(255)),
               sa.Column('user', sa.String(255)),
               )


async def init_pg():
    engine = await create_engine(user='postgres',
                                 database='postgres',
                                 host=os.getenv('POSTGRES_HOST', '127.0.0.1'),
                                 password='postgres',
                                 port=5432)

    return engine


async def insert_data(old_url, new_url, user_id=None):
    engine = await init_pg()
    async with engine.acquire() as conn:
        await conn.execute(tbl.insert().values(old_link=old_url, new_link=new_url, user=user_id))


async def get_link(new_url):
    engine = await init_pg()
    async with engine.acquire() as conn:
        result = await conn.execute(tbl.select().where(tbl.c.new_link == new_url))
        result = await result.fetchone()

    return result[2]


async def get_user_links(user_id):
    engine = await init_pg()
    async with engine.acquire() as conn:
        links_data = await conn.execute(tbl.select().where(tbl.c.user == user_id))
        links_data = await links_data.fetchall()
        links = [f'{link[2]} -> http://127.0.0.1:8080/{link[1]}' for link in links_data]

    return links
