import sys
from pathlib import Path
import os

print(Path(os.getcwd()).parent.parent.as_posix())
sys.path.append(Path(os.getcwd()).parent.parent.as_posix())

import socketserver
from typing import Any, Optional, Dict
from ROAR_Jetson.vive.triad_openvr import TriadOpenVR
import logging
from ROAR_Jetson.vive.models import ViveTrackerMessage
import json
from pprint import pprint
from ROAR_Desktop.ROAR_Server.base_server import ROARServer

triad_openvr: Optional[TriadOpenVR] = None


def reconnect_triad_vr():
    global triad_openvr
    print(
        f"Trying to reconnect to OpenVR to refresh devices. "
        f"Devices online:")
    triad_openvr = TriadOpenVR()
    pprint(triad_openvr.devices)


def get_tracker(tracker_name):
    global triad_openvr
    return triad_openvr.devices.get(tracker_name, None)


def create_tracker_message(tracker, tracker_name):
    try:
        euler = tracker.get_pose_euler()
        vel_x, vel_y, vel_z = tracker.get_velocity()
        x, y, z, yaw, pitch, roll = euler
        message = ViveTrackerMessage(valid=True, x=-x, y=y, z=z,
                                     yaw=yaw, pitch=pitch, roll=roll,
                                     vel_x=vel_x, vel_y=vel_y, vel_z=vel_z,
                                     device_name=tracker_name)
        return message
    except:
        print(f"Cannot find Tracker {tracker} is either offline or malfunctioned")
        reconnect_triad_vr()
        return None


def construct_json_message(data: ViveTrackerMessage) -> str:
    json_data = json.dumps(data.json(), sort_keys=False, indent=2)
    json_data += ";"
    return json_data


def poll(tracker_name) -> Optional[ViveTrackerMessage]:
    tracker = get_tracker(tracker_name=tracker_name)
    if tracker is not None:
        message: Optional[ViveTrackerMessage] = create_tracker_message(tracker=tracker,
                                                                       tracker_name=tracker_name)
        return message
    else:
        reconnect_triad_vr()
    return None

class ViveTrackerUDPMessageHandler(socketserver.DatagramRequestHandler):
    def handle(self):
        global triad_openvr
        if triad_openvr is None:
            reconnect_triad_vr()
        tracker_name = self.request[0].strip().decode()
        socket = self.request[1]
        message: Optional[ViveTrackerMessage] = poll(tracker_name=tracker_name)
        print("message = ", message)
        if message is not None:
            message = (construct_json_message(data=message))
            socket.sendto(message.encode(), self.client_address)


class ViveTrackerServer(ROARServer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.server = socketserver.UDPServer((self.host, self.port), ViveTrackerUDPMessageHandler)

    def run(self):
        self.server.serve_forever()


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(name)s '
                               '- %(levelname)s - %(message)s',
                        level=logging.DEBUG)
    HOST, PORT = "192.168.1.19", 8000
    vive_tracker_server = ViveTrackerServer(host=HOST, port=PORT)
    vive_tracker_server.run()
