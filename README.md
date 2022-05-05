# GameHub

## Running

Getting your own instance of GameHub running is pretty simple.

Make sure you have a MongoDB server running! If your mongo server is on a different host/port, you can include the `MONGO_PORT` or `MONGO_HOST` environment variables.

**Node V16+ and Python 3.8+ are required.**

```
$ git clone https://github.com/ZeroIntensity/gamehub && cd gamehub
$ yarn install && yarn build
$ python3 -m pip install -r requirements.txt
$ python3 main.py
```

## Why is this using MongoDB and not a relational database?

Ease of use. I have yet to find a good library for ORM/DRM in Python, and Mongo is much easier to make one for.

Now, please do not make an issue saying something like "oh, just use [insert sql library]". These libraries are huge and have APIs that are awful to work with.
