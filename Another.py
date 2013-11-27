import psutil
for x in xrange(3):
   print psutil.cpu_percent(interval=1, percpu=True)
