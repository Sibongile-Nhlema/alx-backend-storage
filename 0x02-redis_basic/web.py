#!/usr/bin/env python3
'''
Module implements the get_page function.
'''
import requests
import redis
from functools import wraps


redis_client = redis.Redis()


def cache_page(expiration: int = 10):
    """
    Decorator to cache the page content and track the number of accesses.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(url: str) -> str:
            # Increment the access count for the URL
            redis_client.incr(f'count:{url}')

            # Check if the page content is already cached
            cached_page = redis_client.get(f'cached:{url}')
            if cached_page:
                return cached_page.decode('utf-8')

            # Call the original function to get the page content
            page_content = func(url)

            # Cache the page content with an expiration time
            redis_client.setex(f'cached:{url}', expiration, page_content)

            return page_content
        return wrapper
    return decorator


@cache_page(expiration=10)
def get_page(url: str) -> str:
    """
    Get the HTML content of a particular URL.
    """
    response = requests.get(url)
    return response.text

# Ensure the function is correctly annotated
get_page.__annotations__ = {'url': str, 'return': str}


# Example usage
if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.example.com"
    print(get_page(url))
    print(get_page(url))  # This should be fetched from the cache

