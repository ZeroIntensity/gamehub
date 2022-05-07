# GameHub

## Unblocked Games Website

### Contribution

There isn't a development documentation, so if you have any questions about how GameHub works feel free to create an issue.

#### Tech Stack

| Stack           | Technology                                                            |
| --------------- | --------------------------------------------------------------------- |
| Backend         | [FastAPI](https://fastapi.tiangolo.com)                               |
| Frontend        | [TypeScript](https://www.typescriptlang.org/)                         |
| CSS             | [Tailwind](https://tailwindcss.com)                                   |
| Template Engine | [Jinja2](https://pypi.org/project/Jinja2)                             |
| Build           | [PostCSS](https://postcss.org/) and [Webpack](https://webpack.js.org) |

### Running

**Node V16+ and Python 3.8+ are required.**

```
$ git clone https://github.com/ZeroIntensity/gamehub && cd gamehub
$ yarn install && yarn build
$ python3 -m pip install -r requirements.txt
$ python3 main.py
```

Everything in `src/config.py` can be changed by supplying an environment variable.

#### Basic .env file

```
APPLY_WEBHOOK=https://discord.com/api/webhooks/...
REPORT_WEBHOOK=https://discord.com/api/webhooks/...
SUGGEST_WEBHOOK=https://discord.com/api/webhooks/...
JWT_ALGORITHM=HS256
JWT_SECRET=mysecret
```

### Why is this using MongoDB and not a relational database?

Ease of use. I have yet to find a good library for ORM/DRM in Python, and Mongo is much easier to make one for.

Now, please do not make an issue saying something like "oh, just use [insert sql library]". These libraries are huge and have APIs that are awful to work with.
