import psutil
import time
for x in xrange(3):
    print psutil.cpu_percent(interval=1, percpu=True)
for x in xrange(3):
    time.sleep(1)
    print psutil.virtual_memory()
