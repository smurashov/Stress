import ConfigParser
import numpy as np
from Stress import Mirantis
import matplotlib.pyplot as pl
import requests
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
if os.path.isdir(os.getcwd() + '/images'):
    for i in os.listdir(os.getcwd() + '/images'):
        os.remove(os.getcwd() + '/images/' + i)
    os.rmdir(os.getcwd() + '/images')
ki = []
RAM = []
os.mkdir('images')
for j in numb:
    print j + " users working"
    if os.path.isfile(filename):
        os.remove(filename)
    procs = []
    for i in xrange(int(j)):
        p = Mirantis(i, user, password, tenant, keystone_url)
        procs.append(p)

    r = requests.get("http://127.0.0.1:7007/start")

    for m in procs:
        m.start()

    for s in procs:
        s.join()

    r = requests.get("http://127.0.0.1:7007/stop")

    with open(filename) as f:
        content = f.readlines()
        k = 0
        for i in content:
            k += float(i.split()[0])
    ki.append(k / int(j))
    mass = []
    r = requests.get("http://127.0.0.1:7007/metrics")
    for x in r.text.strip('[').strip(']').strip(',').split():
        mass.append(float(x.encode('utf-8'
                                   '').strip('[').strip(']').strip(',')))
    RAM.append(sum(filter(lambda x: x > 100,
                          mass)) / len(filter(lambda x: x > 100, mass)))
    CPU = filter(lambda x: x <= 100, mass)
    CPU_numb = len(CPU) / len((filter(lambda x: x > 100, mass)))
    d = [[] for x in xrange(CPU_numb)]
    flag = 0
    for z in xrange(len(CPU)):
        x = z - flag * CPU_numb
        d[x].append(CPU[z])
        if (x + 1) % len(d) == 0:
            flag += 1
    if j == numb[0]:
        CPUs = [[] for x in xrange(CPU_numb)]
    for z in xrange(len(d)):
        CPUs[z].append(d[z][0])
for i in xrange(len(numb)):
    numb[i] = int(numb[i])
for i in xrange(len(CPUs)):
    print CPUs[i]
    pl.bar(numb, CPUs[i], facecolor='#9999ff', edgecolor='white', width=0.5)
    pl.title('CPU' + str(i+1) + 'usage graph')
    pl.xlabel('Users')
    pl.ylabel('CPU_usage%')
    pl.xticks(numb)
    pl.savefig('images/' + 'CPU' + str(i+1) + '_usage.png')
    pl.close()
pl.bar(numb, ki, facecolor='#9999ff', edgecolor='white', width=0.5)
pl.title('Get instance list action')
pl.xlabel('Users')
pl.ylabel('Time')
pl.xticks(numb)
pl.savefig('images/get_instances_list.png')
pl.close()
pl.bar(numb, RAM, facecolor='#9999ff', edgecolor='white', width=0.5)
pl.title('RAM usage graph')
pl.xlabel('Users')
pl.ylabel('RAM_usage')
pl.xticks(numb)
pl.savefig('images/RAM_usage.png')
pl.close()
os.remove(filename)
