import time

import redis
import logging

r = redis.Redis()
logging.basicConfig()


class OutOfStockError(Exception):
    """Raised when item is out of stock"""


def scan_keys(pattern, pos: int = 0) -> list:
    shirts = []
    while True:
        pos, val = r.scan(cursor=pos, match=pattern)
        shirts = shirts + val
        if pos == 0:
            break
    return shirts


def buy_items(r: redis.Redis, itemid) -> None:
    pipe = r.pipeline()

    while True:
        try:
            pipe.watch(itemid)
            nleft: bytes = r.hget(itemid, "quantity")
            if nleft > b"0":
                pipe.multi()
                time.sleep(5.4)
                pipe.hincrby(itemid, "quantity", -1)
                pipe.hincrby(itemid, "npurchased", +1)
                pipe.execute()
                break
            else:
                pipe.unwatch()
                raise OutOfStockError(
                    f"Sorry {itemid} is out of stock"
                )
        except redis.WatchError:
            logging.warning('Error in watch, retrying')

    return None

shirts = scan_keys("shirt:*")
print(shirts)
buy_items(r, shirts[0])
