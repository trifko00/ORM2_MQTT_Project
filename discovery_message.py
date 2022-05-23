import json


class DiscoveryMessage:
    def __init__(self, id=0, ip='127.0.0.1',
                 manual=True, actuators={}, sensors={}):
        self.id = id
        self.ip = ip
        self.manual = manual
        self.actuators = actuators
        self.sensors = sensors

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


if __name__ == "__main__":
    # serialization test goes here!
    print("Serialization test")
