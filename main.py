import os
import json
import random
import string

from aiohttp import web

import jinja2
import aiohttp_jinja2


app = web.Application()
aiohttp_jinja2.setup(
    app, loader=jinja2.FileSystemLoader(os.path.join(os.getcwd(), "templates"))
)


async def home(request):
    response = aiohttp_jinja2.render_template("index.html", request, context=None)

    return response


async def create_short_url(request):
    data = await request.post()
    old_url = data['old_url']

    letters_and_digits = string.ascii_lowercase + string.digits
    new_url = ''.join(random.choice(letters_and_digits) for _ in range(6))

    if os.stat("urls.json").st_size != 0:
        with open('urls.json', 'r') as f:
            data = json.load(f)
    else:
        data = dict()

    data[new_url] = old_url

    with open('urls.json', 'w') as f:
        json.dump(data, f)

    return web.Response(text=new_url)


async def redirect_handler(request):
    new_url = request.match_info['new_url']
    with open('urls.json') as f:
        file_data = json.loads(f.read())
    long_url = file_data.get(new_url)
    if long_url is None:
        raise web.HTTPNotFound(text=f'No such url {new_url}')
    raise web.HTTPFound(long_url)


app.add_routes([web.get('/', home)])
app.add_routes([web.post('/', create_short_url)])
app.add_routes([web.get('/{new_url}', redirect_handler)])

web.run_app(app)
