from os import getenv

from aioredis import Redis

redis = Redis(host=getenv("REDIS_HOST"),
              port=int(getenv("REDIS_PORT")),
              db=getenv("REDIS_DB"),
              password=getenv("REDIS_PASSWORD"))
