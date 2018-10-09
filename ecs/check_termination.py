#!/usr/local/bin/python -u

import os
import boto3
import requests
import traceback
from time import sleep
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s %(levelname)s %(message)s')

interval = int(os.environ.get('INTERVAL', 5))

class ECS():
    def __init__(self, region):
        self.client = boto3.client('ecs', region_name=region)
    def deregister(self, cluster, instance):
        res = client.deregister_container_instance(
            cluster=cluster,
            containerInstance=instance,
            force=True
        )


def get_region():
    availability_zone = requests.get('http://169.254.169.254/latest/meta-data/placement/availability-zone').text
    logger.info('Get Region from EC2 meta-data')
    return availability_zone[0:-1]

def get_metadata():
    res = requests.get('http://127.0.0.1:51678/v1/metadata')
    metadata = res.json()
    logger.info('Get metadata from ecs-agent')
    return metadata


if __name__ == '__main__':
    region = get_region()
    metadata = get_metadata()
    while True:
        try:
            res = requests.get('http://169.254.169.254/latest/meta-data/spot/termination-time')
            if res.status_code == 404:
                sleep(interval)
                continue
            elif res.status_code == 200:
                logger.info('Deregister this instance from the cluster')
                ecs = ECS(region)
                ecs.deregister(metadata['Cluster'], metadata['ContainerInstanceArn'])
            else:
                raise Exception
        except Exception as e:
            break
            traceback.print_exc()
