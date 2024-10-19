import os
import redis


def setup_redis():
    # Read Redis URL from environment variable
    redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379')

    # Initialize Redis client
    r = redis.from_url(redis_url)

    try:
        # Ping Redis to check connection
        r.ping()
        print("Successfully connected to Redis.")

        # Optionally, you can set a key to further verify the connection
        r.set('test_key', 'test_value')
        value = r.get('test_key')
        if value == b'test_value':
            print("Redis is working correctly.")
        else:
            print("Redis set/get test failed.")

        # Clean up the test key
        r.delete('test_key')

    except redis.ConnectionError:
        print("Failed to connect to Redis. Please check your Redis URL and ensure Redis is running.")


if __name__ == "__main__":
    setup_redis()