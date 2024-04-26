import redis

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Test the connection
try:
    r.ping()
    print("Connected to Redis")
except redis.ConnectionError:
    print("Error: Failed to connect to Redis")
