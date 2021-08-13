import sys

import paho.mqtt.client as mqtt


class Client:
    def __init__(self, client_id):
        self.mqtt_client = mqtt.Client(client_id=client_id)
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

    def on_message(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))

    def publish(self, topic, payload):
        self.mqtt_client.publish(topic, payload)


def main():
    if len(sys.argv) < 2:
        print("Missing args: cmd <topic> <payload>")
        return

    mqtt_client = Client("test-client")
    mqtt_client.mqtt_client.connect("127.0.0.1", 1883, 60)
    mqtt_client.publish(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()
