# from PIL import Image

# im = Image.open('app/test.png')

# print(im.format)
# print(im.size)
# print(im.mode)
# print(im.filename)
# print(im.getcolors) 

# print(im.show())

# im.save('test.jpeg')  

# output = im.resize((250, 250))
# output.save('app/output.jpg')

# import redis  

# r = redis.Redis(host='localhost', port=6379, db=0)

# # print(r.ping())

# # r.set("name", "Digi9 Reach")
# # print(r.get("name").decode())

# r.delete("counters")
# r.set("counter", 5)
# r.incr("counters")
# r.incr("counters")
# print(r.get("counters").decode())

from fastapi import FastAPI
import redis
import time

app = FastAPI()

r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

def fetch_weather(city: str) -> dict:
    time.sleep(2)
    return {
        "city": city,
        "temperature": 25,
        "condition": "Sunny"
    }

@app.get("/weather/{city}")
def get_weather(city: str):
    cache_key = f"weather:{city}"

    if r.exists(cache_key):
        data = r.hgetall(cache_key)
        data["source"] = "redis-cache"
        return data

    data = fetch_weather(city)

    r.hset(cache_key, mapping=data)
    r.expire(cache_key, 30)

    data["source"] = "api-call"
    return data
