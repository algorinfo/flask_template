import os
from prometheus_flask_exporter.multiprocess import GunicornPrometheusMetrics

# https://docs.gunicorn.org/en/stable/settings.html
accesslog="-" 
errorlog="-" 
timeout=os.getenv("TIMEOUT", "60")
bind = os.getenv("CHANGEME_LISTEN", "127.0.0.1:8000")
prom_port = os.getenv("PROM_PORT", "8001")

def when_ready(server):
    GunicornPrometheusMetrics.start_http_server_when_ready(int(prom_port))


def child_exit(server, worker):
    GunicornPrometheusMetrics.mark_process_dead_on_child_exit(worker.pid)

# def worker_exit(server, worker):
#    from prometheus_client import multiprocess
#    multiprocess.mark_process_dead(worker.pid)
