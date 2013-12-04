import threading
import time
#import sys
#import inspect
from gevent import monkey

monkey.patch_all(socket=True, dns=True, time=True, select=True,
                 thread=True, os=True, ssl=True, httplib=False,
                 subprocess=False, sys=False, aggressive=True,
                 Event=False)


class Mirantis(threading.Thread):

    def __init__(self, numb, duration, client):
        threading.Thread.__init__(self)
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

