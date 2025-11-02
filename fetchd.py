#!/usr/bin/env python3
import sys
import requests
from markitdown import MarkItDown
from io import BytesIO
from fake_useragent import UserAgent

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: fetchd <url>")
        sys.exit(1)

    url = sys.argv[1]
    ua = UserAgent()

    headers = {
        'User-Agent': ua.safari,
        'Accept': '*/*',
        'Accept-Language': '*',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    md = MarkItDown()
    result = md.convert_stream(BytesIO(response.content))
    print(result.text_content)
