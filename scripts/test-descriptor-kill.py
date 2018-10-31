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
    # Job.KILLED,
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

    killed = False

    while True:

        if job.status == Job.RUNNING and not killed:
            input_ = job.input
            output_ = job.output

            # kill
            # TODO: stub.KillJob(RequestWithId(id=job.id)) without job =?
            # TODO: ContinueJob?
            job = stub.KillJob(RequestWithId(id=job.id))
            assert job.status == Job.KILLED, f"job is not killed: {job.status}"
            assert input_ == job.input, "input is changed"
            assert output_ == job.output, "output is changed"
            print("[{}] Job :\n {}\n".format(time.time(), job))
            print("job is killed.\nwait...")

            # wait
            time.sleep(5)

            # continue
            job.status = Job.PENDING
            job = stub.CreateJob(job)
            assert job.status in STATUS_IN_PROCESS, "job is not in progress"
            print("...continue\n\n")

            killed = True

        time.sleep(3)
        job = stub.GetJob(RequestWithId(id=job.id))
        print("[{}] Job :\n {}\n".format(time.time(), job))

        if job.status in STATUS_FINAL:
            break

    if job.status == Job.KILLED:
        print("Job is killed!")

    if job.status == Job.FAILED:
        print("Job failed!")

    # print("result:", json.loads(job.output))


if __name__ == '__main__':
    main()
