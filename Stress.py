from keystoneclient.v2_0 import client as ksclient
from multiprocessing import Process
from cinderclient import client as cindercl
import novaclient.v1_1.client as nvclient
import glanceclient.v2.client as glclient
import time
import random
import os


class Mirantis(Process):

    def __init__(self, numb, duration, user, password, tenant, keystone_url):
        super(Mirantis, self).__init__()
        keystone = ksclient.Client(username=user, password=password,
                                   tenant_name=tenant, auth_url=keystone_url)
        self.nova = nvclient.Client(user, password, tenant, keystone_url,
                                    service_type="compute")
        self.cinder = cindercl.Client('1', user, password,
                                      tenant, keystone_url)
        glance_endpoint = keystone.service_catalog.url_for(service_type='image',
                                                   endpoint_type='publicURL')
        self.glance = glclient.Client(glance_endpoint,
                                      token=keystone.auth_token)
        self.numb = numb
        self.points = []
        self.duration = float(duration)

    def timecheck(method):

        def timed(*args, **kw):
            ts = time.time()
            result = method(*args, **kw)
            te = time.time()
            with open(os.getcwd() + '/testresults.txt', "a") as myfile:
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
        return self.nova.servers.list()

    @timecheck
    def get_images_list(self):
        return self.glance.images.list()

    def run(self):

        te = time.time()
        ts = time.time()
        while (ts - te) < self.duration:
            k = random.randint(51, 100)
            ts = time.time()
            if k < 50:
                instance = self.create_instance()
                self.delete_instance(instance)
            elif k > 101:
                self.get_images_list()
            elif k < 100:
                self.get_servers_list()
