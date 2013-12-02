from multiprocessing import Process
import time
import clients
from clients.nova import nova
from clients.metadatarepo import MuranoMetaRepo
import sys
import inspect


class Mirantis(Process):

    def __init__(self, numb, duration, user, password, tenant, urls, service):
        super(Mirantis, self).__init__()
        for name, obj in inspect.getmembers(sys.modules[__name__]):
            if inspect.isclass(obj):
                if service in str(obj):
                    print obj
                    self.client = obj(user, password, tenant, urls)
        self.numb = numb
        self.points = []
        self.duration = float(duration)

    def run(self):

        t_start = time.time()
        while (time.time() - t_start) < self.duration:
            self.client.random_action()
