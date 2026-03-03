import requests
import time
from datetime import datetime, timezone

EUROPE_URL = "http://35.205.114.61:8080"
US_URL = "http://34.136.97.138:8080"

### testing 

def run_10_calls(endpoint: str):
    us_times = []
    eu_times = []

    for i in range(10):

        if endpoint == "register":

            payload = {
            "username": f"user{i}",
            "createdAt": datetime.now(timezone.utc).isoformat()
            }

            start_time = time.perf_counter()
            requests.post(f"{US_URL}/{endpoint}", json=payload)
            end_time = time.perf_counter()

            us_times.append(end_time - start_time)

            start_time = time.perf_counter()
            requests.post(f"{EUROPE_URL}/{endpoint}", json=payload)
            end_time = time.perf_counter()

            eu_times.append(end_time - start_time)
        elif endpoint == "list":

            start_time = time.perf_counter()
            requests.get(f"{US_URL}/{endpoint}")
            end_time = time.perf_counter()

            us_times.append(end_time - start_time)

            start_time = time.perf_counter()
            requests.get(f"{EUROPE_URL}/{endpoint}")
            end_time = time.perf_counter()

            eu_times.append(end_time - start_time)

    average_latency_us = sum(us_times) / 10
    average_latency_eu = sum(eu_times) / 10

    return [average_latency_us, average_latency_eu]

def eventual_consistency_test():
    
    requests.get(f"{US_URL}/clear")

    num_not_found = 0

    session = requests.Session()
    
    for i in range(100):
        payload = {"username": f"user{i}", "createdAt": datetime.now(timezone.utc).isoformat()}
          
        session.post(f"{US_URL}/register", json=payload)

        response = session.get(f"{EUROPE_URL}/list")

        if f"user{i}" not in response.text:
            num_not_found += 1

    print(f"number of users not found: {num_not_found}")


print(f"register: {run_10_calls('register')}")
print(f"list: {run_10_calls('list')}")

eventual_consistency_test()

    
