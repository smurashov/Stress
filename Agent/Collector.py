import psutil
import os
from multiprocessing import Process


class SystemLoad(Process):
    def run(self):
        while True:
            with open(os.getcwd() + '/methrics.txt', "a") as myfile:
                a = psutil.cpu_percent(interval=1, percpu=True)
                b = psutil.virtual_memory()
                myfile.write(str(a) + "      " + str(b))
mass = []


def start():
    p = SystemLoad()
    global mass
    mass.append(p)
    p.start()
    return None


def stop():
    global mass
    for i in mass:
        i.terminate()
    return None