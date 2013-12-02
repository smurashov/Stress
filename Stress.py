from multiprocessing import Process
import time
from clients.nova import nova


class Mirantis(Process):

    def __init__(self, numb, duration, user, password, tenant, keystone_url):
        super(Mirantis, self).__init__()
        self.client = nova(user, password, tenant, keystone_url)
        self.numb = numb
        self.points = []
        self.duration = float(duration)

    def run(self):

        te = time.time()
        ts = time.time()
        while (ts - te) < self.duration:
            ts = time.time()
            self.client.random_action()
