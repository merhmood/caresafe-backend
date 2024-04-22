import multiprocessing

# Default number of workers is usually 1, but you can increase it
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2