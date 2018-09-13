# redis-async
A simple redis async wrapper for python3

[![PYPI Version][pypi-image]][pypi-url]
[![Build Status][travis-image]][travis-url]


## NOTE:
Not all redis command are covered yet. Please use it after release `0.1.0`.

## Setup & Install

#### Via pip

```
pip install redis_async
```

#### From source

```
python setup.py build && python setup.py install
```


### Example

```
from redis_async import RedisHash, Redis


# Initialize redis store
Redis.initialize(url='redis://redis:port', prefix='application')

class Store:
  # actual redis key will be like: "application:user:1"
  User = RedisHash(tpl="user:{id}")

def process_user(id):
  # preprocess code ...
  user = Store.User.hgetall(id)
  # process user block
  # ...

async def process_user_async(id):
  # preprocess code ...
  user = await Store.User.hgetallAsync(id)
  # process user block
  # ...

```

[pypi-image]: https://img.shields.io/pypi/v/redis-async.svg
[pypi-url]: https://pypi.org/project/redis-async/
[travis-image]: https://img.shields.io/travis/devfans/redis-async/master.svg
[travis-url]: https://travis-ci.org/devfans/redis-async
