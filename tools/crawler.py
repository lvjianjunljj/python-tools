import urllib.request

import urllib.error


def crawl(url, encoding='utf-8'):
    if url.endswith('.') and not url.endswith('..'):
        url = url[0:url.__len__() - 1]
    try:
        response = urllib.request.urlopen(url)
        result = response.read().decode(encoding)
        return result
    except urllib.error.HTTPError:
        return ''
    except TimeoutError:
        return ''
    except urllib.error.URLError:
        return ''
    except UnicodeDecodeError:
        return ''
