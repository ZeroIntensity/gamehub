# GameHub

## Running

Getting your own instance of GameHub running is pretty simple.

Make sure you have a MongoDB server running! If your mongo server is on a different host/port, you can include the `MONGO_PORT` or `MONGO_HOST` environment variables.

**Node V11+ and Python 3.8+ are required.**

```
$ git clone https://github.com/gamehub-2/gamehub && cd gamehub
$ yarn install && yarn build
$ python3 -m pip install -r requirements.txt
$ python3 main.py
```
