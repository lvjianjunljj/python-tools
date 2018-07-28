import urllib.request


def crawl(url, encoding='utf-8'):
    if url.endswith('.') and not url.endswith('..'):
        url = url[0:url.__len__() - 1]
    response = urllib.request.urlopen(url)
    result = response.read().decode(encoding)
    return result

