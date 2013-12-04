from multiprocessing import Process
import time
import sys
import inspect


class Mirantis(Process):

    def __init__(self, numb, duration, client):
        super(Mirantis, self).__init__()
        """
        for name, obj in inspect.getmembers(sys.modules[clients.__name__]):
            if inspect.ismodule(obj):
                for name1, obj1 in inspect.getmembers(
                        sys.modules[obj.__name__]):
                    if inspect.isclass(obj1):
                        if service in str(obj1):
                            self.client = obj1(user, password, tenant, urls)
                            print obj1
        """
        self.client = client
        self.numb = numb
        self.points = []
        self.duration = float(duration)

    def run(self):

        t_start = time.time()
        while (time.time() - t_start) < self.duration:
            try:
                self.client.random_action()
            except:
                print "Error"

