import ConfigParser
import numpy as np
from Stress import Mirantis
from utils import helptools
import requests
import os
import clients
from clients.nova import nova
from clients.metadatarepo import MuranoMetaRepo

urls = {}
config = ConfigParser.RawConfigParser()
config.read('config.ini')
service = config.get('users', 'testing_service')
agent = config.get('agent', 'agent_url')
user = config.get('keystone', 'user')
password = config.get('keystone', 'password')
tenant = config.get('keystone', 'tenant')
keystone_url = config.get('keystone', 'url')
urls.setdefault('keystone', keystone_url)
metadata_url = config.get('murano', 'metadata_url')
urls.setdefault('metadata_url', metadata_url)
numb = config.get('users', 'numb')
numb = numb.split()
duration = config.get('users', 'duration')
filename = os.getcwd() + '/testresults.txt'
if os.path.isdir(os.getcwd() + '/images'):
    for i in os.listdir(os.getcwd() + '/images'):
        os.remove(os.getcwd() + '/images/' + i)
    os.rmdir(os.getcwd() + '/images')
ki = []
RAM = []
os.mkdir('images')
for j in numb:
    print j + " users starting"
    if os.path.isfile(filename):
        os.remove(filename)
    procs = []
    for i in xrange(int(j)):
        p = Mirantis(i, duration, user, password, tenant, urls, service)
        procs.append(p)

    r = requests.get("%s/start" % agent)

    for m in procs:
        m.start()

    print j + " working"

    for s in procs:
        s.join()

    r = requests.get("%s/stop" % agent)

    with open(filename) as f:
        content = f.readlines()
        k = 0
        for i in content:
            k += float(i.split()[0])
    ki.append(k / len(content))
    if os.path.isfile(filename):
        os.remove(filename)
    mass = []
    r = requests.get("%s/metrics" % agent)
    mass = helptools.pars(r)
    RAM.append(helptools.RAM_average(mass) / 100000)
    CPU = helptools.CPU_data(mass)
    CPU_numb = helptools.CPU_numb(CPU, mass)
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
    helptools.draw(numb, CPUs[i], title='CPU' + str(i+1) + 'usage graph',
                   xlab='Users', ylab='CPU_usage%',
                   filename='CPU' + str(i+1) + '_usage.png')
helptools.draw(numb, ki, title='Get instance list action',
               xlab='Users', ylab='Time(seconds)',
               filename='get_instances_list.png')
helptools.draw(numb, RAM, title='RAM usage graph',
               xlab='Users', ylab='RAM_usage',
               filename='RAM_usage.png')
if os.path.isfile(filename):
    os.remove(filename)
