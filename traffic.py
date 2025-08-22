import requests, random, time

url = "http://localhost:5000/work"

for i in range(500):
    fail = random.choice([False, False, True])  # ~33% failures
    try:
        r = requests.get(url, params={"fail": fail})
        print(f"{i}: {r.status_code}")
    except Exception as e:
        print(f"{i}: Error - {e}")
    time.sleep(random.uniform(0.05, 0.2))
