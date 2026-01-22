import redis
from config import REDIS_HOST, REDIS_PORT, REDIS_DB, SUM_KEY

_pool = redis.ConnectionPool(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    decode_responses=True,
    max_connections=50
)

def get_redis():
    return redis.Redis(connection_pool=_pool)

def add_to_sum(value):
    r = get_redis()
    # incrbyfloat is atomic in redis so we dont need locking
    res = r.incrbyfloat(SUM_KEY, value)
    return float(res)

def get_sum():
    r = get_redis()
    val = r.get(SUM_KEY)
    if val is None:
        return 0.0
    return float(val)

def reset_sum():
    get_redis().set(SUM_KEY, 0)
