#! /usr/bin/env python

from string import Template
import uuid

from docker.client import Client
from docker.utils import kwargs_from_env
import docker

from os import environ
from time import sleep
import sys

DOCKER_HOST = "172.17.0.1"
# DOCKER_HOST = environ['DOCKER_HOST'].replace('tcp', 'http')


def write_template(client, listeners):
    hosts = []
    host_string = ""
    upstream = 'proxy_pass http://backend_hosts;'
    if len(listeners) > 0:
        for listener in listeners:
            for port in listener['Ports']:
                if port['PrivatePort'] == 8080:
                    hosts.append("%s:%d" % (DOCKER_HOST, port['PublicPort']))
                    break
        for host in hosts:
            host_string += "server %s;\n" % host
    else:
        # force 50x error
        upstream = 'fastcgi_pass unix:/does/not/exist;'
        host_string = 'server 127.0.0.1;'

    filein = open('default.conf.tpl', 'r')
    src = Template(filein.read())

    result = src.substitute({'hosts': host_string, 'upstream': upstream})

    target = open('nginx-conf.d/default.conf', 'w')
    target.truncate()
    target.write(result)
    target.close()


def run_listener(client, cluster_id):
    container = client.create_container(
        image='containersol/cattlestore',
        # command='"--delay 1"',
        ports=[8080],
        host_config=client.create_host_config(port_bindings={8080: None}),
        labels={'cluster_id' : cluster_id})
    response = client.start(container=container.get('Id'))
    if response is None:
        return container.get('Id')


def sync(client, cluster_id):
    # cluster = {
    #     'proxies': [],
    #     'listeners_unhealthy': [],
    #     'listeners_healthy': [],
    #     'listeners_dead': []
    # }
    listeners = []
    containers = client.containers(
        filters={'label': 'cluster_id=%s' % cluster_id})
    for container in containers:
        listeners.append(container)
    return listeners

# def run_proxy(client, cluster_id):
#     container = client.create_container(
#         image='nginx',
#         ports=[80],
#         host_config=client.create_host_config(port_bindings={80:8080}),
#         labels=['cluster_id=' + cluster_id])
#     response = client.start(container=container.get('Id'))
#     if response is None:
#         return container.get('Id')


def log(str):
    print(str)
    sys.stdout.flush()

def reload_proxy(client):
    for _ in range(1):
        try:
            exec_id = client.exec_create(
                container='wheeloffortune_proxy_1',
                cmd='nginx -s reload')
            client.exec_start(exec_id['Id'])
            sleep(1)
        except (docker.errors.APIError):
            pass

if __name__ == "__main__":
    cluster_id = uuid.uuid4().hex
    log("Cluster ID: %s" % cluster_id)

    client = Client(**kwargs_from_env(assert_hostname=False))

    # run_proxy(client, cluster_id)

    while(True):
        listeners = sync(client, cluster_id)
        # write_template(client, listeners)

        # Have at least 4 listeners available
        log("I have %d listeners" % len(listeners))
        for _ in range(len(listeners), 4):
            run_listener(client, cluster_id)

        listeners = sync(client, cluster_id)
        write_template(client, listeners)
        reload_proxy(client)
        sleep(.5)
