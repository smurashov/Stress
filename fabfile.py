from fabric.api import env, run, hosts
env.user = 'root'
env.host = '10.20.0.2'
env.hostname = 'test'
env.password = 'r00tme'
env.hosts = ['root@10.20.0.2']
env.passwords = {'root@10.20.0.2': 'r00tme'}
def test():
    run('df -h')
