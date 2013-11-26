from keystoneclient.v2_0 import client as ksclient
from multiprocessing import Process
from cinderclient import client as cindercl
import novaclient.v1_1.client as nvclient
import time

user = 'sergey_demo_user'
password = '111'
tenant = 'ForTests'
keystone_url = 'http://172.18.124.201:5000/v2.0/'


class Mirantis(Process):

    def __init__(self, numb):
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
            with open("test.txt", "a") as myfile:
                myfile.write(str(te - ts) + '\n')
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

    def run(self):
        instance = self.create_instance()
        self.delete_instance(instance)


procs = []
for i in xrange(2):
    p = Mirantis(i)
    procs.append(p)

for m in procs:
    m.start()

for j in procs:
    j.join()