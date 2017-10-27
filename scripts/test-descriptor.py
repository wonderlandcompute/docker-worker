#!/usr/bin/env python

import json
import signal
import sys
from time import time
from lockfile import LockFile

from dockerworker.config import config
from dockerworker.worker import do_docker_job


class JobPH(object):
    """Phony job class"""

    def __init__(self, status='', descriptor=None, output=None):
        self.input = descriptor
        self.id = None
        self.status = status
        self.output = output

    def update_status(self, status):
        self.status = status
        return {u'success': True, u'updated_status': status}

    def update_output(self, output):
        self.output = output
        return {u'success': True, u'updated_output': output}

    def delete(self):
        return None

    def json(self):
        return json.dumps({
            'job_id': self.id,
            'status': self.status,
            'descriptor': self.input
        })


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

    job = JobPH()
    job.id = "job_{}".format(time())

    job.input=json.dumps(json.loads(open(sys.argv[1]).read()))

    do_docker_job(job)
    print job.output


if __name__ == '__main__':
    main()
