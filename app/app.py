import os, time, random
from fastapi import FastAPI, Request, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import structlog

# Logging setup (JSON to stdout)
structlog.configure(processors=[
    structlog.processors.add_log_level,
    structlog.processors.TimeStamper(fmt="iso"),
    structlog.processors.JSONRenderer()
])
log = structlog.get_logger(service=os.getenv("OTEL_SERVICE_NAME","sample-app"))

# Metrics
REQ_COUNTER = Counter("http_requests_total", "Total HTTP requests", ["method","path","status"])
REQ_LATENCY = Histogram("http_request_duration_seconds", "Request latency", buckets=[0.005,0.01,0.025,0.05,0.1,0.25,0.5,1,2,5])

# Tracing via OpenTelemetry
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

trace.set_tracer_provider(TracerProvider())
span_exporter = OTLPSpanExporter(endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT","http://jaeger:4318") + "/v1/traces")
span_processor = BatchSpanProcessor(span_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

app = FastAPI(title="Sample Observability App")

FastAPIInstrumentor.instrument_app(app)
RequestsInstrumentor().instrument()

@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/work")
def do_work(request: Request, fail: bool = False):
    start = time.time()
    with trace.get_tracer(__name__).start_as_current_span("work-span") as span:
        # simulate variable latency
        delay = random.uniform(0.01, 0.5)
        time.sleep(delay)

        status = 200
        if fail and random.random() < 0.3:
            status = 500

        # record metrics
        REQ_LATENCY.observe(time.time() - start)
        REQ_COUNTER.labels(method="GET", path="/work", status=str(status)).inc()

        # log with trace correlation
        current_span = trace.get_current_span()
        span_ctx = current_span.get_span_context()
        trace_id = format(span_ctx.trace_id, "032x")
        log.info("handled_work",
                 path="/work",
                 method="GET",
                 level="info",
                 trace_id=trace_id,
                 duration_ms=int((time.time()-start)*1000),
                 status=status)
        if status != 200:
            return Response(status_code=status, content="error")
        return {"ok": True, "delay": delay}
