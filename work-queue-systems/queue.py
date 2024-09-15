import requests
import json
from kubernetes import client,config
import time

namespace = "default"

def make_container(item,obj):
    container = client.V1Container()
    container.image = "my/worker-image"
    container.name = "worker"
    return container

def make_job(item):
    response = requests.get("http://localhost:8000/item/{}".format(item))
    obj = json.loads(response.text)
    job = client.V1Job()
    job.metadata = client.V1ObjectMeta()
    job.metadata.name = item
    job.spec = client.V1JobSpec()
    job.spec.template = client.V1PodTemplate()
    job.spec.template.spec = client.V1PodTemplateSpec()
    job.spec.template.spec.restart_policy = "Never"
    job.spec.template.spec.container = [
        make_container(item,obj)
    ]
    return job


def update_queue(batch):
    response = requests.get("http://localhost:8000/items")
    obj = json.loads(response.text)
    items = obj['items']

    ret = batch.list_namespace_job(namespace,watch=False)
    for item in items:
        found = False
        for i in ret.items:
            if i.metadata.name == item:
                found = True
            if not found:
                job = make_job(item)
                batch.create_namespaced_job(namespace, job)
    

config.load_kube_config()
batch = client.BatchV1Api()

while True:
    update_queue(batch)
    time.sleep(10)


