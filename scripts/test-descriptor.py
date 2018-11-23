import time
import json
import sys

from wonderlandClient import (
    new_client,
    Job,
    RequestWithId,
)

STATUS_IN_PROCESS = set([
    Job.PENDING,
    Job.PULLED,
    Job.RUNNING,
])
STATUS_FINAL = set([
    Job.COMPLETED,
    Job.FAILED,
])


def main():

    stub = new_client()

    assert len(sys.argv) == 2, "input file is needed"

    job = Job(
        input=json.dumps(json.loads(open(sys.argv[1]).read())),
        kind="docker",
    )

    job = stub.CreateJob(job)
    print("Job", job)

    while True:
        time.sleep(10)
        job = stub.GetJob(RequestWithId(id=job.id))
        print("[{}] Job :\n {}\n".format(time.time(), job))

        if job.status in STATUS_FINAL:
            break

    if job.status == Job.FAILED:
        print("Job failed!")

    print("result:", json.loads(job.output))


if __name__ == '__main__':
    main()
