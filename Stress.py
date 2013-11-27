from keystoneclient.v2_0 import client as ksclient
from multiprocessing import Process
from cinderclient import client as cindercl
import novaclient.v1_1.client as nvclient
import time
import random
import ConfigParser

"""
config = ConfigParser.RawConfigParser()
config.read('config.ini')
user = config.get('keystone', 'user')
password = config.get('keystone', 'password')
tenant = config.get('keystone', 'tenant')
keystone_url = config.get('keystone', 'url')
"""

class Mirantis(Process):

    def __init__(self, numb, user, password, tenant, keystone_url):
        super(Mirantis, self).__init__()
        ksclient.Client(username=user, password=password,
                        tenant_name=tenant, auth_url=keystone_url)
        self.nova = nvclient.Client(user, password, tenant, keystone_url,
                                    service_type="compute")
        self.cinder = cindercl.Client('1', user, password,
                                      tenant, keystone_url)
        self.numb = numb
        self.points = []

    def timecheck(method):

        def timed(*args, **kw):
            ts = time.time()
            result = method(*args, **kw)
            te = time.time()
            with open('testresults.txt', "a") as myfile:
                myfile.write(str(te - ts) + "  " + method.__name__ + '\n')
            return result

        return timed

    """
    @timecheck
    def volume_create_and_delete(self):

        volume = self.cinder.volumes.create(display_name="test-vol" +
                                                         str(self. numb),
                                            size=1)
        volume.delete
    """

    @timecheck
    def create_instance(self):

        image = self.nova.images.find(name="demo")
        flavor = self.nova.flavors.find(name="m1.micro")
        instance = self.nova.servers.create(name="test" + str(self.numb),
                                            image=image, flavor=flavor)
        status = instance.status
        while status == 'BUILD':
            instance = self.nova.servers.get(instance.id)
            status = instance.status
        return instance.name

    @timecheck
    def delete_instance(self, name):
        server = self.nova.servers.find(name=name)
        server.delete()
        server = self.nova.servers.find(name=name)
        while server.status == 'ACTIVE':
            server = self.nova.servers.find(name=name)

    @timecheck
    def get_servers_list(self):
        servers = self.nova.servers.list()
        return servers

    def run(self):
        k = random.randint(51, 100)
        if k < 50:
            instance = self.create_instance()
            self.delete_instance(instance)
        elif k < 100:
            self.get_servers_list()
