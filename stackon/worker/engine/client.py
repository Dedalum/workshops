import json
import threading
import time
from threading import Thread

import paho.mqtt.client as mqtt
from model.job import BadJobDefinitionException, Job

TOPIC = "workerpy"


class Client:
    def __init__(self, client_id):
        self.job_nb = 0
        self.threads = {}
        self.mqtt_client = mqtt.Client(client_id=client_id)
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

        client.subscribe("{}/{}/#".format(TOPIC, client._client_id.decode("utf-8")))

    def on_message(self, client, userdata, msg):
        base_topic = "{}/{}".format(TOPIC, client._client_id.decode("utf-8"))
        print(msg.topic + " " + str(msg.payload))

        if msg.topic == "{}/job".format(base_topic):
            self.job_nb += 1
            self.threads[self.job_nb] = Thread(
                target=self.handle_job,
                args=(str(msg.payload.decode("utf-8")), self.job_nb),
            )
            self.threads[self.job_nb].start()

    def handle_job(self, msg, job_nb):
        job = Job(job_nb)
        try:
            job.load(msg)
            res = job.run()
            # pub result

        except BadJobDefinitionException as err:
            print("Failed running job: {}".format(err))
            return

        # print("DEBUG: {}".format(self.threads))
        # print("Removing thread {} from list".format(self.threads.pop(job_nb)))
        return

    def handle_threads(self):
        last = time.time()
        while True:
            print("DEBUG: current threads: {}".format(len(threading.enumerate())))
            last += 5
            try:
                time.sleep(last - time.time())
            except ValueError:
                pass

    def run(self):

        # daemon set to True allows us to exit the program without waiting for
        # this thread to be complete (it never completes)
        thread_handler = Thread(target=self.handle_threads, daemon=True)
        thread_handler.start()
        self.mqtt_client.connect("127.0.0.1", 1883, 60)

        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        self.mqtt_client.loop_forever()
