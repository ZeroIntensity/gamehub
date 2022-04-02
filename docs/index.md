# Welcome to the GameHub API documentation!

This is a [GraphQL](https://graphql.org/) API, and _everything_ has a docstring, so you won't need too much from this documentation.

## Authentication

All mutations require authentication, so how do we pass this in? This API uses HTTP Basic Authentication. Since all content in production is served over HTTPS, this is ok.

Don't know how basic authentication works? That's fine, it's really simple.

Take your username and password, and format it into a string like this: `username:password`. For example purposes, we will pretend that our name is `abc` with a password of `123`, so it should look like `abc:123`.

Now, we have to pass something to the `Authorization` header of our GraphQL POST request. First, encode the string above in base64. Then, simply pass it in to the header with a prefix of `Basic`, as so:

```
Authorization: Basic YWJjOjEyMw==
```

### Don't know how to encode in base64?

Base64 is extremely common, so theres a good chance the language you are using has a built in function for it somewhere, but heres how to do it Python and JavaScript:

#### Python

```py
from base64 import urlsafe_b64encode

def make_header(username: str, password: str) -> str:
    bytes_string: bytes = f'{username}:{password}'.encode()
    return f'Basic {urlsafe_b64encode(bytes_string).decode()}'

make_header("abc", "123") # Basic YWJjOjEyMw==
```

#### JavaScript

```js
function makeHeader(username, password) {
    encoded = btoa(`${username}:${password}`);
    return `Basic ${encoded}`;
}

makeHeader("abc", "123"); // Basic YWJjOjEyMw==
```
