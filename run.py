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
if os.path.isfile(os.getcwd() + '/get_instances_list.png'):
    os.remove(os.getcwd() + '/get_instances_list.png')
if os.path.isfile(os.getcwd() + '/cpuRAM.txt'):
    os.remove(os.getcwd() + '/cpuRAM.txt')
if os.path.isfile(os.getcwd() + '/RAM_usage.png'):
    os.remove(os.getcwd() + '/RAM_usage.png')
ki = []
RAM = []
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
    with open(os.getcwd() + '/cpuRAM.txt', "a") as myfile:
        myfile.write(r.text)
        for x in r.text.strip('[').strip(']').strip(',').split():
            mass.append(float(x.encode('utf-8'
                                       '').strip('[').strip(']').strip(',')))
        RAM.append(sum(filter(lambda x: x > 100,
                              mass)) / len(filter(lambda x: x > 100, mass)))
        CPU = filter(lambda x: x <= 100, mass)
        CPU_numb = len(CPU) / len((filter(lambda x: x > 100, mass)))
        print CPU
        d = [[] for x in xrange(CPU_numb)]
for i in xrange(len(numb)):
    numb[i] = int(numb[i])
pl.bar(numb, ki, facecolor='#9999ff', edgecolor='white', width=0.5)
pl.title('Get instance list action')
pl.xlabel('Users')
pl.ylabel('Time')
pl.savefig('get_instances_list.png')
pl.bar(numb, RAM, facecolor='#9999ff', edgecolor='white', width=0.5)
pl.title('RAM usage graph')
pl.xlabel('Users')
pl.ylabel('RAM_usage')
pl.savefig('RAM_usage.png')
os.remove(filename)
