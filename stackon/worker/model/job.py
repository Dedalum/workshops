"""
Job
"""

import json

import gevent


class Job:
    def __init__(self, job_id):
        self.task = None
        self.gid = None
        self.id = job_id

    def __str__(self):
        return "Job {}: {}".format(self.id, self.task)

    def load(self, json_msg):
        try:
            job_def = json.loads(json_msg)
        except json.decoder.JSONDecodeError as err:
            raise BadJobDefinitionException("Could not decode job: {}".format(err))

        try:
            self.task = job_def["task"]
            self.gid = job_def["gid"]
        except KeyError as err:
            raise BadJobDefinitionException("Could not set job: {}".format(err))

    def run(self):
        print("running job {} for group {}".format(self.task, self.gid))

        # run the job: create the "connector" that runs the various parts of
        # the job: iter_acc, iter_hist, etc. in their own greenlets
        self._fake_ticker()
        return '{"result":"123"}'

    def _fake_ticker(self):
        for i in range(5):
            print("{}: ticking {}...".format(str(self), i))
            gevent.sleep(1)


class BadJobDefinitionException(Exception):
    pass
