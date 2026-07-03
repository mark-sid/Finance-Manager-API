import multiprocessing


bind = "0.0.0.0:8000"

worker_class = 'sync'
workers = 2 * multiprocessing.cpu_count()
threads = 2
worker_connections = 1000

timeout = 30
graceful_timeout = 30
keepalive = 2

accesslog = "gunicorn_access.log"
errorlog = "gunicorn_error.log"

loglevel = "info"

reload = True