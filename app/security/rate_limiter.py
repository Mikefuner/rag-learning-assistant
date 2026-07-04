import redis

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

class RateLimiter:

    LIMIT = 30
    WINDOW = 60

    def allow(self, api_key: str) -> bool:
        key = f"rate:{api_key}"
        requests = redis_client.incr(key)

        if requests == 1:
            redis_client.expire(key, self.WINDOW)

        return requests <= self.LIMIT