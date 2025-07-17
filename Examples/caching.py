import PyVutils as vu

from diskcache import Cache
cache = Cache('./cache')
cache.clear()

def custom_cache_key(url):
    from cachetools.keys import hashkey
    from urllib.parse import urlparse
    domain = urlparse(url).netloc
    return hashkey(domain)

@vu.custom_cached(custom_cache_key, lambda k: cache.get(k), lambda k, v: cache.set(k, v))
def check_url(url: str) -> bool:
    result = url.startswith("https://")
    print(f"Checking URL: {url} => {result}")
    return result

print("Số lượng items trong cache:", len(cache))
print("Các key trong cache:", list(cache.iterkeys()))
print()

check_url("https://abc.com/page1")  # Lấy từ cache, không in ra gì
check_url("https://abc.com/page2")  # Lấy từ cache, không in ra gì
check_url("https://xyz.com")        # In ra "Checking URL: ...", domain khác

print()
print("Số lượng items trong cache:", len(cache))
print("Các key trong cache:", list(cache.iterkeys()))

cache.close()