from redis import Redis
redis = Redis(host='localhost', port=6379)

redis['a'] = 'Hello'
print(redis['a'])