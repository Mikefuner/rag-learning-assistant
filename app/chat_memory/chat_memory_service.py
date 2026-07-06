import json
import os
import redis
from dotenv import load_dotenv

load_dotenv()

redis_port = int(os.getenv("REDIS_PORT", "6379"))
memory = redis.Redis(host='localhost', port=redis_port, decode_responses=True)

key = "chat:memory"

def add_message(role: str, content: str) -> None:
    message = {"role": role, "content": content}
    memory.rpush(key, json.dumps(message))
    memory.ltrim(key, -20, -1)

def get_messages() -> list[dict[str, str]]:
    messages = [json.loads(message) for message in memory.lrange(key, 0, -1)]
    return messages