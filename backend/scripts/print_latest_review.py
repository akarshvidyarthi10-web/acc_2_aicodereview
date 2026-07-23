import os
import sys
import asyncio
import json

# Ensure backend folder is on sys.path so imports like `services` resolve
HERE = os.path.dirname(__file__)
BACKEND_DIR = os.path.abspath(os.path.join(HERE, '..'))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from services.db_service import db


async def latest():
    docs = await db.reviews.find().sort('created_at', -1).to_list(1)
    print(json.dumps(docs, indent=2, default=str))


if __name__ == '__main__':
    asyncio.run(latest())
