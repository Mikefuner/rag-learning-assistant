import json
import redis

memory = redis.Redis(host='localhost', port=6379, decode_responses=True)

key = "chat:memory"

def add_message(role: str, content: str) -> None:
    message = {"role": role, "content": content}
    memory.rpush(key, json.dumps(message))
    memory.ltrim(key, -20, -1)

def get_messages() -> list[dict[str, str]]:
    messages = [json.loads(message) for message in memory.lrange(key, 0, -1)]
    return messages