import signal
import sys

from wonderlandClient import new_client
from lockfile import LockFile

from .config import config
from .log import logger, capture_exception
from .worker import do_docker_job, Worker


def break_lock():
    try:
        return LockFile(config.LOCK_FILE).break_lock()
    except:
        pass


def sigquit_handler(n, f, worker):
    try:
        worker.fail_all()
    except:
        capture_exception()
        pass

    try:
        break_lock()
    except:
        capture_exception()
        pass
    sys.exit(0)


def main():
    break_lock()

    worker = Worker(
        new_client(),
        "docker",
        do_docker_job,
        threads_num=config.THREADS_NUM,
        sleep_time=config.SLEEP_TIME,
    )

    signal.signal(signal.SIGQUIT, lambda n, f: sigquit_handler(n, f, worker))

    logger.debug("Starting worker...")
    worker.start()


if __name__ == '__main__':
    main()
