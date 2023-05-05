import os
import random
import string

from aiohttp import web

import jinja2
import aiohttp_jinja2

import asyncio
import sys

from db_utils import insert_data, get_link


async def home(request):
    response = aiohttp_jinja2.render_template("index.html", request, context=None)

    return response


async def create_short_url(request):
    data = await request.post()
    old_url = data['old_url']

    letters_and_digits = string.ascii_lowercase + string.digits
    new_url = ''.join(random.choice(letters_and_digits) for _ in range(6))

    await insert_data(old_url, new_url)

    return web.Response(text=new_url)


async def redirect_handler(request):
    new_url = request.match_info['new_url']
    long_url = await get_link(new_url)
    if long_url is None:
        raise web.HTTPNotFound(text=f'No such url {new_url}')
    print(long_url)
    raise web.HTTPFound(long_url)


app = web.Application()
aiohttp_jinja2.setup(
    app, loader=jinja2.FileSystemLoader(os.path.join(os.getcwd(), "templates"))
)
app.add_routes([web.get('/', home)])
app.add_routes([web.post('/', create_short_url)])
app.add_routes([web.get('/{new_url}', redirect_handler)])

if sys.version_info >= (3, 8) and sys.platform.lower().startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

web.run_app(app)
