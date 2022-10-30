import asyncio

from aiohttp import web
from db_ import setup_db
from bson.objectid import ObjectId


async def shut_user_url_get(request):
    url_form_request = """<html lang="en-us">
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
    result = await request.text()
    user_url = result.replace('user_url=', '').replace("%2F", "/")
    #user_url = user_url.replace("%2F", "/")
    database = request.app["db"]
    collection = database['shortener']
    url_record = await collection.insert_one({'user_url': user_url})
    return web.Response(text=str(url_record.inserted_id))


async def show_user_url(request):
    name_url = request.match_info.get('name_url')
    database = request.app["db"]
    collection = database['shortener']
    obj_url = await collection.find_one({"_id": ObjectId(name_url)})
    return web.HTTPFound('https://' + obj_url['user_url'])


db = asyncio.run(setup_db())

app = web.Application()
app.add_routes([web.get('/', shut_user_url_get),
                web.get('/{name_url}', show_user_url),
                web.post('/', shut_user_url_post)])
app["db"] = db

if __name__ == '__main__':
    web.run_app(app)
