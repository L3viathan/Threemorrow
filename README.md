# Threemorrow

### Magic decorator syntax for asynchronous code in Python 3.6

### Please don't actually use this in production. It's more of a thought experiment
than anything else, and relies heavily on behavior specific to Python's old
style classes. Pull requests, issues, comments and suggestions welcome.

Threemorrow is a spiritual fork of
[Tomorrow](https://github.com/madisonmay/Tomorrow), which only worked in Python
2.7. I say spiritual, because it isn't an actual git fork, and the usage
differs slightly (at least for the moment).


## Usage

```python
import time
import requests

from threemorrow import threads

urls = [
    'http://google.com',
    'http://facebook.com',
    'http://youtube.com',
    'http://baidu.com',
    'http://yahoo.com',
]

@threads(5)
def download(url):
    return requests.get(url)

if __name__ == '__main__':
    for url in urls:
        download(url)

    for result, args, kwargs in download:
        print(args[0], "resulted in", result)
```
