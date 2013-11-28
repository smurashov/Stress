import psutil
import os
from multiprocessing import Process


class SystemLoad(Process):
    def run(self):
        while True:
            with open(os.getcwd() + '/metrics.txt', "a") as myfile:
                a = psutil.cpu_percent(interval=1, percpu=True)
                b = psutil.virtual_memory().used / 1024
                myfile.write(str(a) + "      " + str(b) + "\n")
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