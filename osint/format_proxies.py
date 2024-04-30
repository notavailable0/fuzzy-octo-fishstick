import re

proxy_strings = [
    '127.0.0.1:8000:username:password',
    'username:password@127.0.0.1:8000',
    'https://username:password@127.0.0.1:8000',
    'socks5://username:password@127.0.0.1:8000',
    'socks4://username:password@127.0.0.1:8000',
    'example.com:8080',
    '192.168.1.1:9000',
    'username:password@example.com:8080'
]

def reformat_proxy(proxy_str):
    prefixes = ("http://", "socks4://", "socks5://")

    proxy_str = proxy_str.replace("https://", "http://") # in case always using http://
    if proxy_str.startswith(prefixes):
        return proxy_str

    if "@" in proxy_str:
        return f"http://{proxy_str}"

    match = re.search(r'([\d.]+|[a-zA-Z0-9.-]+):(\d+)', proxy_str)
    if match:
        hostname, port = match.groups()
        hostname = f"{hostname}:{port}"

        if proxy_str.index(hostname) == 0:
            proxy_str = proxy_str.replace(f"{hostname}:", "").replace(f"{hostname}", "")
            return f"http://{proxy_str + '@' if proxy_str else ''}{hostname}"

    raise Exception("Invalid proxy format")