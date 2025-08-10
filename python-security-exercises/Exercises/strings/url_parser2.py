from urllib.parse import urlparse, parse_qs
from  datetime import datetime


def parse_url(url):

    scan_time = datetime.now()

    parsed = urlparse(url)
    return {
        "protocol": parsed.scheme,
        "domain": parsed.netloc,
        "path": parsed.path,
        "query_params": parse_qs(parsed.query)
    }
    
# Example Usage
url = ""
print(parse_url(url))