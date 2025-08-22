# Complete Observability Stack (Prometheus + Loki/Promtail + Jaeger + Grafana)

## Prereqs
- Docker 24+ and Docker Compose v2
- Open ports: 3000 (Grafana), 9090 (Prometheus), 3100 (Loki), 16686 (Jaeger), 5000 (App)

## One-time setup
```bash
git clone <your-repo> observability-stack
cd observability-stack
cp .env .env.local || true
# edit .env if needed
```

## Start the stack
```bash
docker compose --env-file .env up -d --build
docker compose ps
```

## Verify services
- App: http://localhost:5000/healthz
- Metrics: http://localhost:5000/metrics
- Prometheus: http://localhost:9090
- Loki (API): http://localhost:3100/ready
- Jaeger UI: http://localhost:16686
- Grafana: http://localhost:3000 (user/pass from .env)

## Generate traffic
```bash
# Warm-up
for i in {1..20}; do curl -s http://localhost:5000/work > /dev/null; done
# Load + errors
for i in {1..200}; do curl -s "http://localhost:5000/work?fail=true" > /dev/null; done
```

## Grafana dashboards
Grafana auto-provisions:
- Datasources: Prometheus, Loki, Jaeger
- Dashboard: Observability/App: *App: Full Observability*

## Production tips
- Change credentials in `.env`
- Mount persistent volumes (already configured) and place on durable storage on cloud VMs
- Lock down Grafana/Prometheus with reverse proxy + TLS (Nginx/Caddy/Cloud LB)
- Use Jaeger with dedicated storage in real prod; all-in-one is for non-critical envs
- Run docker compose as a systemd service or migrate to Swarm/K8s for HA
- Enable Prometheus alerting/Alertmanager and Loki ruler

## Stop & cleanup
```bash
docker compose down
# remove volumes
docker volume rm $(docker volume ls -q | grep obs_ || true)
```
