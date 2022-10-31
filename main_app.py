import asyncio

from aiohttp import web
from db_ import setup_db
from bson.objectid import ObjectId
from urllib.parse import unquote


async def shut_user_url_get(request):
    url_form_request = """<html lang="en-us">
    <head>
     <meta charset="UTF-8">
       <link rel="icon" href="data:,">
       <title>URL Shortener</title>
    </head>
  <form action="/" method="POST">
    <div align="center" id="logo"><h1><a href="http://0.0.0.0:8080" class="logo">Short URL</a><h1>
    </div>
    <div  align="center">
     <label for="user_url"><h2>Paste the URL to be shortened<h2></label>
     <input 
     style="width: 400px; height: 50px;" 
     type="text" name="user_url" id="user_url" 
     placeholder="Enter the link here"/>
    </div>
    <div align="center">
     <button style="color: white;
     background-color: blue;">
     <h3>Shorten URL<h3>
    </button>
    </div>
  </form>
</html>"""
    return web.Response(text=url_form_request, content_type="text/html")


async def shut_user_url_post(request):
    database = request.app["db"]
    collection = database['shortener']

    result = await request.text()
    # user_url = result.replace('user_url=', '').replace("%2F", "/").replace("%3A", ":")
    user_url = unquote(result.replace('user_url=', ''))
    url_breakdown_list = user_url.split('://')
    user_url_record = await collection.insert_one({'prefix': url_breakdown_list[0],
                                                   'user_url': url_breakdown_list[1]})

    return web.Response(text=str(user_url_record.inserted_id))


async def show_user_link(request):
    database = request.app["db"]
    collection = database['shortener']

    name_url = request.match_info.get('name_url')
    try:
        obj_url = await collection.find_one({"_id": ObjectId(name_url)})
        prefix_user_url = str(obj_url.get('prefix'))
        user_url = str(obj_url.get('user_url'))
    except BaseException:
        return web.Response(text="Not found user url")

    return web.HTTPFound(prefix_user_url + '://' + user_url)


db = asyncio.run(setup_db())

app = web.Application()
app.add_routes([web.get('/', shut_user_url_get),
                web.get('/{name_url}', show_user_link),
                web.post('/', shut_user_url_post)])
app["db"] = db

if __name__ == '__main__':
    web.run_app(app)
