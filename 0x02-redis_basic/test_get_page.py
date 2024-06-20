from web import get_page
import redis

# Initialize Redis client
redis_client = redis.Redis()

# Clear Redis for clean testing
redis_client.flushall()

url = "http://slowwly.robertomurray.co.uk/delay/1000/url/http://www.example.com"

# Test the function
print("First call to get_page:")
page_content_1 = get_page(url)  # Should fetch from the web
print(page_content_1)

print("Second call to get_page:")
page_content_2 = get_page(url)  # Should fetch from the cache
print(page_content_2)

# Check the count
count = redis_client.get(f'count:{url}')
print(f"Access count: {int(count)}")  # Should be 2

# Validate content
assert page_content_1 == page_content_2, "Cached content does not match fetched content"
assert int(count) == 2, f"Expected access count to be 2, got {int(count)}"

print("Test passed.")

