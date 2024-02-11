import time
import requests

TIME_BETWEEN_REQUESTS = 0.01
PORT = 30612
URL = f"http://localhost:{PORT}"

i = 0
while True:
    requests.get(URL)
    print(f"Sent request {i}")
    time.sleep(TIME_BETWEEN_REQUESTS)
    i += 1