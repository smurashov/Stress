import novaclient.v1_1.client as nvclient
from utils import timecheck
import random


class nova():

    "Nova"

    def __init__(self, user, password, tenant, urls):
        self.nova = nvclient.Client(user, password, tenant, urls['keystone'],
                                    service_type="compute")

    @timecheck
    def create_instance(self, name, flavor, numb):

        image = self.nova.images.find(name=name)
        flavor = self.nova.flavors.find(name=flavor)
        instance = self.nova.servers.create(name="test" + str(numb),
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

    def random_action(self):
        k = random.randint(0, 100)
        if k < 101:
            return self.get_servers_list()