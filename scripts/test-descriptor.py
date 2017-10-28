#!/usr/bin/env python

import json
import signal
import sys
from multiprocessing import Queue
from time import time

from disneylandClient import Job
from google.protobuf.json_format import Parse
from lockfile import LockFile

from dockerworker.config import config
from dockerworker.worker import do_docker_job


def break_lock():
    try:
        LockFile(config.LOCK_FILE).break_lock()
    except:
        pass


def sigquit_handler(n, f):
    # kill_all_containers()
    break_lock()
    sys.exit(0)


def main():
    break_lock()
    signal.signal(signal.SIGQUIT, sigquit_handler)
    assert len(sys.argv) == 2, "input file is needed"
    queue = Queue()
    job = Job()
    job.id = 2

    job.input = json.dumps(json.loads(open(sys.argv[1]).read()))

    do_docker_job(job, queue)
    Parse(queue.get(), job)
    print job


if __name__ == '__main__':
    main()
