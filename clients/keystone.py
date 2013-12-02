from keystoneclient.v2_0 import client as ksclient


class keystone():

    @classmethod
    def keystone_auth(cls, user, password, tenant, keystone_url):
        keystone = ksclient.Client(username=user, password=password,
                                   tenant_name=tenant, auth_url=keystone_url)
        return keystone

