import ConfigParser
import numpy as np
from Stress import Mirantis
import matplotlib.pyplot as pl
import os


config = ConfigParser.RawConfigParser()
config.read('config.ini')
user = config.get('keystone', 'user')
password = config.get('keystone', 'password')
tenant = config.get('keystone', 'tenant')
keystone_url = config.get('keystone', 'url')
numb = config.get('users', 'numb')
numb = numb.split()
filename = os.getcwd() + '/testresults.txt'
if os.path.isfile(os.getcwd() + '/myfig.png'):
    os.remove(os.getcwd() + '/myfig.png')
ki = []
for j in numb:
    if os.path.isfile(filename):
        os.remove(filename)
    procs = []
    for i in xrange(int(j)):
        p = Mirantis(i, user, password, tenant, keystone_url)
        procs.append(p)

    for m in procs:
        m.start()

    for s in procs:
        s.join()

    with open(filename) as f:
        content = f.readlines()
        k = 0
        for i in content:
            k += float(i.split()[0])
    ki.append(k / int(j))
pl.plot(ki, numb)
pl.savefig('myfig.png')
os.remove(filename)
