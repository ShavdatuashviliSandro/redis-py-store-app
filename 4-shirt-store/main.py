import redis

r = redis.Redis()


def scan_keys(pattern, pos: int = 0) -> list:
    shirts = []
    while True:
        pos, val = r.scan(cursor=pos, match=pattern)
        shirts = shirts + val
        if pos == 0:
            break
    return shirts

def buy_items():


shirts = scan_keys("shirt:*")
print(shirts)
