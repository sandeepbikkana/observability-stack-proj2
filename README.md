=======================================================
Complete Observability System (Metrics, Logs & Traces)
======================================================
Project Overview

Objective: Build a fully integrated monitoring system that includes:

Metrics → Prometheus

Centralized Logs → Loki + Promtail

Request Tracing → Jaeger

Visualization → Grafana

Tools: Prometheus, Grafana, Loki, Jaeger, Docker Compose, Python (FastAPI)

Key Deliverables:

docker-compose.yml

Grafana Dashboards JSON

Log samples

Trace visualizations

Report / insights
========
1️⃣ Project Architecture
           ┌────────────┐
           │  FastAPI   │
           │   App      │
           └────────────┘
                 │
        ┌────────┼────────┐
        │        │        │
   /metrics   Logs   Traces
     │        │        │
Prometheus  Promtail → Loki   Jaeger
                 │
             Grafana Dashboards 

App → Prometheus: metrics via /metrics

App → Promtail → Loki: structured logs

App → Jaeger: request traces

Grafana: unified visualization

2️⃣ Prerequisites

Ubuntu 22.04+ (VM or Cloud)

Docker & Docker Compose v2 installed

sudo apt update
sudo apt install docker.io docker-compose -y
sudo systemctl enable --now docker
docker --version
docker compose version


Optional: Python 3.11 for traffic generation

3️⃣ Project Structure
observability-stack/
│
├─ docker-compose.yml
├─ .env
│
├─ app/
│   ├─ Dockerfile
│   ├─ requirements.txt
│   └─ app.py
│
├─ prometheus/prometheus.yml
├─ loki/loki-config.yml
├─ promtail/promtail-config.yml
├─ grafana/provisioning/datasources/datasources.yml
├─ grafana/provisioning/dashboards/dashboards.yml
├─ grafana/dashboards/app-overview.json
└─ traffic.py

4️⃣ Step 1: Configure Environment Variables

Create a .env file:

GRAFANA_ADMIN_USER=admin
GRAFANA_ADMIN_PASSWORD=admin
PROMETHEUS_SCRAPE_INTERVAL=10s

5️⃣ Step 2: Build & Run Stack
docker compose up -d --build
docker compose ps


Ports:

App → 5000

Prometheus → 9090

Loki → 3100

Grafana → 3000

Jaeger → 16686

6️⃣ Step 3: Test Application

Health check:

curl http://localhost:5000/healthz


Metrics endpoint:

curl http://localhost:5000/metrics

7️⃣ Step 4: Generate Traffic
Option A: Python Script
# traffic.py
import requests, random, time

url = "http://localhost:5000/work"

for i in range(500):
    fail = random.choice([False, False, True])
    try:
        r = requests.get(url, params={"fail": fail})
        print(f"{i}: {r.status_code}")
    except Exception as e:
        print(f"{i}: Error - {e}")
    time.sleep(random.uniform(0.05, 0.2))

python traffic.py

Option B: curl Loop
for i in {1..50}; do curl -s http://localhost:5000/work > /dev/null; done

8️⃣ Step 5: Access Observability Tools

Grafana → http://localhost:3000
 (login with .env credentials)

Dashboards for Metrics, Logs, Traces

Prometheus → http://localhost:9090

Test queries (PromQL)

Loki → http://localhost:3100/ready

Search logs by trace_id or status

Jaeger → http://localhost:16686

Explore traces for requests

9️⃣ Step 6: Prometheus Queries to Test
Metric	PromQL
Total requests	sum(http_requests_total)
Requests per second	rate(http_requests_total[1m])
Error count (500s)	sum(rate(http_requests_total{http_status="500"}[1m]))
Error ratio	sum(rate(http_requests_total{http_status="500"}[1m])) / sum(rate(http_requests_total[1m]))
Avg latency	rate(http_request_latency_seconds_sum[1m]) / rate(http_request_latency_seconds_count[1m])
P95 latency	histogram_quantile(0.95, rate(http_request_latency_seconds_bucket[1m]))
Requests by endpoint	sum(rate(http_requests_total[1m])) by (endpoint)
10️⃣ Step 7: Observing Logs & Traces

Logs (Loki):

Structured JSON logs with trace_id

Filter by status=500 to find errors

Traces (Jaeger):

Explore request flow

Identify slow spans or bottlenecks

11️⃣ Step 8: Export Dashboards

Export Grafana dashboards to JSON → grafana/dashboards/app-overview.json

Include panels for:

Request rate

Error rate

Latency histogram

Live logs

Traces

12️⃣ Step 9: Collect Samples for Deliverables

Log samples → from Grafana Loki

Trace visualizations → screenshots from Jaeger

Metrics graphs → Grafana panels

13️⃣ Step 10: Report / Insights Observed

Example Observations:

Metrics:

Under load, p95 latency increases from 200ms → 450ms

Error rate spikes (~30%) when fail=true

Logs:

Structured logs with trace_id

Failed requests clearly identifiable by status=500

Traces:

Longest span corresponds to slow /work processing

Traces correlated with logs for troubleshooting

Lessons Learned:

Observability enables real-time monitoring and issue correlation

Metrics, logs, and traces together provide full visibility

Learned production-grade container orchestration and monitoring

14️⃣ 14️⃣ Step 11: Stopping the Stack
docker compose down -v


Removes containers and volumes for a fresh start
