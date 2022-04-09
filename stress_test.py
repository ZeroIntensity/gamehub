import rethread  # pip install -U rethread
import requests

URL: str = "http://localhost:5000"

@rethread.auto
def request_thread():
    while True:
        resp = requests.get(URL)

        if not resp.ok:
            print(f"request failure: {resp.text}")

@rethread.auto
def main():
    while True:
        request_thread()

if __name__ == '__main__':
    main()