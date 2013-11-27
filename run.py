import ConfigParser
from Stress import Mirantis

config = ConfigParser.RawConfigParser()
config.read('config.ini')
user = config.get('keystone', 'user')
password = config.get('keystone', 'password')
tenant = config.get('keystone', 'tenant')
keystone_url = config.get('keystone', 'url')
numb = config.get('users', 'numb')
numb = numb.split()

for j in numb:
    procs = []
    for i in xrange(int(j)):
        p = Mirantis(i, user, password, tenant, keystone_url)
        procs.append(p)

    for m in procs:
        m.start()

    for j in procs:
        j.join()
"""
with open('testresults.txt') as f:
    content = f.readlines()
    k = 0
    for i in content:
        k += float(i.split()[0])
    print k / n
"""