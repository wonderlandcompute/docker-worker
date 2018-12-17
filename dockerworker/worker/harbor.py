from docker import DockerClient

from dockerworker.config import config
from dockerworker.log import logger, capture_exception

client = DockerClient(base_url=config.DOCKER_URL, version=config.DOCKER_API_VERSION, timeout=config.DOCKER_TIMEOUT)


def pull_image(image, tag="latest", *args, **kwargs):
    logger.debug("Pulling image {}".format(image))
    client.images.pull(image, tag=tag, *args, **kwargs)


def is_running(containter_id):
    running_ids = [c.id for c in client.containers.list()]
    return containter_id in running_ids


def create_container(image, **kwargs):
    logger.debug("Creating container for image {} with arguments: {}".format(image, kwargs))
    c = client.containers.create(image, **kwargs)
    return c.id


def start_container(container_id, **kwargs):
    attempts = 0
    while attempts < config.DOCKER_START_ATTEMPTS:
        logger.debug("Trying to start container id={}".format(container_id))
        try:
            c = client.containers.get(container_id)
            c.start(**kwargs)
            break
        except Exception as e:
            capture_exception()
            logger.debug("Failed to start container id={}, error: {}".format(container_id, e))
            attempts += 1

    if attempts < config.DOCKER_START_ATTEMPTS:
        logger.debug("Started container id={}".format(container_id))
        return True
    else:
        raise Exception('Failed to start container id={}'.format(container_id))


def logs(container_id, **kwargs):
    c = client.containers.get(container_id)
    return c.logs(**kwargs)


def remove(container_id, **kwargs):
    c = client.containers.get(container_id)
    return c.remove(**kwargs)


def REMOVE_ALL_CONTAINERS():
    "Use with caution"
    logger.debug("Killing and removing all containers!")
    all_ids = [c.id for c in client.containers.list(all=True)]
    for container_id in all_ids:
        for retries in range(20):
            try:
                c = client.containers.get(container_id)
                c.remove(force=True)
                break
            except:
                capture_exception()
                continue
