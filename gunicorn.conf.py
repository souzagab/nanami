import os
import multiprocessing

# Default settings
host = os.getenv('HOST', '0.0.0.0')
port = os.getenv('PORT', '3000')
default_bind = f'{host}:{port}'
default_workers = multiprocessing.cpu_count() * 2 + 1
default_timeout = 120
default_keepalive = 5
default_loglevel = 'info'

# Settings with environment variable overrides
bind = os.getenv('BIND', default_bind)
workers = int(os.getenv('WORKERS', default_workers))
timeout = int(os.getenv('TIMEOUT', default_timeout))
keepalive = int(os.getenv('KEEP_ALIVE', default_keepalive))
loglevel = os.getenv('LOG_LEVEL', default_loglevel)
worker_class = 'uvicorn.workers.UvicornWorker'
accesslog = '-'
errorlog = '-'