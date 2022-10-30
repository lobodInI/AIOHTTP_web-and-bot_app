import os
import motor.motor_asyncio


async def setup_db():
    username = os.environ.get('DB_USERNAME')
    password = os.environ.get('DB_PASSWORD')
    host = os.environ.get('DB_HOST')
    port = os.environ.get('DB_PORT')
    client = motor.motor_asyncio.AsyncIOMotorClient(f"mongodb://{username}:{password}@{host}:{port}")
    db = client['async_db']
    return db


# async def do_insert(db, collection_name, document):
#     result = await db[collection_name].insert_one(document)
#     return result.inserted_id
#
#
# async def do_find_one(db, collection_name, query):
#     document = await db[collection_name].find_one(query)
#     return document
#
#
# async def do_find_many(db, collection_name, query):
#     documents = db[collection_name].find(query)
#     itms = []
#     async for one_itm in documents:
#         one_itm['_id'] = str(one_itm['_id'])
#         itms.append(one_itm)
#     return itms