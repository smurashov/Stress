from keystone import keystone
import requests
import random
import os
import sys
possible_topdir = os.path.normpath(os.path.join(os.path.abspath(__file__),
                                                os.pardir,
                                                os.pardir,
                                                os.pardir))
if os.path.exists(os.path.join(possible_topdir,
                               'Stress',
                               '__init__.py')):
    sys.path.insert(0, possible_topdir)
from utils import timecheck

class MuranoMetaRepo():

    "Murano"

    def __init__(self, user, password, tenant, urls):
        client = keystone.keystone_auth(user, password, tenant,
                                        urls['keystone'])
        self.headers = {'X-Auth-Token': client.auth_token}
        self.metadata_url = urls['metadata_url']

    @timecheck
    def get_list_metadata_objects(self, path):
        resp = requests.get('%s/v1/admin/%s' % (self.metadata_url, path),
                            headers=self.headers)
        return resp

    def random_action(self):
        k = random.randint(0, 100)
        if k < 101:
            return self.get_list_metadata_objects('services')
