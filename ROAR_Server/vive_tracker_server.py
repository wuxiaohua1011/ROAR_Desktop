"""
Implementation of a Vive Tracker Server

For example client implementation, please visit
https://github.com/augcog/ROAR_Jetson/blob/revamp/vive/vive_tracker_client.py


"""

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
from typing import List


class ViveTrackerServer(ROARServer):
    """
    Defines a UDP vive tracker server that constantly "shout out" messages at (HOST, PORT)

    Utilizes OpenVR as its interaction with SteamVR. For hardware setup, please see this tutorial:
    http://help.triadsemi.com/en/articles/836917-steamvr-tracking-without-an-hmd

    """

    def __init__(self, host: str, port: int, record_data: bool = False,
                 output_file_path: Path = Path("./data/RFS_track.txt")):
        super().__init__(host, port)
        self.triad_openvr: Optional[TriadOpenVR] = self.reconnect_triad_vr(debug=True)
        self.record_data = record_data
        self.output_file_path = output_file_path
        self.output_file = None
        if record_data and self.output_file_path.exists() is False:
            self.output_file_path.parent.mkdir(parents=True, exist_ok=True)
        self.output_file = self.output_file_path.open('w')

    def run(self):
        """
        Initialize a server that runs forever.

        This server can be put into a multi-process module to run concurrently with other servers.

        Returns:
            None
        """
        while True:
            for tracker_name in self.get_tracker_names():
                message = self.poll(tracker_name)
                self.logger.info(message)
                if message is not None:
                    socket_message = self.construct_socket_msg(message)
                    self.socket.sendto(socket_message.encode(), (self.host, self.port))
                    if self.record_data:
                        self.record(message)

    def poll(self, tracker_name) -> Optional[ViveTrackerMessage]:
        """
        Polls tracker message by name

        Note:
            Server will attempt to reconnect if tracker name is not found.

        Args:
            tracker_name: the vive tracker message intended to poll

        Returns:
            ViveTrackerMessage if tracker is found, None otherwise.
        """
        tracker = self.get_tracker(tracker_name=tracker_name)
        if tracker is not None:
            message: Optional[ViveTrackerMessage] = self.create_tracker_message(tracker=tracker,
                                                                                tracker_name=tracker_name)
            return message
        else:
            self.reconnect_triad_vr()
        return None

    def get_tracker(self, tracker_name):
        """
        Given tracker name, find the tracker instance

        Args:
            tracker_name: desired tracker's name to find

        Returns:
            tracker instance if found, None otherwise
        """
        return self.triad_openvr.devices.get(tracker_name, None)

    def create_tracker_message(self, tracker, tracker_name) -> Optional[ViveTrackerMessage]:
        """
        Create tracker message given tracker and tracker name

        Note:
            it will attempt to reconnect to OpenVR if conversion or polling from tracker went wrong.

        Args:
            tracker: tracker instance
            tracker_name: the tracker's name corresponding to this tracker

        Returns:
            Vive tracker message if this is a successful conversion, None otherwise

        """
        try:
            euler = tracker.get_pose_euler()
            vel_x, vel_y, vel_z = tracker.get_velocity()
            x, y, z, yaw, pitch, roll = euler
            message = ViveTrackerMessage(valid=True, x=-x, y=y, z=-z,
                                         yaw=yaw, pitch=pitch, roll=roll,
                                         vel_x=vel_x, vel_y=vel_y, vel_z=vel_z,
                                         device_name=tracker_name)
            return message
        except OSError as e:
            print(f"OSError: {e}. Need to restart Vive Tracker Server")
            self.reconnect_triad_vr()
        except Exception as e:
            print(f"Cannot find Tracker {tracker} is either offline or malfunctioned")
            self.reconnect_triad_vr()
            return None

    def construct_socket_msg(self, data: ViveTrackerMessage) -> str:
        """
        Send vive tracker message to socket

        Args:
            data: ViveTracker Message to send

        Returns:
            message in string to send

        """
        json_data = json.dumps(data.json(), sort_keys=False)
        json_data = "&" + json_data
        json_data = json_data + "\r"  # * (512 - len(json_data))
        return json_data

    def reconnect_triad_vr(self, debug=False):
        """
        Attempt to reconnect to TriadOpenVR

        Notes:
            this method will automatically assign self.triad_openvr

        Args:
            debug: **deprecated flag

        Returns:
            openvr instance
        """
        from ROAR_Jetson.vive.triad_openvr import TriadOpenVR
        openvr = TriadOpenVR()

        if debug:
            self.logger.debug(
                f"Trying to reconnect to OpenVR to refresh devices. "
                f"Devices online:")
            pprint(openvr.devices)
        self.triad_openvr = openvr
        return openvr

    def get_tracker_names(self) -> List[str]:
        """
        Get a list of trackers

        Returns:
            list of tracker names

        """
        result = []
        for device_name in self.triad_openvr.devices.keys():
            if "tracker" in device_name:
                result.append(device_name)
        return result

    def record(self, data: ViveTrackerMessage):
        """
        Record the current data

        Args:
            data: current ViveTrackerMessage to record

        Returns:
            None
        """
        x, y, z, roll, pitch, yaw = data.x, data.y, data.z, data.roll, data.pitch, data.yaw
        recording_data = f"{x}, {y},{z},{roll},{pitch},{yaw}"
        m = f"Recording: {recording_data}"
        self.logger.info(m)
        self.output_file.write(recording_data + "\n")


if __name__ == "__main__":
    HOST, PORT = "192.168.1.19", 8000
    vive_tracker_server = ViveTrackerServer(host=HOST, port=PORT, record_data=False)
    logging.basicConfig(format='%(asctime)s|%(name)s|%(levelname)s|%(message)s',
                        datefmt="%H:%M:%S", level=logging.INFO)
    vive_tracker_server.run()
